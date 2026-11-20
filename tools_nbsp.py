#!/usr/bin/env python3
"""Tipografia ES: evita que preposiciones/conjunciones cierren linea y que quede
una sola palabra suelta al final de una frase. Inserta U+00A0 (NBSP).

Uso:  python nbsp.py fichero.html [mas.html ...]
Procesa SOLO texto visible: salta <script>, <style>, el interior de las etiquetas
y las entidades HTML. Nunca borra espacios existentes. Idempotente."""
import re, sys

WORDS = [
    "a","ante","bajo","cabe","con","contra","de","desde","durante","en","entre",
    "hacia","hasta","mediante","para","por","segun","sin","so","sobre","tras","via",
    "del","al",
    "y","e","o","u","ni","que","si","pero","mas","sino","pues","como","porque","aunque",
]
WORD_RE = "(?:" + "|".join(sorted(WORDS, key=len, reverse=True)) + ")"
NBSP = chr(0xA0)

# 1) palabra funcional seguida de palabra normal -> pega la funcional a la siguiente
GLUE_FUNC = re.compile(r"\b(" + WORD_RE + r")[ \t](?=[^\s<&" + NBSP + r"])", re.IGNORECASE)
# 2) ultimas dos palabras antes de . ! ? de cierre de frase (no toca el espacio de detras)
GLUE_SENT = re.compile(r"(\S)[ \t](\S+[.!?])(?=[ \t\r\n<]|$)")
# 3) ultimas dos palabras al final del bloque, conservando el espacio en blanco final
GLUE_END  = re.compile(r"(\S)[ \t](\S+)([ \t\r\n]*)\Z")

SKIP = re.compile(r"(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>|&[a-zA-Z#0-9]+;)",
                  re.IGNORECASE | re.DOTALL)

def glue_text(t):
    t = GLUE_FUNC.sub(lambda m: m.group(1) + NBSP, t)
    t = GLUE_SENT.sub(lambda m: m.group(1) + NBSP + m.group(2), t)
    if t.strip():
        t = GLUE_END.sub(lambda m: m.group(1) + NBSP + m.group(2) + m.group(3), t)
    return t

def process(html):
    out, last = [], 0
    for m in SKIP.finditer(html):
        out.append(glue_text(html[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(glue_text(html[last:]))
    return "".join(out)

for path in sys.argv[1:]:
    src = open(path, encoding="utf-8").read()
    new = process(src)
    # invariante: no se pierde ni un espacio (nº de palabras identico)
    assert len(re.findall(r"\S+", src)) == len(re.findall(r"\S+", new.replace(NBSP, " "))), path
    open(path, "w", encoding="utf-8", newline="\n").write(new)
    print(path + ": NBSP -> " + str(new.count(NBSP)))
