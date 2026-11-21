#!/usr/bin/env python3
"""Genera docs/index.html (ES) y docs/en/index.html (EN) desde una sola plantilla.

Uso: python build.py
La web es un dossier de presentación del libro para lectores y para librerías
y tiendas. Enseña poco del interior a propósito (6 acuarelas y 1 doble página).
Los textos están aquí abajo; si cambia uno, cámbialo en los dos idiomas.
"""
from html import escape
from pathlib import Path
import json

RAIZ = Path(__file__).parent / "docs"
URL = "https://flechasamarillas.aldaraalvarez.es"
WEB3FORMS_KEY = "9730a2ad-8c3b-43d9-b68c-ad611768d778"  # clave pública de Web3Forms (la misma de portamook)
INDEXAR = True
SITIO_ANALITICA = "-SnVv6aGs1Ub"  # código público del sitio en la analítica (sin cookies)

# Índice del libro: solo nombres, sin ilustraciones
ACTOS = [
    ("Oporto y el Miño", "Porto and the Minho",
     ["Porto", "Matosinhos", "Vila do Conde", "Esposende", "Viana do Castelo", "Âncora", "Moledo", "Caminha"]),
    ("Tierras gallegas", "Galician lands",
     ["A Guarda", "Oia", "Baiona", "Nigrán", "Vigo", "Redondela", "Arcade"]),
    ("Las Rías Baixas", "The Rías Baixas",
     ["Pontevedra", "Combarro", "Barro", "Caldas de Reis", "Valga", "Pontecesures"]),
    ("Los últimos kilómetros", "The final kilometres",
     ["Padrón", "A Escravitude", "Milladoiro", "Santiago de Compostela"]),
]
# Muestra: 6 acuarelas (id, nombre, pie ES, pie EN, ancho, alto del webp de 800)
MUESTRA = [
    ("porto", "Porto", "Porto", "La fachada románica de la Sé do Porto", "The Romanesque facade of Porto Cathedral"),
    ("flechas-azules", "Las flechas azules", "The Blue Arrows", "Un mojón con la flecha azul de Fátima y la amarilla de Santiago", "A waymarker with Fátima’s blue arrow and Santiago’s yellow one"),
    ("baiona", "Baiona", "Baiona", "La réplica de la carabela Pinta", "The replica of the caravel Pinta"),
    ("combarro", "Combarro", "Combarro", "Hórreos de piedra sobre las rocas", "Stone granaries over the rocks"),
    ("padron", "Padrón", "Padrón", "Pimientos de Padrón recién recogidos", "Freshly picked Padrón peppers"),
    ("santiago", "Santiago de Compostela", "Santiago de Compostela", "La Praza do Obradoiro, frente a la catedral", "Praza do Obradoiro, facing the cathedral"),
]

