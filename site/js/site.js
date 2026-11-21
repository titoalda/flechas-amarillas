(() => {
  "use strict";
  document.body.classList.remove("sin-js");
  const D = JSON.parse(document.getElementById("datos").textContent).t;

  /* Cabecera con borde al bajar y botón fijo en móvil */
  const cab = document.querySelector(".cabecera");
  const barra = document.querySelector(".barra-movil");
  const contacto = document.getElementById("contacto");
  let enContacto = false, trasPortada = false;
  const pintaBarra = () => barra.classList.toggle("visible", trasPortada && !enContacto);
  new IntersectionObserver(([en]) => {
    trasPortada = !en.isIntersecting;
    cab.classList.toggle("con-borde", trasPortada);
    pintaBarra();
  }, { rootMargin: "-64px 0px 0px 0px" }).observe(document.querySelector(".portada"));
  new IntersectionObserver(([en]) => { enContacto = en.isIntersecting; pintaBarra(); }).observe(contacto);

  /* Menú hamburguesa */
  const mb = document.querySelector(".menu-boton"), menu = document.getElementById("menu");
  if (mb && menu) {
    const pon = (v) => { menu.classList.toggle("abierto", v); mb.setAttribute("aria-expanded", String(v)); };
    mb.addEventListener("click", () => pon(!menu.classList.contains("abierto")));
    menu.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => pon(false)));
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") pon(false); });
  }

  /* Aparición suave */
  const io = new IntersectionObserver((ents) => {
    ents.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("visto"); io.unobserve(en.target); } });
  }, { rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll(".aparece").forEach((el) => io.observe(el));

  /* Libro: sigue al ratón con un giro suave (muelle) */
  const libro = document.querySelector(".libro3d");
  if (libro && matchMedia("(hover:hover) and (prefers-reduced-motion:no-preference)").matches) {
    const base = { y: 22, x: 3, s: 1 };
    let tY = base.y, tX = base.x, tS = 1, cY = base.y, cX = base.x, cS = 1, raf = 0, dentro = false;
    const paso = () => {
      cY += (tY - cY) * 0.1; cX += (tX - cX) * 0.1; cS += (tS - cS) * 0.1;
      libro.style.transform = `rotateY(${cY.toFixed(2)}deg) rotateX(${cX.toFixed(2)}deg) scale(${cS.toFixed(3)})`;
      const quieto = Math.abs(tY - cY) < 0.01 && Math.abs(tX - cX) < 0.01 && Math.abs(tS - cS) < 0.001;
      raf = (!dentro && quieto) ? 0 : requestAnimationFrame(paso);
    };
    const caja = libro.parentElement;
    caja.addEventListener("mouseenter", () => { dentro = true; tS = 1.05; if (!raf) raf = requestAnimationFrame(paso); });
    caja.addEventListener("mousemove", (ev) => {
      const r = caja.getBoundingClientRect();
      const nx = (ev.clientX - r.left) / r.width * 2 - 1, ny = (ev.clientY - r.top) / r.height * 2 - 1;
      tY = base.y + nx * 12; tX = base.x - ny * 8;
    });
    caja.addEventListener("mouseleave", () => { dentro = false; tY = base.y; tX = base.x; tS = 1; if (!raf) raf = requestAnimationFrame(paso); });
  }

  /* Doble página: se amplía al pulsar */
  document.querySelectorAll(".ampliable").forEach((bt) => bt.addEventListener("click", () => {
    const z = document.createElement("div");
    z.className = "zoom"; z.setAttribute("role", "dialog"); z.setAttribute("aria-modal", "true");
    const im = bt.querySelector("img").cloneNode();
    im.removeAttribute("loading"); im.src = im.dataset.grande || im.src;
    z.appendChild(im); document.body.appendChild(z);
    requestAnimationFrame(() => requestAnimationFrame(() => z.classList.add("abierto")));
    const cierra = () => {
      z.classList.remove("abierto"); document.removeEventListener("keydown", tecla);
      setTimeout(() => { z.remove(); bt.focus(); }, 320);
    };
    const tecla = (ev) => { if (ev.key === "Escape") cierra(); };
    z.addEventListener("click", cierra); document.addEventListener("keydown", tecla);
  }));

  /* Formulario */
  const caja = document.getElementById("formulario");
  const form = caja.querySelector("form");
  const cant = form.querySelector("#f-cantidad");
  const btn = form.querySelector('button[type="submit"]');
  const btnTxt = btn.querySelector(".boton-texto");
  const err = form.querySelector(".formulario-error");
  const nombre = form.querySelector("#f-nombre");
  const email = form.querySelector("#f-email");
  const comercio = form.querySelector("#f-comercio");
  const priv = form.querySelector("#f-priv");
  const tipo = () => form.dataset.tipoActual;

  function ponTipo(t) {
    form.dataset.tipoActual = t;
    form.querySelector(`input[name="tipo"][value="${t}"]`).checked = true;
    btnTxt.textContent = t === "tienda" ? D.enviar_t : D.enviar_l;
    comercio.required = t === "tienda";
  }
  form.querySelectorAll('input[name="tipo"]').forEach((r) => r.addEventListener("change", () => ponTipo(r.value)));
  document.querySelectorAll("a[data-tipo]").forEach((a) => a.addEventListener("click", () => ponTipo(a.dataset.tipo)));
  if (location.hash === "#librerias") ponTipo("tienda");

  form.querySelectorAll("[data-paso]").forEach((b) => b.addEventListener("click", () => {
    cant.value = Math.min(500, Math.max(1, (parseInt(cant.value, 10) || 1) + parseInt(b.dataset.paso, 10)));
  }));

  const emailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim());
  const marca = (el, mal, id) => {
    el.setAttribute("aria-invalid", mal ? "true" : "false");
    if (mal) el.setAttribute("aria-describedby", id); else el.removeAttribute("aria-describedby");
  };
  const reglas = [
    [nombre, () => !nombre.value.trim(), "e-nombre"],
    [email, () => !emailOk(email.value), "e-email"],
    [comercio, () => tipo() === "tienda" && !comercio.value.trim(), "e-comercio"],
  ];
  reglas.forEach(([el, mal, id]) => {
    el.addEventListener("blur", () => { if (el.value) marca(el, mal(), id); });
    el.addEventListener("input", () => { if (el.getAttribute("aria-invalid") === "true") marca(el, mal(), id); });
  });
  const muestraError = (txt) => { err.textContent = txt; err.classList.toggle("visible", !!txt); };

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    muestraError("");
    let primero = null;
    reglas.forEach(([el, mal, id]) => { const m = mal(); marca(el, m, id); if (m && !primero) primero = el; });
    if (primero) { primero.focus(); return; }
    if (!priv.checked) { muestraError(D.err_priv); priv.focus(); return; }
    const datos = Object.fromEntries(new FormData(form));
    const txt = btnTxt.textContent;
    btn.setAttribute("aria-busy", "true"); btn.disabled = true; btnTxt.textContent = D.enviando;
    try {
      const r = await fetch("/api/reserva", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(datos) });
      if (r.status === 429) throw new Error("lim");
      if (!r.ok) throw new Error("red");
      caja.querySelector(".hecho-texto").textContent = (tipo() === "tienda" ? D.ok_t : D.ok_l).replace("{email}", email.value.trim());
      caja.classList.add("enviado");
      const h = caja.querySelector(".hecho");
      const f = h.querySelector(".hecho-flecha");
      f.style.animation = "none"; void f.offsetWidth; f.style.animation = "";
      h.focus();
    } catch (e) {
      muestraError(e.message === "lim" ? D.err_lim : D.err_red);
    } finally {
      btn.removeAttribute("aria-busy"); btn.disabled = false; btnTxt.textContent = txt;
    }
  });
  caja.querySelector(".hecho-otra").addEventListener("click", () => {
    const t = tipo(); form.reset(); ponTipo(t); caja.classList.remove("enviado"); nombre.focus();
  });
})();
