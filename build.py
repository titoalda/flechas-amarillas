#!/usr/bin/env python3
"""Genera site/index.html (ES) y site/en/index.html (EN) desde una sola plantilla.

Uso: python build.py
Los textos están aquí abajo; las imágenes en site/img. Si cambia un texto,
cámbialo en los dos idiomas y vuelve a ejecutar.
"""
from html import escape
from pathlib import Path
import json

RAIZ = Path(__file__).parent / "site"
URL = "https://flechasamarillas.titoteca.net"
INDEXAR = False  # en el subdominio provisional no se indexa; True con el dominio propio

# Lugares en el orden del libro: (id, nombre, acto, pie ES, pie EN, tipo)
LUGARES = [
    ("porto", "Porto", 1, "Fachada románica de la Sé do Porto", "The Romanesque facade of Porto Cathedral"),
    ("matosinhos", "Matosinhos", 1, "El Castelo do Queijo, sobre las rocas", "Castelo do Queijo, on the rocks"),
    ("vila-do-conde", "Vila do Conde", 1, "El acueducto de Santa Clara", "The Santa Clara aqueduct"),
    ("gastronomia", None, 1, "Sardinas asadas, broa y vinho verde", "Grilled sardines, broa and vinho verde"),
    ("esposende", "Esposende", 1, "El fuerte de São João Baptista, en la desembocadura del Cávado", "The São João Baptista fort, at the Cávado’s mouth"),
    ("viana-do-castelo", "Viana do Castelo", 1, "El corazón de filigrana de Viana", "The Viana filigree heart"),
    ("ancora", "Âncora", 1, "Dunas y pinar entre Âncora y Moledo", "Dunes and pines between Âncora and Moledo"),
    ("moledo", "Moledo", 1, "El Forte da Ínsua, frente a la playa", "Forte da Ínsua, off the beach"),
    ("caminha", "Caminha", 1, "La lancha que cruza el Miño hacia A Guarda", "The boat crossing the Minho to A Guarda"),
    ("clima", None, 2, "Niebla matinal sobre la costa gallega", "Morning fog over the Galician coast"),
    ("a-guarda", "A Guarda", 2, "Cabañas circulares del castro de Santa Trega", "Circular huts of the Santa Trega hillfort"),
    ("oia", "Oia", 2, "El monasterio de Oia, a pie de ola", "Oia monastery, at the water’s edge"),
    ("baiona", "Baiona", 2, "La réplica de la carabela Pinta", "The replica of the caravel Pinta"),
    ("nigran", "Nigrán", 2, "El puente medieval de A Ramallosa", "The medieval bridge of A Ramallosa"),
    ("vigo", "Vigo", 2, "El puerto pesquero de Vigo al amanecer", "Vigo’s fishing port at dawn"),
    ("redondela", "Redondela", 2, "Uno de los viaductos de hierro", "One of the iron viaducts"),
    ("arcade", "Arcade", 2, "Bateas de ostras en el fondo de la ría de Vigo", "Oyster rafts at the head of the Ría de Vigo"),
    ("naturaleza", None, 2, "Percebes en las rocas batidas por el oleaje", "Goose barnacles on wave-battered rocks"),
    ("pontevedra", "Pontevedra", 3, "La fachada curva de A Peregrina", "The curved facade of A Peregrina"),
    ("combarro", "Combarro", 3, "Hórreos de piedra sobre las rocas", "Stone granaries over the rocks"),
    ("arquitectura", None, 3, "Un cruceiro en una encrucijada gallega", "A cruceiro at a Galician crossroads"),
    ("barro", "Barro", 3, "La cascada y los molinos del Barosa", "The waterfall and mills of the Barosa"),
    ("caldas-de-reis", "Caldas de Reis", 3, "La fervenza termal de Caldas de Reis", "The thermal waterfall of Caldas de Reis"),
    ("valga", "Valga", 3, "Marismas del estuario del Ulla", "Marshes of the Ulla estuary"),
    ("pontecesures", "Pontecesures", 3, "El puente sobre el Ulla", "The bridge over the Ulla"),
    ("padron", "Padrón", 4, "Pimientos de Padrón recién recogidos", "Freshly picked Padrón peppers"),
    ("a-escravitude", "A Escravitude", 4, "La escalinata del santuario", "The sanctuary’s staircase"),
    ("milladoiro", "Milladoiro", 4, "El monumento de piedras apiladas", "The stacked-stone monument"),
    ("santiago", "Santiago de Compostela", 4, "La Praza do Obradoiro, frente a la catedral", "Praza do Obradoiro, facing the cathedral"),
    ("fisterra", None, 5, "El faro de Fisterra", "The Fisterra lighthouse"),
]
TEMAS = {
    "gastronomia": ("Gastronomía", "Food"),
    "clima": ("Clima", "Weather"),
    "naturaleza": ("Naturaleza", "Nature"),
    "arquitectura": ("Arquitectura", "Architecture"),
    "fisterra": ("Fisterra", "Fisterra"),
}
ACTOS = {
    1: ("Oporto y el Miño", "Porto and the Minho"),
    2: ("Tierras gallegas", "Galician lands"),
    3: ("Las Rías Baixas", "The Rías Baixas"),
    4: ("Los últimos kilómetros", "The final kilometres"),
}
DOBLES = [
    ("vila-do-conde", "Vila do Conde", "Vila do Conde"),
    ("gastronomia", "Gastronomía, una de las cuatro fichas temáticas", "Food, one of the four theme pages"),
    ("baiona", "Baiona, el pueblo de la autora", "Baiona, the author’s hometown"),
    ("fisterra", "Epílogo, un poco más allá", "Epilogue, a little further"),
]

