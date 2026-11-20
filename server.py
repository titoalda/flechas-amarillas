#!/usr/bin/env python3
"""Servidor de la web: sirve site/ y recibe reservas en POST /api/reserva.

Cada reserva se guarda en data/reservas.jsonl y, si hay SMTP configurado,
se avisa por correo. Solo biblioteca estándar.

Variables de entorno:
  PORT            puerto (8622)
  SMTP_URL        smtps://usuario:contraseña@servidor:465  o  smtp://...:587 (STARTTLS)
  RESERVAS_TO     a quién se avisa de cada reserva
  RESERVAS_FROM   remitente (por defecto, el usuario del SMTP)
"""
import json
import os
import re
import smtplib
import ssl
import threading
import time
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import formataddr
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

RAIZ = Path(__file__).parent
SITE = RAIZ / "site"
DATA = Path(os.environ.get("DATA_DIR", RAIZ / "data"))
DATA.mkdir(parents=True, exist_ok=True)
PORT = int(os.environ.get("PORT", "8622"))
SMTP_URL = os.environ.get("SMTP_URL", "")
RESERVAS_TO = os.environ.get("RESERVAS_TO", "")
RESERVAS_FROM = os.environ.get("RESERVAS_FROM", "")

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")
LIMITE = 5          # solicitudes por IP
MAX_FICHERO = 20 * 1024 * 1024  # tope del fichero de solicitudes (unas 40.000)
VENTANA = 3600      # en una hora
_vistos: dict[str, list[float]] = {}
_lock = threading.Lock()


LIMITE_GLOBAL = 100  # avisos por correo por hora; pasado el tope se guarda sin avisar
_global: list[float] = []


def limitado(ip: str) -> bool:
    """Límite por IP. El puerto solo escucha en local y CF-Connecting-IP
    la pone Cloudflare en el túnel, así que no se puede falsificar desde fuera."""
    ahora = time.time()
    with _lock:
        if len(_vistos) > 5000:  # limpia IPs caducadas para no crecer sin fin
            for k in [k for k, v in _vistos.items() if not v or ahora - v[-1] >= VENTANA]:
                del _vistos[k]
        lista = [t for t in _vistos.get(ip, []) if ahora - t < VENTANA]
        if len(lista) >= LIMITE:
            _vistos[ip] = lista
            return True
        lista.append(ahora)
        _vistos[ip] = lista
        return False


def correo_permitido() -> bool:
    """Tope global solo para el correo: nadie puede bloquear las reservas de otros."""
    ahora = time.time()
    with _lock:
        _global[:] = [t for t in _global if ahora - t < VENTANA]
        if len(_global) >= LIMITE_GLOBAL:
            return False
        _global.append(ahora)
        return True


def avisar(r: dict) -> None:
    if not (SMTP_URL and RESERVAS_TO):
        return
    u = urlparse(SMTP_URL)
    usuario, clave = unquote(u.username or ""), unquote(u.password or "")
    remite = RESERVAS_FROM or usuario
    m = EmailMessage()
    tienda = r["tipo"] == "tienda"
    if tienda:
        m["Subject"] = f"Flechas amarillas · TIENDA: {r['comercio']} ({r['localidad'] or 'sin localidad'})"
    else:
        m["Subject"] = f"Flechas amarillas · reserva: {r['nombre']} ({r['cantidad']})"
    m["From"] = formataddr(("Flechas amarillas web", remite))
    m["To"] = RESERVAS_TO
    m["Reply-To"] = formataddr((r["nombre"], r["email"]))
    m.set_content(
        f"Nueva solicitud de «Lo que esconden las flechas amarillas» ({'librería o tienda' if tienda else 'lector'})\n\n"
        + (f"Comercio: {r['comercio']}\nTeléfono: {r['telefono'] or '-'}\n" if tienda else "")
        + f"Nombre: {r['nombre']}\nCorreo: {r['email']}\nEjemplares: {r['cantidad']}\n"
        f"Localidad: {r['localidad'] or '-'}\nIdioma de la web: {r['idioma']}\n"
        f"Fecha: {r['fecha']}\n\nMensaje:\n{r['mensaje'] or '-'}\n\n"
        "Responder a este correo contesta directamente a quien reservó.\n"
    )
    ctx = ssl.create_default_context()
    try:
        if u.scheme == "smtps":
            with smtplib.SMTP_SSL(u.hostname, u.port or 465, context=ctx, timeout=20) as s:
                s.login(usuario, clave)
                s.send_message(m)
        else:
            with smtplib.SMTP(u.hostname, u.port or 587, timeout=20) as s:
                s.starttls(context=ctx)
                s.login(usuario, clave)
                s.send_message(m)
    except Exception as ex:  # la reserva ya está guardada; solo se registra el fallo
        print(f"[aviso] no se pudo enviar el correo: {type(ex).__name__}: {ex}", flush=True)