T = {
    "es": dict(
        lang="es", raiz="", otro="/en/", otro_txt="English", otro_lang="en", otro_aria="Read in English",
        title="Lo que esconden las flechas amarillas · Camino Portugués por la Costa",
        desc="Libro de bolsillo ilustrado en acuarela por Aldara Álvarez González: 25 lugares del Camino Portugués por la Costa, de Oporto a Santiago, en español y en inglés. Para lectores, librerías y tiendas del Camino.",
        saltar="Saltar al contenido",
        marca="Lo que esconden las flechas amarillas", marca_corta="Las flechas amarillas",
        nav=[("#libro", "El libro"), ("#contenido-libro", "Contenido"), ("#librerias", "Librerías y tiendas"), ("#autora", "La autora")],
        contacto="Contacto",
        ante="Camino Portugués por la Costa · De Oporto a Santiago",
        h1="Lo que esconden las flechas amarillas", h1_html="Lo que esconden<br>las flechas amarillas",
        h1_en="Behind the Yellow Arrows",
        lema="Detrás de cada flecha amarilla hay algo que nadie te cuenta.",
        lema_en="Behind every yellow arrow there is something nobody tells you.",
        resumen="Un libro de bolsillo, ilustrado en acuarela, con 25 lugares del camino contados en español y en inglés.",
        cta="Reserva tu ejemplar", cta2="Soy librería o tienda",
        estado="Edición de 2026 · Precio por confirmar",
        portada_alt="Cubierta del libro con un mojón de piedra, una vieira y una flecha amarilla junto al mar",
        libro_ante="El libro",
        libro_h="Lo que la flecha señala pero nunca explica",
        libro_txt=[
            "Las flechas amarillas dicen al peregrino por dónde ir, pero no qué hay a su alrededor. Este libro cuenta algo pequeño de 25 lugares del Camino Portugués por la Costa, de Oporto a Santiago: una piedra, una leyenda, un plato.",
            "No es una guía práctica. No da distancias ni albergues. Es un libro para llevar en el bolsillo y leer en las paradas, y para guardar al volver.",
        ],
        razones_h="Por qué funciona",
        razones=[
            ("De bolsillo", "Formato A6 y poco peso. Cabe en la mochila de quien ya carga bastante."),
            ("Bilingüe", "Cada texto en español y, debajo, en inglés sencillo, pensado para peregrinos de cualquier país."),
            ("Ilustrado a mano", "Una acuarela por lugar y una flecha amarilla escondida en cada una."),
            ("Un recuerdo del Camino", "Se lee durante la ruta y se queda como regalo o recuerdo al terminarla."),
        ],
        muestra_ante="Una muestra",
        muestra_h="Así es por dentro",
        muestra_txt="Cada lugar ocupa una doble página, con la ilustración a la izquierda y la historia a la derecha.",
        doble_alt="Doble página de Vila do Conde con la ilustración del acueducto y el texto en español e inglés",
        doble_pie="Doble página de Vila do Conde",
        doble2_alt="Doble página de Oia con la ilustración del monasterio y el texto en español e inglés",
        doble2_pie="Doble página de Oia",
        doble3_alt="Doble página de Arcade con la ilustración de las bateas de ostras y el texto en español e inglés",
        doble3_pie="Doble página de Arcade",
        contenido_ante="Contenido",
        contenido_h="Cuatro actos, de Oporto a Santiago",
        contenido_txt="El libro sigue el camino en el orden en que se recorre. Además, cuatro fichas temáticas y un epílogo.",
        mapa_alt="Mapa en acuarela de la costa de Portugal y Galicia con los cuatro actos del camino",
        acto="Acto",
        extras=[("Introducción", "La flecha amarilla y las flechas azules"), ("Temas", "Gastronomía, clima, naturaleza y arquitectura"), ("Epílogo", "Fisterra, un poco más allá")],
        ficha_h="Ficha técnica",
        ficha=[
            ("Título", "Lo que esconden las flechas amarillas"),
            ("Título en inglés", "Behind the Yellow Arrows"),
            ("Texto e ilustraciones", "Aldara Álvarez González"),
            ("Idiomas", "Español e inglés"),
            ("Páginas", "88, a color"),
            ("Formato", "A6, 105 × 148 mm"),
            ("Edición", "2026"),
            ("Precio", "Por confirmar"),
        ],
        lib_ante="Para librerías y tiendas",
        lib_h="Un libro para el mostrador del Camino",
        lib_txt="Pensado para librerías, tiendas de recuerdos, albergues y puntos de información a lo largo del Camino Portugués y en Santiago.",
        lib_puntos=[
            "Formato pequeño, fácil de exponer junto a la caja.",
            "Precio de bolsillo, al alcance de una compra de impulso.",
            "Bilingüe, para el peregrino nacional y el extranjero.",
            "Habla de los lugares por los que pasa tu cliente.",
        ],
        lib_cond="Si quieres tenerlo en tu tienda, escríbenos y te contamos las condiciones.",
        lib_cta="Pedir información",
        autora_ante="La autora",
        autora_nombre="Aldara Álvarez González",
        autora_txt="Diseñadora e ilustradora de Baiona, en el Camino Portugués por la Costa. Ha escrito, ilustrado y maquetado el libro.",
        autora_cita="Este libro nació de una idea sencilla: contar, entre Oporto y Santiago, todo lo que una flecha amarilla señala pero nunca explica.",
        autora_cita_en="This book began with a simple idea: to tell, between Porto and Santiago, everything a yellow arrow points to but never explains.",
        autora_web="Ver su trabajo",
        con_ante="Contacto",
        con_h="Reserva o pide información",
        con_txt="El libro está a punto de imprimirse. Reservar no compromete a nada: te escribiremos con el precio cuando esté listo.",
        tipo_leg="¿Quién eres?", tipo_lector="Quiero el libro", tipo_tienda="Librería o tienda",
        f_nombre="Nombre", f_email="Correo electrónico", f_cantidad="Ejemplares", f_cantidad_t="Ejemplares orientativos",
        f_menos="Uno menos", f_mas="Uno más",
        f_comercio="Nombre del comercio", f_localidad="Localidad", f_telefono="Teléfono",
        f_opcional="(opcional)", f_mensaje="Mensaje",
        f_privacidad='He leído la <a href="{raiz}/privacidad.html">política de privacidad</a> y acepto que se usen mis datos solo para responder a esta solicitud.',
        f_enviar_l="Reservar sin compromiso", f_enviar_t="Pedir información", f_enviando="Enviando…",
        f_aviso="Solo te escribiremos sobre este libro.",
        f_err_nombre="Escribe tu nombre.", f_err_email="Revisa el correo, parece incompleto.",
        f_err_comercio="Escribe el nombre del comercio.",
        f_err_priv="Necesitamos que aceptes la política de privacidad.",
        f_err_red="No se ha podido enviar. Prueba de nuevo en un momento.",
        f_err_lim="Has enviado varias solicitudes seguidas. Prueba de nuevo dentro de un rato.",
        ok_h="Recibido",
        ok_l="Gracias. Te escribiremos a {email} cuando el libro esté impreso. Buen camino.",
        ok_t="Gracias. Te escribiremos a {email} con las condiciones para tu tienda.",
        ok_otra="Enviar otra",
        pie_final="Aquí se acaban las flechas de esta página. Lo que viene lo escribes tú.",
        pie_copy="© 2026 Aldara Álvarez González. Textos e ilustraciones originales.",
        privacidad="Privacidad",
    ),
    "en": dict(
        lang="en", raiz="/en", otro="/", otro_txt="Español", otro_lang="es", otro_aria="Leer en español",
        title="Behind the Yellow Arrows · Portuguese Coastal Way",
        desc="A pocket book illustrated in watercolour by Aldara Álvarez González: 25 places on the Portuguese Coastal Way, from Porto to Santiago, in Spanish and English. For readers, bookshops and shops on the Camino.",
        saltar="Skip to content",
        marca="Behind the Yellow Arrows", marca_corta="The Yellow Arrows",
        nav=[("#libro", "The book"), ("#contenido-libro", "Contents"), ("#librerias", "Bookshops"), ("#autora", "The author")],
        contacto="Contact",
        ante="Portuguese Coastal Way · From Porto to Santiago",
        h1="Behind the Yellow Arrows", h1_html="Behind the<br>Yellow Arrows",
        h1_en="Lo que esconden las flechas amarillas",
        lema="Behind every yellow arrow there is something nobody tells you.",
        lema_en="Detrás de cada flecha amarilla hay algo que nadie te cuenta.",
        resumen="A pocket book, illustrated in watercolour, with 25 places on the Way told in Spanish and English.",
        cta="Reserve your copy", cta2="I run a bookshop or shop",
        estado="2026 edition · Price to be confirmed",
        portada_alt="Book cover with a stone waymarker, a scallop shell and a yellow arrow by the sea",
        libro_ante="The book",
        libro_h="What the arrow points to but never explains",
        libro_txt=[
            "Yellow arrows tell pilgrims where to go, but not what is around them. This book tells one small thing about 25 places on the Portuguese Coastal Way, from Porto to Santiago: a stone, a legend, a dish.",
            "It is not a practical guide. It gives no distances and no hostels. It is a book to carry in your pocket and read when you stop, and to keep when you get home.",
        ],
        razones_h="Why it works",
        razones=[
            ("Pocket size", "A6 and light. It fits in the backpack of someone who already carries enough."),
            ("Bilingual", "Every text in Spanish with simple English below, written for pilgrims from any country."),
            ("Painted by hand", "One watercolour for each place, with a yellow arrow hidden in every one."),
            ("A keepsake of the Way", "Read along the route, then kept as a gift or a memory once it is over."),
        ],
        muestra_ante="A sample",
        muestra_h="What it looks like inside",
        muestra_txt="Each place has a double page, with the illustration on the left and its story on the right.",
        doble_alt="Double page about Vila do Conde with the aqueduct illustration and the text in Spanish and English",
        doble_pie="Double page about Vila do Conde",
        doble2_alt="Double page about Oia with the monastery illustration and the text in Spanish and English",
        doble2_pie="Double page about Oia",
        doble3_alt="Double page about Arcade with the oyster rafts illustration and the text in Spanish and English",
        doble3_pie="Double page about Arcade",
        contenido_ante="Contents",
        contenido_h="Four acts, from Porto to Santiago",
        contenido_txt="The book follows the Way in the order you walk it. It also has four theme pages and an epilogue.",
        mapa_alt="Watercolour map of the coast of Portugal and Galicia with the four acts of the Way",
        acto="Act",
        extras=[("Introduction", "The yellow arrow and the blue arrows"), ("Themes", "Food, weather, nature and architecture"), ("Epilogue", "Fisterra, a little further")],
        ficha_h="Book details",
        ficha=[
            ("Title", "Behind the Yellow Arrows"),
            ("Spanish title", "Lo que esconden las flechas amarillas"),
            ("Text and illustrations", "Aldara Álvarez González"),
            ("Languages", "Spanish and English"),
            ("Pages", "88, in colour"),
            ("Format", "A6, 105 × 148 mm"),
            ("Edition", "2026"),
            ("Price", "To be confirmed"),
        ],
        lib_ante="For bookshops and shops",
        lib_h="A book for the counter on the Camino",
        lib_txt="Made for bookshops, gift shops, hostels and information points along the Portuguese Way and in Santiago.",
        lib_puntos=[
            "Small format, easy to display by the till.",
            "Pocket price, within reach of an impulse buy.",
            "Bilingual, for Spanish and international pilgrims alike.",
            "It talks about the places your customers walk through.",
        ],
        lib_cond="If you would like to stock it, write to us and we will tell you the terms.",
        lib_cta="Ask for information",
        autora_ante="The author",
        autora_nombre="Aldara Álvarez González",
        autora_txt="Designer and illustrator from Baiona, on the Portuguese Coastal Way. She wrote, illustrated and designed the book.",
        autora_cita="This book began with a simple idea: to tell, between Porto and Santiago, everything a yellow arrow points to but never explains.",
        autora_cita_en="Este libro nació de una idea sencilla: contar, entre Oporto y Santiago, todo lo que una flecha amarilla señala pero nunca explica.",
        autora_web="See her work",
        con_ante="Contact",
        con_h="Reserve a copy or ask for information",
        con_txt="The book is about to be printed. Reserving does not commit you to anything: we will write to you with the price when it is ready.",
        tipo_leg="Who are you?", tipo_lector="I want the book", tipo_tienda="Bookshop or shop",
        f_nombre="Name", f_email="Email", f_cantidad="Copies", f_cantidad_t="Approximate copies",
        f_menos="One less", f_mas="One more",
        f_comercio="Shop name", f_localidad="Town or city", f_telefono="Phone",
        f_opcional="(optional)", f_mensaje="Message",
        f_privacidad='I have read the <a href="{raiz}/privacidad.html">privacy policy</a> and agree to my data being used only to answer this request.',
        f_enviar_l="Reserve, no commitment", f_enviar_t="Ask for information", f_enviando="Sending…",
        f_aviso="We will only write to you about this book.",
        f_err_nombre="Please write your name.", f_err_email="Please check your email, it looks incomplete.",
        f_err_comercio="Please write the shop name.",
        f_err_priv="Please accept the privacy policy.",
        f_err_red="It could not be sent. Please try again in a moment.",
        f_err_lim="You have sent several requests in a row. Please try again later.",
        ok_h="Received",
        ok_l="Thank you. We will write to {email} when the book is printed. Buen camino.",
        ok_t="Thank you. We will write to {email} with the terms for your shop.",
        ok_otra="Send another",
        pie_final="Here the arrows of this page end. What comes next, you write.",
        pie_copy="© 2026 Aldara Álvarez González. Original text and illustrations.",
        privacidad="Privacy",
    ),
}