T = {
    "es": dict(
        lang="es", raiz="", otro="/en/", otro_txt="English", otro_lang="en", otro_aria="Read in English",
        title="Lo que esconden las flechas amarillas · Camino Portugués por la Costa",
        desc="Libro de bolsillo ilustrado en acuarela por Aldara Álvarez González. 25 lugares del Camino Portugués por la Costa, de Oporto a Santiago, en español y en inglés. Reserva tu ejemplar.",
        saltar="Saltar al contenido",
        marca="Lo que esconden las flechas amarillas", marca_corta="Las flechas amarillas",
        nav=[("#libro", "El libro"), ("#camino", "El camino"), ("#lugares", "Lugares"), ("#autora", "La autora")],
        reservar="Reservar",
        ante="Camino Portugués por la Costa · De Oporto a Santiago",
        h1="Lo que esconden las flechas amarillas",
        h1_en="Behind the Yellow Arrows",
        lema="Detrás de cada flecha amarilla hay algo que nadie te cuenta.",
        lema_en="Behind every yellow arrow there is something nobody tells you.",
        resumen="Un libro de bolsillo con 25 lugares del camino, ilustrados en acuarela y contados en español y en inglés. Para leer cuando pares a descansar los pies.",
        cta="Reserva tu ejemplar", cta2="Ver los lugares",
        estado="<strong>En imprenta pronto.</strong> Reserva sin compromiso y te avisamos con el precio.",
        portada_alt="Cubierta del libro con un mojón de piedra, una vieira y una flecha amarilla junto al mar",
        libro_ante="El libro",
        libro_h="Este libro",
        libro_txt=[
            "Este libro no es una guía práctica: no da distancias ni albergues. Reúne 25 lugares del Camino Portugués por la Costa, de Oporto a Santiago, y cuenta algo pequeño de cada uno: una piedra, una leyenda, un plato.",
            "Algunas historias vienen de hace siglos y otras de lo que pasa hoy en una plaza o en un puerto, pero todas están a pocos pasos del camino.",
        ],
        libro_cita="Hay una flecha amarilla en cada ilustración. ¿Las encuentras todas?",
        libro_cita_en="There is a yellow arrow in every illustration. Can you find them all?",
        libro_img_alt="Flecha amarilla pintada sobre un muro de piedra",
        ficha=[("84", "páginas a color"), ("25", "lugares, de Oporto a Santiago"), ("4", "fichas de gastronomía, clima, naturaleza y arquitectura"), ("A6", "de bolsillo, 105 × 148 mm"), ("ES · EN", "cada texto en español y en inglés"), ("1", "flecha escondida en cada ilustración")],
        camino_ante="El camino, página a página",
        camino_h="Cuatro actos, de Oporto a Santiago",
        camino_txt="El libro sigue el Camino Portugués por la Costa en el orden en que se camina. Toca un lugar para ver su ilustración.",
        mapa_alt="Mapa en acuarela de la costa de Portugal y Galicia con los cuatro actos del camino",
        acto="Acto", temas="Temas", epilogo="Epílogo", epilogo_txt="Fisterra, un poco más allá",
        lugares_ante="Lugares",
        lugares_h="Una acuarela por parada",
        lugares_txt="Cada lugar ocupa una doble página: a la izquierda su ilustración y a la derecha su historia.",
        anterior="Anterior", siguiente="Siguiente", pista="Desliza para ver más",
        tema="Tema", epi="Epílogo",
        dentro_ante="Por dentro",
        dentro_h="Así se ve abierto",
        dentro_txt="Texto en español y, debajo, en inglés. Léelo en orden o ábrelo por donde quieras: como en el camino, cada parada se sostiene sola.",
        autora_ante="La autora",
        autora_nombre="Aldara Álvarez González",
        autora_txt="Diseñadora e ilustradora de Baiona. Ha escrito, ilustrado y maquetado el libro entero.",
        autora_cita="Este libro nació de una idea sencilla: contar, entre Oporto y Santiago, todo lo que una flecha amarilla señala pero nunca explica.",
        autora_cita_en="This book began with a simple idea: to tell, between Porto and Santiago, everything a yellow arrow points to but never explains.",
        autora_web="Ver su trabajo",
        autora_img_alt="La sombra de un peregrino sobre un camino de tierra ocre, con una flecha amarilla",
        res_ante="Reserva",
        res_h="Reserva tu ejemplar",
        res_txt="El libro está a punto de ir a imprenta y aún no tiene precio cerrado. Reservar no te compromete a nada.",
        pasos=["Nos dejas tu nombre, tu correo y cuántos ejemplares quieres.", "Cuando esté impreso te escribimos con el precio y las formas de pago y envío.", "Decides entonces si lo confirmas."],
        f_nombre="Nombre", f_email="Correo electrónico", f_cantidad="Ejemplares", f_menos="Uno menos", f_mas="Uno más",
        f_localidad="Localidad", f_opcional="(opcional)", f_mensaje="¿Algo que quieras contarnos?",
        f_privacidad='He leído la <a href="{raiz}/privacidad.html">política de privacidad</a> y acepto que se usen mis datos solo para gestionar esta reserva.',
        f_enviar="Reservar sin compromiso", f_enviando="Enviando…",
        f_aviso="Solo te escribiremos sobre este libro.",
        f_err_nombre="Escribe tu nombre.", f_err_email="Revisa el correo, parece incompleto.",
        f_err_priv="Necesitamos que aceptes la política de privacidad.",
        f_err_red="No se ha podido enviar. Prueba de nuevo en un momento.",
        f_err_lim="Has enviado varias reservas seguidas. Prueba de nuevo dentro de un rato.",
        ok_h="Reserva recibida",
        ok_txt="Gracias. Te escribiremos a {email} cuando el libro esté impreso. Buen camino.",
        ok_otra="Hacer otra reserva",
        pie_final="Aquí se acaban las flechas de esta página. Lo que viene lo escribes tú.",
        pie_copy="© 2026 Aldara Álvarez González. Textos e ilustraciones originales.",
        privacidad="Privacidad",
        visor_cerrar="Cerrar", visor_dialogo="Ilustración ampliada",
    ),
    "en": dict(
        lang="en", raiz="/en", otro="/", otro_txt="Español", otro_lang="es", otro_aria="Leer en español",
        title="Behind the Yellow Arrows · Portuguese Coastal Way",
        desc="A pocket book illustrated in watercolour by Aldara Álvarez González. 25 places on the Portuguese Coastal Way, from Porto to Santiago, in Spanish and English. Reserve your copy.",
        saltar="Skip to content",
        marca="Behind the Yellow Arrows", marca_corta="The Yellow Arrows",
        nav=[("#libro", "The book"), ("#camino", "The Way"), ("#lugares", "Places"), ("#autora", "The author")],
        reservar="Reserve",
        ante="Portuguese Coastal Way · From Porto to Santiago",
        h1="Behind the Yellow Arrows",
        h1_en="Lo que esconden las flechas amarillas",
        lema="Behind every yellow arrow there is something nobody tells you.",
        lema_en="Detrás de cada flecha amarilla hay algo que nadie te cuenta.",
        resumen="A pocket book with 25 places on the Way, painted in watercolour and told in Spanish and English. For reading when you stop to rest your feet.",
        cta="Reserve your copy", cta2="See the places",
        estado="<strong>Going to print soon.</strong> Reserve with no commitment and we will tell you the price.",
        portada_alt="Book cover with a stone waymarker, a scallop shell and a yellow arrow by the sea",
        libro_ante="The book",
        libro_h="This book",
        libro_txt=[
            "This book is not a practical guide. It gives no distances and no hostels. It collects 25 places along the Portuguese Coastal Way, from Porto to Santiago, and tells one small thing about each: a stone, a legend, a dish.",
            "Some stories are centuries old. Others are about what happens today in a square or a harbour. All of them are a few steps from the Way.",
        ],
        libro_cita="There is a yellow arrow in every illustration. Can you find them all?",
        libro_cita_en="Hay una flecha amarilla en cada ilustración. ¿Las encuentras todas?",
        libro_img_alt="A yellow arrow painted on a stone wall",
        ficha=[("84", "pages in colour"), ("25", "places, from Porto to Santiago"), ("4", "theme pages on food, weather, nature and architecture"), ("A6", "pocket size, 105 × 148 mm"), ("ES · EN", "every text in Spanish and English"), ("1", "hidden arrow in every illustration")],
        camino_ante="The Way, page by page",
        camino_h="Four acts, from Porto to Santiago",
        camino_txt="The book follows the Portuguese Coastal Way in the order you walk it. Tap a place to see its illustration.",
        mapa_alt="Watercolour map of the coast of Portugal and Galicia with the four acts of the Way",
        acto="Act", temas="Themes", epilogo="Epilogue", epilogo_txt="Fisterra, a little further",
        lugares_ante="Places",
        lugares_h="One watercolour for each stop",
        lugares_txt="Each place has a double page: the illustration on the left and its story on the right.",
        anterior="Previous", siguiente="Next", pista="Swipe to see more",
        tema="Theme", epi="Epilogue",
        dentro_ante="Inside",
        dentro_h="What it looks like open",
        dentro_txt="Text in Spanish with English below. Read it in order or open it anywhere: as on the Camino, every stop stands on its own.",
        autora_ante="The author",
        autora_nombre="Aldara Álvarez González",
        autora_txt="Designer and illustrator from Baiona, Galicia. She wrote, illustrated and designed the whole book.",
        autora_cita="This book began with a simple idea: to tell, between Porto and Santiago, everything a yellow arrow points to but never explains.",
        autora_cita_en="Este libro nació de una idea sencilla: contar, entre Oporto y Santiago, todo lo que una flecha amarilla señala pero nunca explica.",
        autora_web="See her work",
        autora_img_alt="A pilgrim’s shadow on an ochre dirt path, with a yellow arrow",
        res_ante="Reserve",
        res_h="Reserve your copy",
        res_txt="The book is about to go to print and the price is not set yet. Reserving does not commit you to anything.",
        pasos=["Leave your name, your email and how many copies you want.", "When it is printed, we will write to you with the price and the payment and shipping options.", "Then you decide whether to confirm."],
        f_nombre="Name", f_email="Email", f_cantidad="Copies", f_menos="One less", f_mas="One more",
        f_localidad="Town or city", f_opcional="(optional)", f_mensaje="Anything you want to tell us?",
        f_privacidad='I have read the <a href="{raiz}/privacidad.html">privacy policy</a> and agree to my data being used only to handle this reservation.',
        f_enviar="Reserve, no commitment", f_enviando="Sending…",
        f_aviso="We will only write to you about this book.",
        f_err_nombre="Please write your name.", f_err_email="Please check your email, it looks incomplete.",
        f_err_priv="Please accept the privacy policy.",
        f_err_red="It could not be sent. Please try again in a moment.",
        f_err_lim="You have sent several reservations in a row. Please try again later.",
        ok_h="Reservation received",
        ok_txt="Thank you. We will write to {email} when the book is printed. Buen camino.",
        ok_otra="Make another reservation",
        pie_final="Here the arrows of this page end. What comes next, you write.",
        pie_copy="© 2026 Aldara Álvarez González. Original text and illustrations.",
        privacidad="Privacy",
        visor_cerrar="Close", visor_dialogo="Enlarged illustration",
    ),
}


