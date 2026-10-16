"""Gota en estilo dibujado a mano (inspirado en Hollow Knight), acabado A · Limpio.

Dibuja cada fotograma con curvas vectoriales (SVG), monta una hoja de
fotogramas por variante y la convierte a PNG con transparencia usando
Brave en modo headless. Fuente de verdad del diseño: CONTEXTO_PERSONAJE.md

Uso: python -I gota_hk.py <carpeta Gota>
"""
import json
import math
import os
import subprocess
import sys

TAM = 256          # unidades del lienzo de cada fotograma
ESCALA = 2         # el PNG se renderiza a 512 x 512 por fotograma
COLS = 8
SUELO = 200        # la base de la gota no se mueve
CX = 128
MS_FOTOGRAMA = 83  # ~12 fotogramas por segundo

BRAVE = os.path.join(os.environ["LOCALAPPDATA"], "BraveSoftware", "Brave-Browser",
                     "Application", "brave.exe")

ANCHO = 0.9   # un poco más delgada que la gota clásica


def _x(x):
    return f"{CX + (x - CX) * ANCHO:.2f}"


# Silueta: punta ligeramente redondeada arriba, base redonda y ancha
GOTA = (f"M {_x(130)} 61 C {_x(136)} 74, {_x(178)} 110, {_x(178)} 150 "
        f"A {50 * ANCHO:.2f} 50 0 0 1 {_x(78)} 150 "
        f"C {_x(78)} 110, {_x(120)} 74, {_x(126)} 61 Q {_x(128)} 57.5 {_x(130)} 61 Z")
REFLEJO = f"M {_x(93)} 117 Q {_x(86)} 136 {_x(90)} 156 Q {_x(92.5)} 138 {_x(99)} 119 Z"

ESTILO = ("line{stroke:#dfe3e9;stroke-opacity:.8;stroke-width:3.2;stroke-linecap:round}"
          ".mano{fill:#e9ecf0;fill-opacity:.8;stroke:#cfd5dc;stroke-width:1.2}")

DEFS = f"""
  <linearGradient id="cuerpo" x1="0" y1="60" x2="0" y2="200" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#f1f3f6" stop-opacity="0.38"/>
    <stop offset="0.55" stop-color="#e8ebf0" stop-opacity="0.62"/>
    <stop offset="1" stop-color="#dde2e8" stop-opacity="0.86"/>
  </linearGradient>
  <mask id="fuera" maskUnits="userSpaceOnUse" x="0" y="0" width="256" height="256">
    <rect width="256" height="256" fill="#fff"/><path d="{GOTA}" fill="#000"/>
  </mask>
  <filter id="sombra" x="-50%" y="-200%" width="200%" height="500%">
    <feGaussianBlur stdDeviation="2.5"/>
  </filter>"""

# Postura firme por defecto: pies algo separados y manos abiertas a los lados.
# Distancias "fuera" medidas en horizontal desde el punto de unión.
POSTURA = {
    "mano": (11, 16),        # sin brazos: la mano flota junto al cuerpo (fuera, abajo)
    "manoAz": 100,          # grados entre la mirada y cada mano
    "piernaSep": 14,         # separación de cada pie al eje
    "piernaAbre": 3.5,       # cuánto se abre cada pie hacia fuera
}
INCLINACION = 0.22           # cámara algo elevada: lo cercano se ve más abajo


def ancho_cuerpo(y):
    """Semiancho de la sección horizontal del cuerpo (es de revolución)."""
    d = y - 150
    return ANCHO * math.sqrt(max(0.0, 50 * 50 - d * d))


def respiracion(t, perfil, veces=1):
    """Valor -1..1 del ciclo. 'pausa' aplana los extremos (se detiene arriba y abajo)."""
    s = math.sin(2 * math.pi * veces * t)
    if perfil == "pausa":
        return math.copysign(abs(s) ** 0.55, s)
    return s


OJOS_BASE = {
    "parpado": (0, 0),   # parte superior recortada (lado interior, lado exterior), 0..1
    "ancho": 1, "alto": 1, "dy": 0,
    "mirada": 0,         # grados extra hacia donde mira (+) o hacia la cámara (-)
    "cerrados": False,
    "parpadeo": False,   # parpadea una vez por ciclo
}
_ids = [0]