ROMANOS = ["I", "II", "III", "IV"]


def e(s):
    return escape(s, quote=True)


def pagina(t):
    L = t["lang"]
    es = L == "es"
    R = t["raiz"]
    pref = "" if es else "../"
    flecha = f"{pref}img/flecha.png"
    otro = t["otro_lang"]

    datos = json.dumps(dict(t=dict(
        enviando=t["f_enviando"], enviar_l=t["f_enviar_l"], enviar_t=t["f_enviar_t"],
        err_nombre=t["f_err_nombre"], err_email=t["f_err_email"], err_comercio=t["f_err_comercio"],
        err_priv=t["f_err_priv"], err_red=t["f_err_red"], err_lim=t["f_err_lim"],
        ok_l=t["ok_l"], ok_t=t["ok_t"])), ensure_ascii=False)

    nav = "".join(f'<a href="{h}" class="nav-secundario">{e(x)}</a>' for h, x in t["nav"])
    libro_txt = "".join(f"<p>{e(p)}</p>" for p in t["libro_txt"])
    ICONOS = [
        '<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="13" y="6" width="22" height="36" rx="2.5"/><path d="M13 14h22M19 22h10M19 28h10M19 34h6"/></svg>',
        '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M7 11h22a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H18l-7 6v-6H7a2 2 0 0 1-2-2V13a2 2 0 0 1 2-2z"/><path d="M33 19h8a2 2 0 0 1 2 2v13a2 2 0 0 1-2 2h-3v5l-6-5h-8a2 2 0 0 1-2-2v-3"/></svg>',
        '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M8 40c2-1 4-5 6-8l4 3c-2 3-5 6-10 5z"/><path d="M18 32L38 8c2-2 5 1 3 3L21 35"/><path d="M12 43c6 0 10-2 14-2"/></svg>',
        '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 42S7 31 7 19a9 9 0 0 1 17-4 9 9 0 0 1 17 4c0 12-17 23-17 23z"/><path d="M17 22h14m-5-5l5 5-5 5"/></svg>',
    ]
    razones = "".join(f'<li><span class="razon-icono">{ICONOS[i]}</span><span class="razon-n" aria-hidden="true">0{i+1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(t["razones"]))

    muestra = ""
    for mid, nes, nen, pes, pen in MUESTRA:
        nom = e(nes if es else nen)
        if mid == "flechas-azules":
            nom = nom.replace(" azules", ' <br class="salto-m">azules') if es else nom.replace("The ", 'The <br class="salto-m">')
        muestra += (f'<figure class="aparece"><button type="button" class="muestra-img ampliable" aria-label="{e(pes if es else pen)}">'
                    f'<img class="acuarela" src="{pref}img/muestra/{mid}.webp" data-grande="{pref}img/muestra/{mid}-grande.webp" '
                    f'alt="{e(pes if es else pen)}" loading="lazy" decoding="async"></button>'
                    f'<figcaption><b>{nom}</b><span>{e(pes if es else pen)}</span></figcaption></figure>')

    actos = ""
    for i, (tes, ten, lugares) in enumerate(ACTOS):
        lis = "".join(f"<li>{e(x)}</li>" for x in lugares)
        actos += (f'<div class="acto"><h3>{e(t["acto"])} {ROMANOS[i]}</h3>'
                  f'<h4>{e(tes if es else ten)}</h4><ol>{lis}</ol></div>')
    extras = "".join(f"<p><strong>{e(a)}</strong> {e(b)}</p>" for a, b in t["extras"])
    ficha = "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in t["ficha"])
    lib_puntos = "".join(f"<li>{e(p)}</li>" for p in t["lib_puntos"])

    robots = "index,follow" if INDEXAR else "noindex,follow"
    canon = URL + ("/" if es else "/en/")

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
    "inLanguage": ["es", "en"], "numberOfPages": 88, "bookFormat": "https://schema.org/Paperback",
    "about": "Camino Portugués por la Costa", "image": URL + "/img/portada.webp",
    "description": t["desc"]}, ensure_ascii=False)}</script>