def e(s):
    return escape(s, quote=True)


def nombre(lid, n, lang):
    if n:
        return n
    return TEMAS[lid][0 if lang == "es" else 1]


def pagina(t):
    L = t["lang"]
    es = L == "es"
    R = t["raiz"]
    pref = "" if es else "../"
    # Datos para el visor (JS)
    items = []
    num = 0
    for lid, n, acto, pes, pen in LUGARES:
        if n:
            num += 1
        etiqueta = (f"{num:02d}" if n else (t["epi"] if acto == 5 else t["tema"]))
        items.append(dict(id=lid, n=nombre(lid, n, L), et=etiqueta,
                          pie=pes if es else pen, pie2=pen if es else pes))
    datos = json.dumps(dict(items=items, t=dict(
        enviando=t["f_enviando"], enviar=t["f_enviar"], err_nombre=t["f_err_nombre"],
        err_email=t["f_err_email"], err_priv=t["f_err_priv"], err_red=t["f_err_red"],
        err_lim=t["f_err_lim"], ok=t["ok_txt"])), ensure_ascii=False)

    nav = "".join(f'<a href="{h}" class="nav-secundario">{e(x)}</a>' for h, x in t["nav"])

    # Actos
    actos_html = ""
    for a in (1, 2, 3, 4):
        lis = "".join(
            f'<li><button type="button" data-abre="{lid}">{e(n)}</button></li>'
            for lid, n, ac, *_ in LUGARES if ac == a and n)
        actos_html += (f'<div class="acto"><h3>{e(t["acto"])} {"I" * a if a < 4 else "IV"}</h3>'
                       f'<h4>{e(ACTOS[a][0 if es else 1])}</h4><ol>{lis}</ol></div>')
    temas_btn = " · ".join(
        f'<button type="button" class="enlace-tema" data-abre="{k}">{e(TEMAS[k][0 if es else 1])}</button>'
        for k in ("gastronomia", "clima", "naturaleza", "arquitectura"))
    actos_html += (f'<div class="acto-extra"><span><strong>{e(t["temas"])}</strong> {temas_btn}</span>'
                   f'<span><strong>{e(t["epilogo"])}</strong> <button type="button" class="enlace-tema" data-abre="fisterra">{e(t["epilogo_txt"])}</button></span></div>')

    # Tira de lugares
    tira = ""
    for it in items:
        tira += (f'<li><button type="button" class="tarjeta" data-abre="{it["id"]}">'
                 f'<span class="tarjeta-img"><img class="acuarela" src="{pref}img/lugares/{it["id"]}-480.webp" '
                 f'alt="{e(it["pie"])}" loading="lazy" decoding="async"></span>'
                 f'<span class="tarjeta-num">{e(it["et"])}</span>'
                 f'<span class="tarjeta-nombre">{e(it["n"])}</span>'
                 f'<span class="tarjeta-pie">{e(it["pie"])}</span></button></li>')

    dobles = ""
    for did, des, den in DOBLES:
        cap = des if es else den
        dobles += (f'<figure class="aparece"><button type="button" class="doble" data-doble="{did}" data-titulo="{e(cap)}">'
                   f'<img src="{pref}img/paginas/{did}-900.webp" srcset="{pref}img/paginas/{did}-900.webp 900w, {pref}img/paginas/{did}.webp 1800w" '
                   f'sizes="(max-width:700px) 100vw, 50vw" alt="{e(cap)}" loading="lazy" decoding="async" width="900" height="634"></button>'
                   f'<figcaption>{e(cap)}</figcaption></figure>')

    ficha = "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in t["ficha"])
    pasos = "".join(f"<li><span>{e(p)}</span></li>" for p in t["pasos"])
    libro_txt = "".join(f"<p>{e(p)}</p>" for p in t["libro_txt"])
    robots = "index,follow" if INDEXAR else "noindex,follow"
    canon = URL + ("/" if es else "/en/")
    flecha = f"{pref}img/flecha.png"

    return f"""<!doctype html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="es" href="{URL}/">
<link rel="alternate" hreflang="en" href="{URL}/en/">
<link rel="alternate" hreflang="x-default" href="{URL}/">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="book">
<meta property="og:title" content="{e(t["h1"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:image" content="{URL}/img/og.jpg">
<meta property="og:url" content="{canon}">
<meta property="og:locale" content="{'es_ES' if es else 'en_GB'}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pref}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{pref}fonts/poiret-one-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{pref}fonts/lato-latin-300-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pref}css/site.css?v=__V__">
<script type="application/ld+json">{json.dumps({
    "@context": "https://schema.org", "@type": "Book",
    "name": "Lo que esconden las flechas amarillas", "alternateName": "Behind the Yellow Arrows",
    "author": {"@type": "Person", "name": "Aldara Álvarez González", "url": "https://aldaraalvarez.es"},
    "illustrator": {"@type": "Person", "name": "Aldara Álvarez González"},
    "inLanguage": ["es", "en"], "numberOfPages": 84, "bookFormat": "https://schema.org/Paperback",
    "about": "Camino Portugués por la Costa", "image": URL + "/img/portada.webp",
    "description": t["desc"]}, ensure_ascii=False)}</script>
</head>
<body class="sin-js">
<a class="salto" href="#contenido">{e(t["saltar"])}</a>
<header class="cabecera">
  <div class="envoltura">
    <a class="marca" href="{R}/"><img src="{flecha}" alt="" width="30" height="14"><span class="marca-larga">{e(t["marca"])}</span><span class="marca-corta">{e(t["marca_corta"])}</span></a>
    <nav class="nav" aria-label="{'Principal' if es else 'Main'}">
      {nav}
      <a class="idioma" href="{t["otro"]}" hreflang="{t["otro_lang"]}" lang="{t["otro_lang"]}" aria-label="{e(t["otro_aria"])}">{e(t["otro_txt"])}</a>
      <a class="boton boton-principal" href="#reserva">{e(t["reservar"])}</a>
    </nav>
  </div>
</header>

<main id="contenido">
<section class="portada">
  <div class="envoltura">
    <div class="portada-texto">
      <p class="antetitulo">{e(t["ante"])}</p>
      <h1 class="titulo titulo-xl">{e(t["h1"])}</h1>
      <p class="en-titulo" lang="{t["otro_lang"]}">{e(t["h1_en"])}</p>
      <p class="lema">{e(t["lema"])}</p>
      <p class="lema-en en" lang="{t["otro_lang"]}">{e(t["lema_en"])}</p>
      <p class="portada-resumen">{e(t["resumen"])}</p>
      <div class="acciones">
        <a class="boton boton-principal" href="#reserva">{e(t["cta"])} <img class="boton-flecha" src="{flecha}" alt="" width="26" height="12"></a>
        <a class="boton boton-secundario" href="#lugares">{e(t["cta2"])}</a>
      </div>
      <p class="estado">{t["estado"]}</p>
    </div>
    <div class="libro">
      <div class="libro-cubierta"><img src="{pref}img/portada-520.webp" srcset="{pref}img/portada-520.webp 520w, {pref}img/portada.webp 900w" sizes="(max-width:820px) 74vw, 420px" alt="{e(t["portada_alt"])}" width="520" height="735" fetchpriority="high"></div>
      <div class="libro-sombra"></div>
      <img class="flecha-portada" src="{flecha}" alt="" width="150" height="68">
    </div>
  </div>
</section>

<section class="seccion seccion-calida" id="libro">
  <div class="envoltura libro-explicado">
    <figure class="aparece"><img class="acuarela" src="{pref}img/lugares/flecha-amarilla.webp" alt="{e(t["libro_img_alt"])}" loading="lazy" width="811" height="1062"></figure>
    <div class="aparece">
      <p class="antetitulo">{e(t["libro_ante"])}</p>
      <h2 class="titulo titulo-l">{e(t["libro_h"])}</h2>
      <div style="margin-top:1.2rem">{libro_txt}</div>
      <div class="cita-libro"><p>{e(t["libro_cita"])}</p><p class="en" lang="{t["otro_lang"]}">{e(t["libro_cita_en"])}</p></div>
      <ul class="ficha">{ficha}</ul>
    </div>
  </div>
</section>

<section class="seccion" id="camino">
  <div class="envoltura camino">
    <figure class="mapa aparece"><img class="acuarela" src="{pref}img/lugares/mapa.webp" alt="{e(t["mapa_alt"])}" loading="lazy" width="864" height="1196"></figure>
    <div>
      <div class="cabeza-seccion aparece">
        <p class="antetitulo">{e(t["camino_ante"])}</p>
        <h2 class="titulo titulo-l">{e(t["camino_h"])}</h2>
        <p>{e(t["camino_txt"])}</p>
      </div>
      <div class="actos aparece">{actos_html}</div>
    </div>
  </div>
</section>

<section class="seccion seccion-calida" id="lugares">
  <div class="envoltura">
    <div class="tira-cabeza">
      <div class="cabeza-seccion aparece" style="margin-bottom:0">
        <p class="antetitulo">{e(t["lugares_ante"])}</p>
        <h2 class="titulo titulo-l">{e(t["lugares_h"])}</h2>
        <p>{e(t["lugares_txt"])}</p>
      </div>
      <div class="tira-controles">
        <button type="button" class="atras" aria-label="{e(t["anterior"])}"><img src="{flecha}" alt=""></button>
        <button type="button" class="adelante" aria-label="{e(t["siguiente"])}"><img src="{flecha}" alt=""></button>
      </div>
    </div>
  </div>
  <ul class="tira" tabindex="0" aria-label="{e(t["lugares_h"])}" style="margin-top:clamp(24px,4vw,40px)">{tira}</ul>
  <div class="envoltura"><p class="tira-pista">{e(t["pista"])}</p></div>
</section>

<section class="seccion" id="dentro">
  <div class="envoltura">
    <div class="cabeza-seccion aparece">
      <p class="antetitulo">{e(t["dentro_ante"])}</p>
      <h2 class="titulo titulo-l">{e(t["dentro_h"])}</h2>
      <p>{e(t["dentro_txt"])}</p>
    </div>
    <div class="dobles">{dobles}</div>
  </div>
</section>

<section class="seccion seccion-calida" id="autora">
  <div class="envoltura autora">
    <div class="aparece">
      <p class="antetitulo">{e(t["autora_ante"])}</p>
      <blockquote><p style="margin:0">«{e(t["autora_cita"])}»</p><span class="en" lang="{t["otro_lang"]}">{e(t["autora_cita_en"])}</span></blockquote>
      <div style="margin-top:2rem">
        <p class="autora-nombre">{e(t["autora_nombre"])}</p>
        <p>{e(t["autora_txt"])}</p>
        <a class="boton boton-secundario" href="https://aldaraalvarez.es{'' if es else '/en/'}" rel="noopener">{e(t["autora_web"])} <span aria-hidden="true">↗</span></a>
      </div>
    </div>
    <figure class="aparece"><img class="acuarela" src="{pref}img/lugares/acto4.webp" alt="{e(t["autora_img_alt"])}" loading="lazy" width="1000" height="1316"></figure>
  </div>
</section>

<section class="seccion" id="reserva">
  <div class="envoltura reserva">
    <div class="aparece">
      <p class="antetitulo">{e(t["res_ante"])}</p>
      <h2 class="titulo titulo-l">{e(t["res_h"])}</h2>
      <p style="margin-top:1rem">{e(t["res_txt"])}</p>
      <ol class="reserva-pasos">{pasos}</ol>
    </div>
    <div class="formulario aparece" id="formulario">
      <form novalidate action="/api/reserva" method="post">
        <input type="hidden" name="idioma" value="{L}">
        <div class="trampa" aria-hidden="true"><label>Web <input type="text" name="web" tabindex="-1" autocomplete="off"></label></div>
        <div class="campo"><label for="f-nombre">{e(t["f_nombre"])}</label><input id="f-nombre" name="nombre" autocomplete="name" required maxlength="120"><p class="campo-error" id="e-nombre">{e(t["f_err_nombre"])}</p></div>
        <div class="campo"><label for="f-email">{e(t["f_email"])}</label><input id="f-email" name="email" type="email" inputmode="email" autocomplete="email" required maxlength="160" spellcheck="false"><p class="campo-error" id="e-email">{e(t["f_err_email"])}</p></div>
        <div class="fila">
          <div class="campo"><label for="f-cantidad">{e(t["f_cantidad"])}</label>
            <div class="contador"><button type="button" data-paso="-1" aria-label="{e(t["f_menos"])}">−</button><input id="f-cantidad" name="cantidad" type="number" inputmode="numeric" min="1" max="50" value="1"><button type="button" data-paso="1" aria-label="{e(t["f_mas"])}">+</button></div>
          </div>
          <div class="campo"><label for="f-localidad">{e(t["f_localidad"])} <span class="opcional">{e(t["f_opcional"])}</span></label><input id="f-localidad" name="localidad" autocomplete="address-level2" maxlength="120"></div>
        </div>
        <div class="campo"><label for="f-mensaje">{e(t["f_mensaje"])} <span class="opcional">{e(t["f_opcional"])}</span></label><textarea id="f-mensaje" name="mensaje" maxlength="1500" rows="3"></textarea></div>
        <label class="consentimiento"><input type="checkbox" name="privacidad" value="si" required id="f-priv"><span>{t["f_privacidad"].format(raiz=R)}</span></label>
        <button class="boton boton-principal" type="submit">{e(t["f_enviar"])} <img class="boton-flecha" src="{flecha}" alt="" width="26" height="12"></button>
        <p class="formulario-error" role="alert"></p>
        <p class="formulario-aviso">{e(t["f_aviso"])}</p>
      </form>
      <div class="hecho" role="status" tabindex="-1">
        <img class="hecho-flecha" src="{flecha}" alt="" width="150" height="68">
        <h3 class="titulo titulo-m">{e(t["ok_h"])}</h3>
        <p class="hecho-texto"></p>
        <button type="button" class="boton boton-secundario hecho-otra">{e(t["ok_otra"])}</button>
      </div>
    </div>
  </div>
</section>
</main>

<footer class="pie">
  <div class="envoltura">
    <p class="pie-final" style="margin:0">{e(t["pie_final"])}</p>
    <p style="margin:0">{e(t["pie_copy"])} · <a href="{R}/privacidad.html">{e(t["privacidad"])}</a> · <a href="{t["otro"]}" hreflang="{t["otro_lang"]}" lang="{t["otro_lang"]}">{e(t["otro_txt"])}</a></p>
  </div>
</footer>

<div class="barra-movil"><a class="boton boton-principal" href="#reserva">{e(t["cta"])} <img class="boton-flecha" src="{flecha}" alt="" width="26" height="12"></a></div>

<div class="visor" role="dialog" aria-modal="true" aria-label="{e(t["visor_dialogo"])}" hidden>
  <button type="button" class="visor-cerrar" aria-label="{e(t["visor_cerrar"])}">×</button>
  <button type="button" class="visor-ant" aria-label="{e(t["anterior"])}"><img src="{flecha}" alt=""></button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button type="button" class="visor-sig" aria-label="{e(t["siguiente"])}"><img src="{flecha}" alt=""></button>
</div>

<script id="datos" type="application/json">{datos}</script>
<script src="{pref}js/site.js?v=__V__" defer></script>
</body>
</html>
"""


def main():
    import hashlib
    v = hashlib.sha1((RAIZ / "css/site.css").read_bytes() + (RAIZ / "js/site.js").read_bytes()).hexdigest()[:8]
    for clave, ruta in (("es", RAIZ / "index.html"), ("en", RAIZ / "en/index.html")):
        html = pagina(T[clave]).replace("__V__", v)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(html, encoding="utf-8", newline="\n")
        print("escrito", ruta.relative_to(RAIZ.parent))
    # Tipografía española: sin preposiciones ni conjunciones a final de línea
    import subprocess, sys
    subprocess.run([sys.executable, str(Path(__file__).parent / "tools_nbsp.py"),
                    str(RAIZ / "index.html"), str(RAIZ / "privacidad.html")], check=True)


if __name__ == "__main__":
    main()