def ojos_svg(v, t, giro):
    """Ojos negros sólidos, ovalados, sin pupilas. La expresión sale de su forma."""
    e = dict(OJOS_BASE, **(v["ojos_t"](t) if "ojos_t" in v else v.get("ojos", {})))
    r_ojo = ancho_cuerpo(136) * 0.8   # algo menor que el cuerpo: la cara no se pega al borde
    cerrados = e["cerrados"] or (e["parpadeo"] and 0.56 <= t < 0.63)
    res = []
    for lado in (-1, 1):
        az = giro + math.radians(e["mirada"]) + lado * math.radians(12)
        c = math.cos(az)
        if c <= 0.05:
            continue
        ex = CX + r_ojo * math.sin(az)
        rx, ry = 3.4 * c * e["ancho"], 6.2 * e["alto"]
        cy = 136 + e["dy"]
        if cerrados:
            res.append(f'<path d="M {ex - rx - 1.2:.2f} {cy:.2f} Q {ex:.2f} {cy + 2.2:.2f} '
                       f'{ex + rx + 1.2:.2f} {cy:.2f}" fill="none" stroke="#121216" '
                       f'stroke-width="2" stroke-linecap="round"/>')
            continue
        ojo = f'<ellipse cx="{ex:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="#121216"'
        interior, exterior = e["parpado"]
        if not (interior or exterior):
            res.append(ojo + "/>")
            continue
        # El lado interior es el que da hacia el otro ojo
        izq, der = (exterior, interior) if lado == -1 else (interior, exterior)
        arriba = cy - ry
        x0, x1 = ex - rx - 2, ex + rx + 2
        _ids[0] += 1
        cid = f"parpado{_ids[0]}"
        res.append(f'<clipPath id="{cid}"><polygon points="{x0:.2f},{arriba + 2 * ry * izq:.2f} '
                   f'{x1:.2f},{arriba + 2 * ry * der:.2f} {x1:.2f},{cy + ry + 2:.2f} '
                   f'{x0:.2f},{cy + ry + 2:.2f}"/></clipPath>')
        res.append(ojo + f' clip-path="url(#{cid})"/>')
    return res


def fotograma(v, t):
    a = respiracion(t, v.get("perfil"), v.get("respiraciones", 1))
    if "extra_a" in v:            # p. ej. un sobresalto
        a += v["extra_a"](t)
    amp = v.get("amplitud", 0.025)
    sy = 1 + amp * a                         # inspira: un poco más alta
    sx = 1 - amp * 0.48 * a                  # y un poco más estrecha
    manoDy = -v.get("manos", 1.6) * a
    # Pulso de transparencia (reposo prolongado): mínimo al final de la inspiración
    pulso = v.get("pulso", 0)
    op = 1 - pulso * (0.5 - 0.5 * math.cos(2 * math.pi * t))
    if "opacidad_t" in v:
        op = v["opacidad_t"](t)
    op_contorno = 1 - (1 - op) * 0.4
    op_reflejo = 1 - (1 - op) * 0.5
    respira = (f"translate({CX} {SUELO}) scale({sx:.4f} {sy:.4f}) "
               f"translate({-CX} {-SUELO})")
    P = dict(POSTURA, **v.get("postura", {}))
    giro = math.radians(v.get("angulo", 45))   # 0 = de frente; mira hacia la derecha

    def proyectar(az, radio, y):
        """Punto sobre la dirección az (rad, 0 = hacia la cámara) a cierta distancia del eje."""
        x = CX + radio * math.sin(az)
        z = radio * math.cos(az)
        return x, y + z * INCLINACION, z

    delante, detras = [], []   # extremidades delante o detrás del cuerpo

    # Manos (sin brazos): flotan junto al lateral del cuerpo
    mo, md = P["mano"]
    for lado in (-1, 1):
        az = giro + lado * math.radians(P["manoAz"])
        r0 = ancho_cuerpo(160)
        _, _, z = proyectar(az, r0, 160)
        xh, yh, _ = proyectar(az, r0 + mo, 160 + md)
        if z <= 0:
            # Mano lejana: asoma por detrás del borde de la silueta
            lado_x = 1 if math.sin(az) >= 0 else -1
            xh = CX + lado_x * (ancho_cuerpo(yh) + 1.5)
        trozo = f'<circle class="mano" cx="{xh:.2f}" cy="{yh + manoDy:.2f}" r="4.6"/>'
        (delante if z > 0 else detras).append(trozo)

    # Pies (sin piernas): flotan bajo el cuerpo y no se mueven al respirar
    pies_d, pies_t = [], []
    for lado in (-1, 1):
        az = giro + lado * math.pi / 2
        sep, abre = P["piernaSep"], P["piernaAbre"]
        _, _, z = proyectar(az, sep, 199)
        xf, yf, _ = proyectar(az, sep + abre + 3, 213)
        trozo = f'<ellipse class="mano" cx="{xf:.2f}" cy="{yf:.2f}" rx="6" ry="4.2"/>'
        (pies_d if z > 0 else pies_t).append(trozo)

    partes = [f'<ellipse cx="{CX}" cy="222" rx="{46 * (1 - 0.02 * a):.2f}" ry="6.5" '
              f'fill="#0f1320" fill-opacity="0.22" filter="url(#sombra)"/>',
              f'<g opacity="{op:.3f}">{"".join(pies_t)}</g>']

    cuerpo = [f'<g opacity="{op:.3f}"><g mask="url(#fuera)">{"".join(detras)}</g>'
              f'<path d="{GOTA}" fill="url(#cuerpo)"/></g>',
              # Doble contorno gris muy claro
              f'<g opacity="{op_contorno:.3f}">'
              f'<path d="{GOTA}" fill="none" stroke="#cdd3da" stroke-opacity="0.95" '
              f'stroke-width="2.2" stroke-linejoin="round"/>'
              f'<path d="{GOTA}" fill="none" stroke="#e3e7ec" stroke-opacity="0.8" '
              f'stroke-width="1.1" transform="translate(128 142) scale(0.93) translate(-128 -142)"/></g>',
              # Reflejo pequeño en el lateral izquierdo (la luz no gira con ella)
              f'<path d="{REFLEJO}" fill="#ffffff" '
              f'fill-opacity="{0.88 * op_reflejo:.3f}"/>']
    # Ojos: juntos, se acortan con la perspectiva. Radio algo menor que el del
    # cuerpo (convención de dibujo) para que la cara no se pegue al borde
    cuerpo.extend(ojos_svg(v, t, giro))
    cuerpo.append(f'<g opacity="{op:.3f}">{"".join(delante)}</g>')
    partes.append(f'<g transform="{respira}">{"".join(cuerpo)}</g>')
    partes.append(f'<g opacity="{op:.3f}">{"".join(pies_d)}</g>')
    return "".join(partes)