</head>
<body class="sin-js">
<a class="salto" href="#contenido">{e(t["saltar"])}</a>
<header class="cabecera">
  <div class="envoltura">
    <a class="marca" href="{R}/"><img src="{flecha}" alt="" width="30" height="14"><span class="marca-larga">{e(t["marca"])}</span><span class="marca-corta">{e(t["marca_corta"])}</span></a>
    <button type="button" class="menu-boton" aria-expanded="false" aria-controls="menu" aria-label="{'Menú' if es else 'Menu'}"><span></span><span></span><span></span></button>
    <nav class="nav" id="menu" aria-label="{'Principal' if es else 'Main'}">
      {nav}
      <a class="idioma" href="{t["otro"]}" hreflang="{otro}" lang="{otro}" aria-label="{e(t["otro_aria"])}">{e(t["otro_txt"])}</a>
      <a class="boton boton-principal" href="#contacto">{e(t["contacto"])}</a>
    </nav>
  </div>
</header>

<main id="contenido">
<section class="portada">
  <div class="envoltura">
    <div class="portada-texto">
      <p class="antetitulo">{e(t["ante"])}</p>
      <h1 class="titulo titulo-xl">{t["h1_html"]}</h1>
      <p class="en-titulo" lang="{otro}">{e(t["h1_en"])}</p>
      <p class="lema">{e(t["lema"])}</p>
      <p class="lema-en en" lang="{otro}">{e(t["lema_en"])}</p>
      <p class="portada-resumen">{e(t["resumen"])}</p>
      <div class="acciones">
        <a class="boton boton-principal" href="#contacto" data-tipo="lector">{e(t["cta"])} <img class="boton-flecha" src="{flecha}" alt="" width="26" height="12"></a>
        <a class="boton boton-secundario" href="#contacto" data-tipo="tienda">{e(t["cta2"])}</a>
      </div>
      <p class="estado">{e(t["estado"])}</p>
    </div>
    <div class="libro">
      <div class="libro3d"><img class="libro-cubierta" src="{pref}img/portada-520.webp" srcset="{pref}img/portada-520.webp 800w, {pref}img/portada-1100.webp 1100w, {pref}img/portada.webp 1700w" sizes="(max-width:820px) 70vw, 420px" alt="{e(t["portada_alt"])}" width="800" height="1128" fetchpriority="high"><span class="lomo" style="background-image:url({pref}img/lomo.webp)"></span></div>
    </div>
  </div>
