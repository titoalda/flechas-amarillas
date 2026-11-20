(() => {
  "use strict";
  document.body.classList.remove("sin-js");
  const D = JSON.parse(document.getElementById("datos").textContent);
  const items = D.items;
  const base = document.documentElement.lang === "es" ? "" : "../";
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Cabecera con borde al bajar y barra de reserva en móvil */
  const cab = document.querySelector(".cabecera");
  const barra = document.querySelector(".barra-movil");
  const portada = document.querySelector(".portada");
  const reserva = document.getElementById("reserva");
  let enReserva = false, trasPortada = false;
  const pintaBarra = () => barra.classList.toggle("visible", trasPortada && !enReserva);
  new IntersectionObserver(([en]) => {
    trasPortada = !en.isIntersecting;
    cab.classList.toggle("con-borde", trasPortada);
    pintaBarra();
  }, { rootMargin: "-64px 0px 0px 0px" }).observe(portada);
  new IntersectionObserver(([en]) => { enReserva = en.isIntersecting; pintaBarra(); }).observe(reserva);

  /* Aparición suave */
  const io = new IntersectionObserver((ents) => {
    ents.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("visto"); io.unobserve(en.target); } });
  }, { rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll(".aparece").forEach((el) => io.observe(el));

  /* Tira de lugares */
  const tira = document.querySelector(".tira");
  const atras = document.querySelector(".tira-controles .atras");
  const adelante = document.querySelector(".tira-controles .adelante");
  const paso = () => tira.clientWidth * 0.8;
  const estadoTira = () => {
    atras.disabled = tira.scrollLeft < 8;
    adelante.disabled = tira.scrollLeft + tira.clientWidth > tira.scrollWidth - 8;
  };
  atras.addEventListener("click", () => tira.scrollBy({ left: -paso(), behavior: reduce ? "auto" : "smooth" }));
  adelante.addEventListener("click", () => tira.scrollBy({ left: paso(), behavior: reduce ? "auto" : "smooth" }));
  tira.addEventListener("scroll", estadoTira, { passive: true });
  addEventListener("resize", estadoTira);
  estadoTira();

  /* Visor */
  const visor = document.querySelector(".visor");
  const vImg = visor.querySelector("figure img");
  const vCap = visor.querySelector("figcaption");
  const vAnt = visor.querySelector(".visor-ant");
  const vSig = visor.querySelector(".visor-sig");
  let modo = "lugar", lista = [], pos = 0, origen = null;
  const dobles = [...document.querySelectorAll("[data-doble]")].map((b) => ({ id: b.dataset.doble, titulo: b.dataset.titulo }));

  function pinta() {
    if (modo === "lugar") {
      const it = lista[pos];
      visor.classList.remove("es-doble");
      vImg.src = `${base}img/lugares/${it.id}.webp`;
      vImg.alt = it.pie;
      vImg.className = "acuarela";
      vCap.innerHTML = "";
      const b = document.createElement("b"); b.textContent = it.n;
      const s = document.createElement("span"); s.textContent = it.pie;
      const s2 = document.createElement("span"); s2.className = "en"; s2.textContent = it.pie2;
      vCap.append(b, s, s2);
    } else {
      const d = lista[pos];
      visor.classList.add("es-doble");
      vImg.src = `${base}img/paginas/${d.id}.webp`;
      vImg.alt = d.titulo;
      vImg.className = "";
      vCap.innerHTML = "";
      const s = document.createElement("span"); s.textContent = d.titulo;
      vCap.append(s);
    }
    // precarga la siguiente
    const sig = lista[(pos + 1) % lista.length];
    if (sig) new Image().src = modo === "lugar" ? `${base}img/lugares/${sig.id}.webp` : `${base}img/paginas/${sig.id}.webp`;
  }
  function abre(m, l, i, btn) {
    modo = m; lista = l; pos = i; origen = btn;
    pinta();
    visor.hidden = false;
    visor.classList.add("abierto");
    document.documentElement.style.overflow = "hidden";
    visor.querySelector(".visor-cerrar").focus();
  }
  function cierra() {
    visor.classList.remove("abierto");
    visor.hidden = true;
    document.documentElement.style.overflow = "";
    if (origen) origen.focus();
  }
  const mueve = (d) => { pos = (pos + d + lista.length) % lista.length; pinta(); };
  document.addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-abre]");
    if (b) { abre("lugar", items, Math.max(0, items.findIndex((x) => x.id === b.dataset.abre)), b); return; }
    const d = ev.target.closest("[data-doble]");
    if (d) abre("doble", dobles, dobles.findIndex((x) => x.id === d.dataset.doble), d);
  });
  visor.querySelector(".visor-cerrar").addEventListener("click", cierra);
  vAnt.addEventListener("click", () => mueve(-1));
  vSig.addEventListener("click", () => mueve(1));
  visor.addEventListener("click", (ev) => { if (ev.target === visor) cierra(); });
  document.addEventListener("keydown", (ev) => {
    if (visor.hidden) return;
    if (ev.key === "Escape") cierra();
    else if (ev.key === "ArrowLeft") mueve(-1);
    else if (ev.key === "ArrowRight") mueve(1);
    else if (ev.key === "Tab") {
      const f = [...visor.querySelectorAll("button")];
      const i = f.indexOf(document.activeElement);
      ev.preventDefault();
      f[(i + (ev.shiftKey ? -1 : 1) + f.length) % f.length].focus();
    }
  });
  let x0 = null;
  visor.addEventListener("touchstart", (ev) => { x0 = ev.touches[0].clientX; }, { passive: true });
  visor.addEventListener("touchend", (ev) => {
    if (x0 === null) return;
    const dx = ev.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) mueve(dx < 0 ? 1 : -1);
    x0 = null;
  });

  /* Formulario */
  const caja = document.getElementById("formulario");
  const form = caja.querySelector("form");
  const cant = form.querySelector("#f-cantidad");
  const btn = form.querySelector('button[type="submit"]');
  const err = form.querySelector(".formulario-error");
  form.querySelectorAll("[data-paso]").forEach((b) => b.addEventListener("click", () => {
    const v = Math.min(50, Math.max(1, (parseInt(cant.value, 10) || 1) + parseInt(b.dataset.paso, 10)));
    cant.value = v;
  }));
  const nombre = form.querySelector("#f-nombre");
  const email = form.querySelector("#f-email");
  const priv = form.querySelector("#f-priv");
  const emailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim());
  const marca = (el, mal, id) => {
    el.setAttribute("aria-invalid", mal ? "true" : "false");
    if (mal) el.setAttribute("aria-describedby", id); else el.removeAttribute("aria-describedby");
  };
  nombre.addEventListener("blur", () => { if (nombre.value) marca(nombre, !nombre.value.trim(), "e-nombre"); });
  email.addEventListener("blur", () => { if (email.value) marca(email, !emailOk(email.value), "e-email"); });
  [nombre, email].forEach((el) => el.addEventListener("input", () => { if (el.getAttribute("aria-invalid") === "true") marca(el, el === email ? !emailOk(el.value) : !el.value.trim(), el === email ? "e-email" : "e-nombre"); }));

  const muestraError = (txt) => { err.textContent = txt; err.classList.toggle("visible", !!txt); };

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    muestraError("");
    const mN = !nombre.value.trim(), mE = !emailOk(email.value);
    marca(nombre, mN, "e-nombre"); marca(email, mE, "e-email");
    if (mN || mE) { (mN ? nombre : email).focus(); return; }
    if (!priv.checked) { muestraError(D.t.err_priv); priv.focus(); return; }
    const datos = Object.fromEntries(new FormData(form));
    btn.setAttribute("aria-busy", "true"); btn.disabled = true;
    const txt = btn.firstChild.textContent; btn.firstChild.textContent = D.t.enviando + " ";
    try {
      const r = await fetch("/api/reserva", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(datos) });
      if (r.status === 429) throw new Error("lim");
      if (!r.ok) throw new Error("red");
      caja.querySelector(".hecho-texto").textContent = D.t.ok.replace("{email}", email.value.trim());
      caja.classList.add("enviado");
      const h = caja.querySelector(".hecho");
      const flecha = h.querySelector(".hecho-flecha");
      flecha.style.animation = "none"; void flecha.offsetWidth; flecha.style.animation = "";
      h.focus();
    } catch (e) {
      muestraError(e.message === "lim" ? D.t.err_lim : D.t.err_red);
    } finally {
      btn.removeAttribute("aria-busy"); btn.disabled = false; btn.firstChild.textContent = txt;
    }
  });
  caja.querySelector(".hecho-otra").addEventListener("click", () => {
    form.reset(); caja.classList.remove("enviado"); nombre.focus();
  });
})();