class Handler(SimpleHTTPRequestHandler):
    server_version = "flechas"
    sys_version = ""

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(SITE), **kw)

    def log_message(self, fmt, *args):  # sin IPs en el registro
        print(f"{self.command} {self.path.split('?')[0]} {args[1] if len(args) > 1 else ''}", flush=True)

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
            "script-src 'self'; font-src 'self'; connect-src 'self'; form-action 'self'; "
            "frame-ancestors 'none'; base-uri 'self'",
        )
        p = self.path.split("?")[0]
        if p.startswith("/fonts/") or "?v=" in self.path:
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        elif p.startswith("/img/"):  # las imágenes pueden cambiar o retirarse: caché corta
            self.send_header("Cache-Control", "public, max-age=86400")
        elif p.endswith((".html", "/")):
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self):
        if self.path.split("?")[0] == "/salud":
            return self._json(200, {"ok": True})
        p = self.path.split("?")[0]
        if p.endswith("/") is False and (SITE / p.lstrip("/")).is_dir():
            self.send_response(301)
            self.send_header("Location", p + "/")
            self.end_headers()
            return
        return super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/api/reserva":
            return self._json(404, {"error": "no existe"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            n = 0
        if n <= 0 or n > 8000:
            return self._json(413, {"error": "tamaño"})
        try:
            d = json.loads(self.rfile.read(n).decode("utf-8"))
            assert isinstance(d, dict)
        except Exception:
            return self._json(400, {"error": "formato"})

        if (d.get("web") or "").strip():  # trampa para bots: se finge éxito
            return self._json(200, {"ok": True})

        ip = self.headers.get("CF-Connecting-IP") or self.client_address[0]
        if limitado(ip):
            return self._json(429, {"error": "demasiadas"})

        txt = lambda k, mx: re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", str(d.get(k) or "")).strip()[:mx]
        r = {
            "fecha": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            "nombre": txt("nombre", 120).replace("\n", " "),
            "email": txt("email", 160).replace("\n", ""),
            "localidad": txt("localidad", 120).replace("\n", " "),
            "mensaje": txt("mensaje", 1500),
            "idioma": "en" if d.get("idioma") == "en" else "es",
            "tipo": "tienda" if d.get("tipo") == "tienda" else "lector",
            "comercio": txt("comercio", 160).replace("\n", " "),
            "telefono": txt("telefono", 40).replace("\n", " "),
        }
        try:
            r["cantidad"] = max(1, min(500, int(d.get("cantidad") or 1)))
        except (TypeError, ValueError):
            r["cantidad"] = 1
        if not r["nombre"] or not EMAIL_RE.match(r["email"]) or d.get("privacidad") != "si":
            return self._json(422, {"error": "datos"})
        if r["tipo"] == "tienda" and not r["comercio"]:
            return self._json(422, {"error": "datos"})
        fichero = DATA / "reservas.jsonl"
        if fichero.exists() and fichero.stat().st_size > MAX_FICHERO:
            print("[aviso] reservas.jsonl supera el tope; solicitud rechazada", flush=True)
            return self._json(503, {"error": "lleno"})

        with _lock:
            with open(DATA / "reservas.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        if correo_permitido():
            threading.Thread(target=avisar, args=(r,), daemon=True).start()
        else:
            print("[aviso] tope de correos por hora alcanzado; reserva guardada sin aviso", flush=True)
        return self._json(200, {"ok": True})

    def _json(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)


Handler.extensions_map.update({".webp": "image/webp", ".woff2": "font/woff2", ".svg": "image/svg+xml", ".js": "text/javascript"})

if __name__ == "__main__":
    print(f"Sirviendo {SITE} en :{PORT} · aviso por correo {'activo' if SMTP_URL and RESERVAS_TO else 'desactivado'}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