</section>

<section class="seccion seccion-calida" id="libro">
  <div class="envoltura">
    <div class="libro-intro aparece">
      <div>
        <p class="antetitulo">{e(t["libro_ante"])}</p>
        <h2 class="titulo titulo-l">{e(t["libro_h"])}</h2>
      </div>
      <div class="libro-intro-texto">{libro_txt}</div>
    </div>
    <h3 class="sr">{e(t["razones_h"])}</h3>
    <ul class="razones aparece">{razones}</ul>
  </div>
</section>

<section class="seccion" id="muestra">
  <div class="envoltura">
    <div class="cabeza-seccion aparece">
      <p class="antetitulo">{e(t["muestra_ante"])}</p>
      <h2 class="titulo titulo-l">{e(t["muestra_h"])}</h2>
      <p>{e(t["muestra_txt"])}</p>
    </div>
    <div class="muestra">{muestra}</div>
    <div class="dobles">
    <figure class="doble aparece">
      <button type="button" class="ampliable" aria-label="{e(t["doble_alt"])}"><img src="{pref}img/muestra/doble.webp" data-grande="{pref}img/muestra/doble-grande.webp" alt="{e(t["doble_alt"])}" loading="lazy" decoding="async" width="1200" height="846"></button>
      <figcaption>{e(t["doble_pie"])}</figcaption>
    </figure>
    <figure class="doble aparece">
      <button type="button" class="ampliable" aria-label="{e(t["doble2_alt"])}"><img src="{pref}img/muestra/doble-oia.webp" data-grande="{pref}img/muestra/doble-oia-grande.webp" alt="{e(t["doble2_alt"])}" loading="lazy" decoding="async" width="1200" height="846"></button>
      <figcaption>{e(t["doble2_pie"])}</figcaption>
    </figure>
    <figure class="doble doble-movil aparece">
      <button type="button" class="ampliable" aria-label="{e(t["doble3_alt"])}"><img src="{pref}img/muestra/doble-arcade.webp" data-grande="{pref}img/muestra/doble-arcade-grande.webp" alt="{e(t["doble3_alt"])}" loading="lazy" decoding="async" width="1200" height="846"></button>
      <figcaption>{e(t["doble3_pie"])}</figcaption>
    </figure>
    </div>
  </div>