def hoja_svg(v, n):
    filas = math.ceil(n / COLS)
    w, h = COLS * TAM, filas * TAM
    celdas = []
    for i in range(n):
        ox, oy = (i % COLS) * TAM, (i // COLS) * TAM
        celdas.append(f'<g transform="translate({ox} {oy})">{fotograma(v, i / n)}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * ESCALA}" height="{h * ESCALA}" '
            f'viewBox="0 0 {w} {h}"><style>{ESTILO}</style><defs>{DEFS}</defs>'
            f'{"".join(celdas)}</svg>'), w * ESCALA, h * ESCALA


def renderizar(svg_path, png_path, w, h):
    subprocess.run([BRAVE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--default-background-color=00000000", f"--window-size={w},{h}",
                    f"--screenshot={png_path}", "file:///" + svg_path.replace("\\", "/")],
                   check=True, capture_output=True)


ALERTA = {"mano": (14, 8), "piernaSep": 16, "piernaAbre": 4.5}

def suave(x):
    """0..1 con aceleración y frenado suaves."""
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def tramo(t, t0, t1):
    return (t - t0) / (t1 - t0)


PARPADEO = {"parpadeo": True}
OJOS_ALERTA = {"ancho": 1.12, "alto": 1.22}
OJOS_DETERMINADA = {"parpado": (0.5, 0.1)}
OJOS_PREOCUPADA = {"parpado": (0.1, 0.5)}
OJOS_RECELOSA = {"alto": 0.6, "dy": 1, "parpado": (0.15, 0.15)}


def ojos_entrada_prolongado(t):
    """Mira a la cámara -> párpados a media altura -> ojos cerrados."""
    p = 0.38 * suave(tramo(t, 0.40, 0.55)) + 0.54 * suave(tramo(t, 0.70, 0.88))
    return {"mirada": -28 * suave(tramo(t, 0.05, 0.25)), "parpado": (p, p), "cerrados": t >= 0.9}


def ojos_reaccion(t):
    """Abre de golpe en alerta, se relaja y parpadea hasta la expresión seria."""
    if t < 0.04:
        return {"cerrados": True}
    k = 1 - suave(tramo(t, 0.50, 0.70))
    return {"ancho": 1 + 0.12 * k, "alto": 1 + 0.22 * k, "cerrados": 0.78 <= t < 0.84}


def sobresalto(t):
    return 1.6 * math.exp(-((t - 0.07) / 0.05) ** 2)


def animacion(id_, nombre, descripcion, nota, **v):
    return {"nombre": nombre, "descripcion": descripcion,
            "variantes": [dict(id=id_, nombre=nombre, nota=nota, **v)]}


PROPUESTAS = [
    animacion("reposo", "Reposo", "Idle normal. Expresión: seria con parpadeo.",
              "Respira dos veces cada 3,2 s y parpadea una vez.",
              ciclo=3200, respiraciones=2, ojos=PARPADEO),
    animacion("reposo_prolongado_entrada", "Reposo prolongado · entrada",
              "Cuando lleva mucho tiempo quieta (se reproduce una vez): mira a la cámara, "
              "baja los párpados a media altura y cierra los ojos.",
              "4 s. Al terminar enlaza con el bucle de reposo prolongado.",
              ciclo=4000, respiraciones=2, ojos_t=ojos_entrada_prolongado, bucle=False),
    animacion("reposo_prolongado", "Reposo prolongado · bucle",
              "Ojos cerrados y ligero pulso de transparencia, como si respirara.",
              "El cuerpo baja hasta el 75 % de opacidad y vuelve, en 2 s.",
              ciclo=2000, pulso=0.25, ojos={"cerrados": True}),
    animacion("reaccion_movimiento", "Reacción al movimiento",
              "Cuando detecta movimiento (se reproduce una vez): alerta y luego seria con parpadeo.",
              "Abre los ojos de golpe con un pequeño sobresalto, los relaja y parpadea. 1,8 s.",
              ciclo=1800, respiraciones=1, ojos_t=ojos_reaccion, extra_a=sobresalto, bucle=False),
    animacion("reposo_alerta", "Reposo en alerta · ojos de alerta",
              "Zona peligrosa: respiración corta, manos altas, pies abiertos y ojos de alerta.",
              "Para peligro moderado o al recuperarse de un golpe. Parpadea una vez por ciclo.",
              ciclo=2500, respiraciones=2, amplitud=0.018, manos=1.2, postura=ALERTA,
              ojos=dict(OJOS_ALERTA, **PARPADEO)),
    animacion("reposo_determinada", "Reposo en alerta · determinada",
              "Misma postura de alerta, con la mirada determinada.",
              "Para enemigos o zonas muy peligrosas: se planta y no retrocede.",
              ciclo=2500, respiraciones=2, amplitud=0.018, manos=1.2, postura=ALERTA,
              ojos=dict(OJOS_DETERMINADA, **PARPADEO)),
    animacion("reposo_preocupada", "Reposo · preocupada",
              "Idle normal con la mirada preocupada, según el contexto de la historia.",
              "Su lado sensible, sin dramatismo.",
              ciclo=3200, respiraciones=2, ojos=dict(OJOS_PREOCUPADA, **PARPADEO)),
    animacion("reposo_recelosa", "Reposo · recelosa",
              "Idle normal con los ojos entrecerrados, según el contexto de la historia.",
              "Desconfía o se concentra.",
              ciclo=3200, respiraciones=2, ojos=dict(OJOS_RECELOSA, **PARPADEO)),
]


def main():
    base = sys.argv[1]
    rev = os.path.join(base, "revision")
    carpeta = os.path.join(rev, "sprites")
    fuentes = os.path.join(base, "fuentes")
    os.makedirs(carpeta, exist_ok=True)
    os.makedirs(fuentes, exist_ok=True)
    animaciones = []
    for anim in PROPUESTAS:
        variantes = []
        for v in anim["variantes"]:
            n = max(8, round(v["ciclo"] / MS_FOTOGRAMA))
            svg, w, h = hoja_svg(v, n)
            svg_path = os.path.join(fuentes, v["id"] + ".svg")
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(svg)
            renderizar(svg_path, os.path.join(carpeta, v["id"] + ".png"), w, h)
            variantes.append({"id": v["id"], "nombre": v["nombre"], "nota": v["nota"],
                              "hoja": f"sprites/{v['id']}.png", "cols": COLS, "n": n,
                              "duraciones": [round(v["ciclo"] / n)] * n,
                              "bucle": v.get("bucle", True)})
            print("ok", v["id"], n, "fotogramas")
        animaciones.append({"nombre": anim["nombre"], "descripcion": anim["descripcion"],
                            "multiple": anim.get("multiple", False), "variantes": variantes})
    with open(os.path.join(rev, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"tam": TAM, "escalaFuente": ESCALA, "suave": True,
                   "animaciones": animaciones}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
