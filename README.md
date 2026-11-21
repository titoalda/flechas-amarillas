# Lo que esconden las flechas amarillas · web

Web de venta (reserva) del libro de Aldara Álvarez González.

- `build.py` genera `docs/index.html` (ES) y `docs/en/index.html` (EN) desde los textos que contiene. Tras cambiar un texto o el CSS/JS: `python build.py`.
- `server.py` sirve `docs/` y recibe las reservas en `POST /api/reserva`; las guarda en `data/reservas.jsonl` y avisa por correo si hay `SMTP_URL` y `RESERVAS_TO` (ver `.env.example`).
- `docker compose up -d` lo levanta en el puerto 8622.
- Imágenes sacadas del PDF del libro (versión Digital del 15-nov-2026) a 250 ppp.
- `INDEXAR = False` en `build.py` mientras viva en un subdominio provisional.