</section>

<section class="seccion seccion-calida" id="contenido-libro">
  <div class="envoltura camino">
    <figure class="mapa aparece"><img class="acuarela" src="{pref}img/muestra/mapa.webp" alt="{e(t["mapa_alt"])}" loading="lazy" width="1100" height="1616"></figure>
    <div>
      <div class="cabeza-seccion aparece">
        <p class="antetitulo">{e(t["contenido_ante"])}</p>
        <h2 class="titulo titulo-l">{e(t["contenido_h"])}</h2>
        <p>{e(t["contenido_txt"])}</p>
      </div>
      <div class="actos aparece">{actos}</div>
      <div class="extras aparece">{extras}</div>
    </div>
  </div>
</section>

<section class="seccion" id="ficha">
  <div class="envoltura ficha-bloque aparece">
    <h2 class="titulo titulo-m">{e(t["ficha_h"])}</h2>
    <dl class="ficha-tecnica">{ficha}</dl>
  </div>
</section>

<section class="seccion seccion-librerias" id="librerias">
  <div class="envoltura librerias aparece">
    <div>
      <p class="antetitulo">{e(t["lib_ante"])}</p>
      <h2 class="titulo titulo-l">{e(t["lib_h"])}</h2>
      <p class="librerias-intro">{e(t["lib_txt"])}</p>
    </div>
    <div>
      <ul class="lista-flechas">{lib_puntos}</ul>
      <p class="librerias-cond">{e(t["lib_cond"])}</p>
      <a class="boton boton-principal" href="#contacto" data-tipo="tienda">{e(t["lib_cta"])} <img class="boton-flecha" src="{flecha}" alt="" width="26" height="12"></a>
    </div>
  </div>
</section>

<section class="seccion" id="autora">
  <div class="envoltura autora aparece">
    <blockquote><p>«{e(t["autora_cita"])}»</p><span class="en" lang="{otro}">{e(t["autora_cita_en"])}</span></blockquote>
    <div>
      <p class="antetitulo">{e(t["autora_ante"])}</p>
      <p class="autora-nombre">{e(t["autora_nombre"])}</p>
      <p>{e(t["autora_txt"])}</p>
      <a class="boton boton-secundario" href="https://aldaraalvarez.es{'' if es else '/en/'}" rel="noopener">{e(t["autora_web"])} <svg class="icono-ext" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M5 3h8v8M13 3L3 13" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
    </div>
  </div>
</section>

<section class="seccion seccion-calida" id="contacto">
  <div class="envoltura reserva">
    <div class="aparece">
      <p class="antetitulo">{e(t["con_ante"])}</p>
      <h2 class="titulo titulo-l">{e(t["con_h"])}</h2>
      <p style="margin-top:1rem">{e(t["con_txt"])}</p>
    </div>
    <div class="formulario aparece" id="formulario">
      <form novalidate action="https://api.web3forms.com/submit" method="post" data-tipo-actual="lector" data-wf="{WEB3FORMS_KEY}">
        <input type="hidden" name="idioma" value="{L}">
        <div class="trampa" aria-hidden="true"><label>Web <input type="text" name="web" tabindex="-1" autocomplete="off"></label></div>
        <fieldset class="campo"><legend>{e(t["tipo_leg"])}</legend>
          <div class="selector-tipo">
            <label><input type="radio" name="tipo" value="lector" checked> {e(t["tipo_lector"])}</label>
            <label><input type="radio" name="tipo" value="tienda"> {e(t["tipo_tienda"])}</label>
          </div>
        </fieldset>
        <div class="fila">
          <div class="campo"><label for="f-nombre">{e(t["f_nombre"])}</label><input id="f-nombre" name="nombre" autocomplete="name" required maxlength="120"><p class="campo-error" id="e-nombre">{e(t["f_err_nombre"])}</p></div>
          <div class="campo"><label for="f-email">{e(t["f_email"])}</label><input id="f-email" name="email" type="email" inputmode="email" autocomplete="email" required maxlength="160" spellcheck="false"><p class="campo-error" id="e-email">{e(t["f_err_email"])}</p></div>
        </div>
        <div class="fila solo-tienda">
          <div class="campo solo-tienda"><label for="f-comercio">{e(t["f_comercio"])}</label><input id="f-comercio" name="comercio" autocomplete="organization" maxlength="160"><p class="campo-error" id="e-comercio">{e(t["f_err_comercio"])}</p></div>
          <div class="campo solo-tienda"><label for="f-telefono">{e(t["f_telefono"])} <span class="opcional">{e(t["f_opcional"])}</span></label><input id="f-telefono" name="telefono" type="tel" autocomplete="tel" maxlength="40"></div>
        </div>
        <div class="fila">
          <div class="campo"><label for="f-cantidad"><span class="solo-lector-txt">{e(t["f_cantidad"])}</span><span class="solo-tienda-txt">{e(t["f_cantidad_t"])}</span></label>
            <div class="contador"><button type="button" data-paso="-1" aria-label="{e(t["f_menos"])}">−</button><input id="f-cantidad" name="cantidad" type="number" inputmode="numeric" min="1" max="500" value="1"><button type="button" data-paso="1" aria-label="{e(t["f_mas"])}">+</button></div>
          </div>
          <div class="campo"><label for="f-localidad">{e(t["f_localidad"])} <span class="opcional solo-lector-txt">{e(t["f_opcional"])}</span></label><input id="f-localidad" name="localidad" autocomplete="address-level2" maxlength="120"></div>
        </div>
        <div class="campo"><label for="f-mensaje">{e(t["f_mensaje"])} <span class="opcional">{e(t["f_opcional"])}</span></label><textarea id="f-mensaje" name="mensaje" maxlength="1500" rows="2"></textarea></div>
        <label class="consentimiento"><input type="checkbox" name="privacidad" value="si" required id="f-priv"><span>{t["f_privacidad"].format(raiz=R)}</span></label>
        <button class="boton boton-principal" type="submit"><span class="boton-texto">{e(t["f_enviar_l"])}</span> <img class="boton-flecha" src="{flecha}" alt="" width="26" height="12"></button>
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
    <p style="margin:0">{e(t["pie_copy"])} · <a href="{R}/privacidad.html">{e(t["privacidad"])}</a> · <a href="{t["otro"]}" hreflang="{otro}" lang="{otro}">{e(t["otro_txt"])}</a></p>
  </div>
</footer>

<div class="barra-movil"><a class="boton boton-principal" href="#contacto">{e(t["cta"])} <img class="boton-flecha" src="{flecha}" alt="" width="26" height="12"></a></div>

<script id="datos" type="application/json">{datos}</script>
<script src="{pref}js/site.js?v=__V__" defer></script>
{ANALITICA}
</body>
</html>
"""


ANALITICA = """<script>
(function(d,l){var u=new URLSearchParams(l.search),q=function(k){return encodeURIComponent(u.get(k)||'')};
new Image().src='https://nanuve.net/v?site=%s&path='+encodeURIComponent(l.pathname)+'&ref='+encodeURIComponent(d.referrer)
+'&w='+screen.width+'&l='+encodeURIComponent(navigator.language||'')+'&us='+q('utm_source')+'&um='+q('utm_medium')+'&uc='+q('utm_campaign');
})(document,location);
</script>""" % SITIO_ANALITICA


def sitemap():
    pag = [("/", "/en/"), ("/en/", "/")]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for ruta, _ in pag:
        out.append(f"  <url><loc>{URL}{ruta}</loc>")
        if ruta in ("/", "/en/"):
            out += [f'    <xhtml:link rel="alternate" hreflang="es" href="{URL}/"/>',
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{URL}/en/"/>',
                    f'    <xhtml:link rel="alternate" hreflang="x-default" href="{URL}/"/>']
        out.append("  </url>")
    out.append("</urlset>")
    return chr(10).join(out) + chr(10)


ROBOTS = f"""# Lo que esconden las flechas amarillas
# Politica de IA: buscadores y asistentes pueden leer y citar la web;
# el entrenamiento de modelos con su contenido no esta permitido.

User-agent: *
Allow: /
Content-Signal: ai-train=no, search=yes, ai-input=yes

User-agent: GPTBot
User-agent: ClaudeBot
User-agent: anthropic-ai
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: CCBot
User-agent: Bytespider
User-agent: Meta-ExternalAgent
User-agent: cohere-ai
Disallow: /

Sitemap: {URL}/sitemap.xml
"""


def main():
    import hashlib
    import subprocess
    import sys
    v = hashlib.sha1((RAIZ / "css/site.css").read_bytes() + (RAIZ / "js/site.js").read_bytes()).hexdigest()[:8]
    for clave, ruta in (("es", RAIZ / "index.html"), ("en", RAIZ / "en/index.html")):
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(pagina(T[clave]).replace("__V__", v), encoding="utf-8", newline="\n")
        print("escrito", ruta.relative_to(RAIZ.parent), flush=True)
    (RAIZ / "sitemap.xml").write_text(sitemap(), encoding="utf-8", newline=chr(10))
    (RAIZ / "robots.txt").write_text(ROBOTS, encoding="utf-8", newline=chr(10))
    # Tipografía española: sin preposiciones ni conjunciones a final de línea
    subprocess.run([sys.executable, str(Path(__file__).parent / "tools_nbsp.py"),
                    str(RAIZ / "index.html"), str(RAIZ / "privacidad.html")], check=True)


if __name__ == "__main__":
    main()
