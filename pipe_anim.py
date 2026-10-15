"""Animacion Manim: prompts de escena, validacion AST, render y ensamblado."""
import ast
import json
import re
import subprocess
import sys
import time
from pathlib import Path

from pipe_core import (BASE, HERE, _audio_path, _es_fallo_quota, _guardar_log,
                       _probe_duration, _SENT_SPLIT, fmt_eta, run, Progreso)
from pipe_storyboard import _campo, _narracion_job, _parse_storyboard
from pipe_tts import _ids_con_archivo, fmt_mmss, segmento_de_escena

RIG_API = """API del rig (zenn_rig.py, ya importado con *). USO OBLIGATORIO:
los personajes y objetos se crean SOLO con estas funciones. PROHIBIDO
construir personajes con Circle/Line sueltos o redefinir el rig.

PERSONAJE PRINCIPAL — "EL PORQUÉ" (protagonista en TODAS las escenas):
  protagonista(pos, playera, altura=3.0, expresion, pose) -> el conductor:
  cabezón de ojos grandes, playera de color, extremidades negras simples.
  LAYOUT: con banda_titulo()/titulo_seguro() arriba, el protagonista va
  ABAJO (pos con y<=-1.2, altura<=2.6; p. ej. pos=DOWN*1.2+LEFT*3.5);
  sin banda puede ir al centro (pos=ORIGIN, altura=3.0).
  playera: "naranja" (default/intro), "azul", "verde", "roja", "amarilla",
    "rosa", "teal", "morada", "negra", "blanca" (strings en español;
    también valen las constantes PLAYERA_NARANJA/AZUL/...).
    Cambia el color por bloque temático.
  expresion: feliz, alegria_pura, triste, enojado, sorpresa,
    mente_explotada, pensando, confundido, miedo, decidido, euforico,
    cansado, dormido, nervioso, sarcastico.
  pose: de_pie, senalando, brazos_cruzados, caminando, corriendo.
  cambiar_cara(prota, tipo) -> cambia la expresión en el acto (para animar).
  version_prota(n, pos) -> atajo: 1=intro naranja, 2=presentación azul,
    4=curiosidad roja, 5=pregunta amarilla, 6=transmisión verde señalando,
    7=detalles rosa, 8=final teal.
- Monigote clásico (secundario): stick_idle(pos, height=2.2, color=INK),
  stick_walk(fig, target, run_time=2.0), stick_run(fig, target, run_time=1.5),
  stick_point(fig, target), stick_think(fig, texto), stick_group(n, ...),
  expresion(fig, tipo): "normal", "feliz", "preocupado", "sorpresa",
  "triste", "miedo", "dormido"
- title_card(texto, color) -> tarjeta de capítulo a pantalla completa
- callout(texto, color, pos) -> dato destacado COMPACTO (se auto-ajusta;
  nunca sale del encuadre aunque pidas pos lejana: el rig lo recorta).
  pos p. ej. pos=RIGHT*3.4+UP*1, SIEMPRE al lado contrario del
  protagonista, NUNCA encima. PROHIBIDO font_size>72 (gigante = rechazo).
  / arrow(start, end) / red_accent(obj)
- split_screen(izq, der) / clock_montage(radius)
- Fondos: fondo(color) pantalla completa; estrellas(n); luna(pos, radio, bg)
- Props clásicos: sol(), calendario(pos), pagina_calendario(), reloj_pared(),
  pastel(pos), red_seguridad(), caja(etiqueta, pos), camino(), casa(pos),
  oficina(pos), digitos(pos), adn(pos, escala), grafica_barras(pos, valores,
  ancho, etiquetas), lupa(pos, escala), fondo_papel() [fondo crema cálido
  opcional: self.add(fondo_papel()) al inicio]
- Props con color (v2): perro(pos, color, escala), gato(pos, color, escala),
  dino(pos, color, escala), fuego(pos, escala), lapida(texto, pos),
  curva(pos, ancho, alto) [gráfica con punto rojo], planeta(pos, radio, color),
  casco_vikingo(pos, escala), hueso(pos, escala), vela(pos, escala),
  moneda_dorada(texto, pos, radio)
- Texto SEGURO (v3, auto-ajustado: nunca se sale del encuadre):
  banda_titulo(texto, color) -> banda superior con texto que se encoge solo;
  titulo_seguro(texto, color) -> título auto-escalado;
  etiqueta(texto, (x, y)) -> etiqueta pequeña (nunca baja a subtítulos);
  tarjeta_canal() -> tarjeta de apertura/cierre "EL PORQUÉ"
- Personajes ilustrados (v3): personaje(pos, cuerpo, altura, expresion_tipo)
  [cuerpo de color + cara: normal/feliz/preocupado/sorpresa/triste/miedo],
  pez(pos, color, escala), matraz(pos, escala, liquido), ojo_grande(pos, escala)
- Paleta: MOSTAZA, CORAL, AZUL_MARINO, CREMA, además de WHITE, INK, YELLOW,
  ORANGE, RED, TEAL. Fondo blanco por defecto; para noche/espacio:
  self.add(fondo(INK)) al inicio y monigotes color=WHITE.
- Manim estándar: Scene, Text, FadeIn, FadeOut, Create, Write, Transform,
  LEFT/RIGHT/UP/DOWN/ORIGIN, self.play(), self.wait()
PROHIBIDO: Tex/MathTex (no hay LaTeX), archivos, internet, otros módulos."""

SCENE_PROMPT = """Eres programador de animación Manim para un canal de divulgación estilo Zenn.
Escribe el archivo Python COMPLETO de UNA escena. Debe contener EXACTAMENTE:
from manim import *
from zenn_rig import *

class {cls}(Scene):
    def construct(self):
        ...

{rig}

Escena {sid}:
VOZ (narración; en pantalla solo callouts cortos): {voz}
VISUAL: {visual}
Duración objetivo: ~{secs} segundos (suma de run_time + waits).

Reglas de calidad visual:
- 2-4 elementos por escena (monigote + props), no un solo objeto flotando.
- Usa expresion() acorde a la emoción de la narración.
- Usa props CON COLOR y, si la escena es nocturna/espacial, fondo oscuro.
- Movimientos simples pero presentes: entradas (FadeIn/Create), caminar,
  señalar, transformaciones. Nada de pantalla estática todo el tiempo.
- Código COMPACTO (~40-70 líneas): nada de comentarios largos.

COMPOSICIÓN — OBLIGATORIO (la cámara mide 14.22 x 8: x de -7.1 a 7.1,
y de -4 a 4):
- ZONA DE SUBTÍTULOS: entre y=-2.4 y y=-4 van los subtítulos quemados.
  NUNCA pongas texto, títulos, bandas ni elementos importantes ahí.
- Títulos y bandas: usa SIEMPRE banda_titulo() o titulo_seguro()
  (se auto-ajustan; PROHIBIDO Text() gigante manual que se salga).
- UNA SOLA banda/título/callout por escena: PROHIBIDO llamar más de una
  vez en la misma escena a banda_titulo(), titulo_seguro(), title_card(),
  tarjeta_canal() o callout() (se enciman y tapan todo). Si la escena
  necesita dos ideas, usa split_screen() o etiquetas pequeñas.
- LAYOUT CON BANDA (obligatorio): si la escena lleva banda_titulo() o
  titulo_seguro() ARRIBA, el protagonista va ABAJO: pos con y<=-1.2 y
  altura<=2.6 (p. ej. pos=DOWN*1.2+LEFT*3.5 o pos=DOWN*1.2+RIGHT*3.5).
  La cabeza del protagonista NUNCA entra a la zona y>1.7: la banda la
  taparía (es el fallo más repetido en producción y se rechaza por
  validación).
- Sin banda: el protagonista puede ir al centro (pos=ORIGIN, altura=3.0).
- PROHIBIDO Text() con font_size mayor a 60: para títulos usa
  banda_titulo()/titulo_seguro(); para datos destacados, callout();
  para etiquetas, etiqueta(). El texto crudo grande se corta en los
  bordes (también se rechaza por validación).
- Etiquetas: usa etiqueta(texto, (x, y)) con y >= -1.9.
- callout(): dato compacto con pos= (p. ej. pos=RIGHT*3.4+UP*1), al lado
  CONTRARIO del protagonista; NUNCA encima de él. El rig impide que salga
  del encuadre, pero el validador RECHAZA el solape con el protagonista:
  si el prota va a la izquierda, el callout va a la derecha y viceversa.
- SEPARACIÓN: un elemento grande por zona (izquierda/derecha,
  arriba/abajo); deja >=1.5 unidades entre elementos; NADA puede tapar
  a otro: ni bocadillos sobre texto, ni figuras sobre etiquetas,
  ni círculos/flechas sobre subtítulos.
- Todo el texto en pantalla entre y=-2.2 y y=3.4.
Devuelve SOLO el código, sin explicaciones ni ```."""

FIX_PROMPT = """Este código Manim falló al renderizar. Corrígelo y devuelve el archivo COMPLETO, solo código.
Respeta al carácter las firmas REALES del rig: si un parámetro no aparece ahí, no existe (inventarlo vuelve a fallar).

{rig}

ERROR:
{error}

CÓDIGO:
{code}"""


def _rig_api_text(rig_file=None):
    """RIG_API + firmas reales del rig, para que el modelo no invente kwargs."""
    sigs = []
    try:
        p = Path(rig_file) if rig_file else None
        if p and p.exists():
            import ast
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                        and not node.name.startswith("_"):
                    try:
                        sigs.append(f"{node.name}({ast.unparse(node.args)})")
                    except Exception:
                        pass
    except Exception:
        sigs = []
    if not sigs:
        return RIG_API
    bloque = ("Firmas REALES del rig (respétalas; NO inventes parámetros):\n"
              + "\n".join("- " + s for s in sigs) + "\n\n")
    return bloque + RIG_API


def _strip_fences(text):
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-z]*\n", "", t)
        t = re.sub(r"\n```\s*$", "", t)
    return t.strip()


# --- evaluador restringido de coordenadas Manim (para el chequeo de layout) ---
_MANIM_VEC = {
    "ORIGIN": (0.0, 0.0, 0.0),
    "LEFT": (-1.0, 0.0, 0.0), "RIGHT": (1.0, 0.0, 0.0),
    "UP": (0.0, 1.0, 0.0), "DOWN": (0.0, -1.0, 0.0),
}


def _eval_vec(node):
    """Evalúa expresiones simples de coordenadas Manim.

    Devuelve ("vec", (x, y)) o ("num", v) o None si no se puede resolver.
    Soporta: ORIGIN/LEFT/RIGHT/UP/DOWN, números, tuplas, np.array([...]),
    +, -, *, y negación. Cualquier otra cosa → None (no se puede probar).
    """
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return ("num", float(node.value))
        return None
    if isinstance(node, ast.Name):
        v = _MANIM_VEC.get(node.id)
        return ("vec", (v[0], v[1])) if v else None
    if isinstance(node, (ast.Tuple, ast.List)) and len(node.elts) >= 2:
        x, y = _eval_vec(node.elts[0]), _eval_vec(node.elts[1])
        if x and x[0] == "num" and y and y[0] == "num":
            return ("vec", (x[1], y[1]))
        return None
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        v = _eval_vec(node.operand)
        if v and v[0] == "vec":
            return ("vec", (-v[1][0], -v[1][1]))
        if v and v[0] == "num":
            return ("num", -v[1])
        return None
    if isinstance(node, ast.BinOp):
        l, r = _eval_vec(node.left), _eval_vec(node.right)
        if not l or not r:
            return None
        if isinstance(node.op, ast.Add) and l[0] == "vec" and r[0] == "vec":
            return ("vec", (l[1][0] + r[1][0], l[1][1] + r[1][1]))
        if isinstance(node.op, ast.Sub) and l[0] == "vec" and r[0] == "vec":
            return ("vec", (l[1][0] - r[1][0], l[1][1] - r[1][1]))
        if isinstance(node.op, ast.Mult):
            if l[0] == "vec" and r[0] == "num":
                return ("vec", (l[1][0] * r[1], l[1][1] * r[1]))
            if l[0] == "num" and r[0] == "vec":
                return ("vec", (l[1] * r[1][0], l[1] * r[1][1]))
        return None
    if isinstance(node, ast.Call):
        f = node.func
        if (isinstance(f, ast.Attribute) and f.attr == "array"
                and isinstance(f.value, ast.Name) and f.value.id == "np"
                and node.args):
            return _eval_vec(node.args[0])
        return None
    return None


def _kw(call, nombre, posicional=None, default=None):
    for kw in call.keywords:
        if kw.arg == nombre:
            return kw.value
    if posicional is not None and len(call.args) > posicional:
        return call.args[posicional]
    return default


def _num(node, default):
    v = _eval_vec(node)
    if v and v[0] == "num":
        return v[1]
    return default


# Helpers de texto cuyo posicionamiento se valida contra el protagonista.
_TEXTO_POS = {"callout", "etiqueta"}
# Tamaños por defecto del rig (scripts/zenn_rig.py)
_TXT_DEF = {"callout": {"font_size": 60, "ancho_max": 7.0, "pad": 0.7},
            "etiqueta": {"font_size": 40, "ancho_max": 5.5, "pad": 0.0}}


def _nombre_llamada(node):
    f = node.func
    if isinstance(f, ast.Attribute):
        return f.attr
    if isinstance(f, ast.Name):
        return f.id
    return ""


def _texto_de(call, helper):
    """Texto del helper (arg 0 o kwarg text/texto)."""
    if call.args:
        try:
            return str(ast.literal_eval(call.args[0]))
        except Exception:
            return ""
    for kw in call.keywords:
        if kw.arg in ("text", "texto"):
            try:
                return str(ast.literal_eval(kw.value))
            except Exception:
                return ""
    return ""


def _cajas_texto(tree):
    """Cajas de callout()/etiqueta(): (centro, w, h) finales.

    Sigue .move_to()/.shift() encadenados (`x = callout(...).move_to(E)`)
    o en sentencias separadas (`x.move_to(E)`). Si la posición no es
    evaluable, se omite (el rig la encuadra en runtime de todos modos).
    """
    nodos = sorted(ast.walk(tree),
                   key=lambda n: (getattr(n, "lineno", 0),
                                  getattr(n, "col_offset", 0)))
    # var -> [helper, call, [(mov, expr)]] en orden de aparición
    vars_txt = {}
    for node in nodos:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            v, moves = node.value, []
            while isinstance(v, ast.Call) and isinstance(v.func, ast.Attribute) \
                    and v.func.attr in ("move_to", "shift"):
                moves.append((v.func.attr,
                              v.args[0] if v.args else None))
                v = v.func.value
            if isinstance(v, ast.Call) and _nombre_llamada(v) in _TEXTO_POS:
                vars_txt[node.targets[0].id] = [_nombre_llamada(v), v,
                                                list(reversed(moves))]
    for node in nodos:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            c, f = node.value, node.value.func
            if isinstance(f, ast.Attribute) and f.attr in ("move_to", "shift") \
                    and isinstance(f.value, ast.Name) \
                    and f.value.id in vars_txt:
                vars_txt[f.value.id][2].append(
                    (f.attr, c.args[0] if c.args else None))
    cajas = []
    for var, (helper, call, moves) in vars_txt.items():
        d = _TXT_DEF[helper]
        fs = _num(_kw(call, "font_size", default=None), d["font_size"])
        am = _num(_kw(call, "ancho_max", default=None), d["ancho_max"])
        texto = _texto_de(call, helper)
        # centro base: kwarg pos= (callout) o arg 1 pos (etiqueta)
        base = _kw(call, "pos", default=None)
        if base is None and helper == "etiqueta" and len(call.args) >= 2:
            base = call.args[1]
        centro = (0.0, 0.0)
        if base is not None:
            v = _eval_vec(base)
            if v and v[0] == "vec":
                centro = v[1]
            else:
                continue  # no evaluable: el rig lo encuadra en runtime
        for mov, expr in moves:
            if expr is None:
                continue
            v = _eval_vec(expr)
            if not v or v[0] != "vec":
                centro = None
                break
            if mov == "move_to":
                centro = v[1]
            else:
                centro = (centro[0] + v[1][0], centro[1] + v[1][1])
        if centro is None:
            continue
        w = min(am, max(1.0, len(texto) * fs * 0.009)) + d["pad"]
        h = fs * 0.02 + d["pad"]
        cajas.append((helper, centro, w, h))
    return cajas


def _cajas_prota(tree):
    """Cajas del protagonista: (centro, w, h) desde pos/altura."""
    cajas = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        nm = _nombre_llamada(node)
        if nm == "protagonista":
            pos = _kw(node, "pos", posicional=0, default=None)
            alt = _num(_kw(node, "altura", posicional=2, default=None), 3.0)
        elif nm == "version_prota":
            pos = _kw(node, "pos", posicional=1, default=None)
            alt = _num(_kw(node, "altura", posicional=2, default=None), 3.0)
        else:
            continue
        if pos is None:
            continue
        v = _eval_vec(pos)
        if not v or v[0] != "vec":
            continue
        px, py = v[1]
        cajas.append(((px, py + alt / 2), 0.5 * alt, alt))
    return cajas


def _checar_solape_texto(tree):
    """Ningún callout/etiqueta puede tapar al protagonista.

    El rig ya impide que salgan del encuadre (_Seguro); aquí se valida
    que no se encimen con el conductor de la escena.
    """
    protas = _cajas_prota(tree)
    if not protas:
        return ""
    for helper, (cx, cy), w, h in _cajas_texto(tree):
        for (px, py), pw, ph in protas:
            if abs(cx - px) < (w + pw) / 2 and abs(cy - py) < (h + ph) / 2:
                return (f"El {helper}() tapa al protagonista (centros a "
                        f"{abs(cx - px):.1f}/{abs(cy - py):.1f} unidades). "
                        f"Pon el {helper} al lado CONTRARIO del protagonista "
                        f"con pos= (p. ej. prota a la izquierda → "
                        f"{helper} con pos=RIGHT*3.4+UP*1), nunca encima.")
    return ""


def _checar_banda_vs_prota(tree):
    """La banda superior no puede tapar la cabeza del protagonista.

    Si hay banda_titulo()/titulo_seguro() y el protagonista queda con la
    cabeza dentro de la zona de la banda → error (cuenta como intento y se
    autorrepara). Solo se chequea cuando pos/altura son evaluables.
    """
    bandas, protas = [], []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        name = f.attr if isinstance(f, ast.Attribute) else (
            f.id if isinstance(f, ast.Name) else "")
        if name in ("banda_titulo", "titulo_seguro"):
            y = _num(_kw(node, "y", default=None), 2.55)
            bandas.append(y - 0.85)  # borde inferior de la banda
        elif name == "protagonista":
            pos = _kw(node, "pos", posicional=0, default=None)
            alt = _num(_kw(node, "altura", posicional=2, default=None), 3.0)
            protas.append((pos, alt))
        elif name == "version_prota":
            pos = _kw(node, "pos", posicional=1, default=None)
            alt = _num(_kw(node, "altura", posicional=2, default=None), 3.0)
            protas.append((pos, alt))
    if not bandas or not protas:
        return ""
    for pos_node, alt in protas:
        if pos_node is None:
            continue
        v = _eval_vec(pos_node)
        if not v or v[0] != "vec":
            continue  # no evaluable: no se puede probar, se deja pasar
        cabeza_top = v[1][1] + alt - 0.02  # como en el rig
        for borde in bandas:
            if cabeza_top > borde:
                return (f"La banda tapa la cabeza del protagonista "
                        f"(cabeza hasta y={cabeza_top:.2f}, la banda baja "
                        f"hasta y={borde:.2f}). Con banda arriba, el "
                        "protagonista va ABAJO: pos con y<=-1.2 y altura<=2.6 "
                        "(p. ej. pos=DOWN*1.2+LEFT*3.5, altura=2.6).")
    return ""


# Llamadas que pintan banda/título grande: solo UNA por escena (si no,
# se enciman, como pasó en producción).
_BANDAS = {"banda_titulo", "titulo_seguro", "title_card", "tarjeta_canal",
           "callout"}


def _validar_escena(code, cls):
    """Garantías por construcción del código de UNA escena.

    1) Usa el rig y define la clase pedida.
    2) El protagonista aparece (obligatorio en todas las escenas).
    3) UNA sola banda/título/callout (no se pueden encimar).
    Devuelve "" si pasa, o el mensaje de error (cuenta como intento y
    dispara la autorreparación con FIX_PROMPT).
    """
    if "zenn_rig" not in code or f"class {cls}" not in code:
        return (f"El código no usa el rig (falta 'from zenn_rig import *' o "
                f"la clase {cls}). Usa SOLO el rig para monigotes y props; "
                "no los construyas con Circle/Line sueltos.")
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"Error de sintaxis en el código: {e}"
    llamadas = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Attribute):
                llamadas.append(f.attr)
            elif isinstance(f, ast.Name):
                llamadas.append(f.id)
    if not any(n in ("protagonista", "version_prota") for n in llamadas):
        return ("Falta el protagonista: TODA escena debe incluir "
                "protagonista(...) o version_prota(n, ...) como conductor. "
                "Sin excepción.")
    bandas = [n for n in llamadas if n in _BANDAS]
    if len(bandas) > 1:
        return (f"La escena llama {len(bandas)} veces a banda/título "
                f"({', '.join(bandas)}): solo se permite UNA por escena "
                "porque se enciman. Quita las demás o usa etiqueta() para "
                "ideas secundarias.")
    # Layout: la banda no puede tapar la cabeza del protagonista.
    err_l = _checar_banda_vs_prota(tree)
    if err_l:
        return err_l
    # Layout: ningún callout/etiqueta puede tapar al protagonista.
    err_s = _checar_solape_texto(tree)
    if err_s:
        return err_s
    # Text() crudo gigante = texto cortado en bordes. Para títulos usar el
    # rig (banda_titulo/titulo_seguro/callout), que se auto-ajusta.
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            nm = f.attr if isinstance(f, ast.Attribute) else (
                f.id if isinstance(f, ast.Name) else "")
            if nm == "Text":
                fs = _num(_kw(node, "font_size", default=None), 48)
                if fs > 60:
                    return (f"Text() con font_size={fs:.0f} se sale de la "
                            "pantalla y se corta en los bordes. PROHIBIDO "
                            "font_size>60: usa banda_titulo(), "
                            "titulo_seguro(), callout() o etiqueta(), que se "
                            "auto-ajustan solos.")
            elif nm in ("callout", "etiqueta", "banda_titulo",
                        "titulo_seguro", "title_card"):
                fs = _num(_kw(node, "font_size", default=None), 0)
                if fs > 72:
                    return (f"{nm}() con font_size={fs:.0f} produce un "
                            "elemento gigante que tapa al protagonista. "
                            "PROHIBIDO font_size>72 en helpers de texto: usa "
                            "el tamaño por defecto (callout=60, etiqueta=40).")
    return ""


def _rig_source():
    for c in (HERE / "scripts" / "zenn_rig.py", BASE / "scripts" / "zenn_rig.py",
              BASE / "panel" / "scripts" / "zenn_rig.py"):
        if c.exists():
            return c
    return None


def _generar_y_renderizar_escena(generate_fn, sdir, media, vdir, job, sc,
                                 rig_text, solo_render=False):
    """Genera (LLM) + valida + renderiza UNA escena, con autorreparación.

    solo_render=True: no llama al LLM (cero tokens); re-renderiza el
    scripts/{sid}.py que ya existe.
    Devuelve (ok: bool, err: str, es_quota: bool).
    """
    sid, cls = sc["id"], sc["id"].upper()
    out = vdir / f"{sid}.mp4"
    f = sdir / f"{sid}.py"
    adur = _probe_duration(_audio_path(job, sid))
    secs = round(adur) if adur else max(4, len(sc["voz"].split()) // 3)
    code, err = None, ""
    intentos = 1 if solo_render else 3
    for intento in range(intentos):
        if solo_render:
            if not f.exists():
                return False, f"No hay código previo {sid}.py para re-renderizar.", False
            code = f.read_text(encoding="utf-8", errors="replace")
        else:
            try:
                if intento == 0:
                    prompt = SCENE_PROMPT.format(
                        cls=cls, rig=rig_text, sid=cls, voz=sc["voz"],
                        visual=sc["visual"] or sc["voz"][:80], secs=secs)
                    code, _ = generate_fn(
                        prompt, system="Eres programador experto en Manim. "
                                       "Devuelves solo código Python válido.")
                else:
                    fixed, _ = generate_fn(
                        FIX_PROMPT.format(error=err[-1500:], code=code,
                                          rig=rig_text),
                        system="Eres programador experto en Manim. "
                               "Devuelves solo código Python válido.")
                    code = fixed
            except Exception as e:
                err = str(e)
                break
        code = _strip_fences(code)
        # Validación por construcción: rig, protagonista y UNA sola banda.
        # No gastamos un render si no pasa; cuenta como intento.
        err = _validar_escena(code, cls)
        if err:
            continue
        f.write_text(code, encoding="utf-8")
        r = subprocess.run(
            [sys.executable, "-m", "manim", "render", "-qm",
             "--media_dir", str(media), "-o", sid, f.name, cls],
            cwd=str(sdir), capture_output=True, text=True, timeout=600)
        if r.returncode == 0:
            # Con -o <sid> el archivo final se llama <sid>.mp4
            # (ojo: partial_movie_files/ también contiene mp4s).
            cands = [q for q in media.glob(f"videos/**/{sid}.mp4")
                     if "partial_movie_files" not in q.parts]
            cands.sort(key=lambda q: q.stat().st_mtime)
            if cands:
                out.write_bytes(cands[-1].read_bytes())
                vdur = _probe_duration(out)
                aviso = ""
                if adur and vdur < 0.3 * adur:
                    aviso = (f" AVISO: el video dura {vdur:.1f}s pero el audio "
                             f"{adur:.1f}s — el ensamblado rellenará con imagen "
                             "congelada; considera regenerar la escena.")
                return True, (f"render OK ({vdur:.1f}s)." + aviso), False
            err = "manim terminó sin generar el mp4."
        else:
            err = (r.stdout or "")[-1200:] + (r.stderr or "")[-1200:]
    return False, err, _es_fallo_quota(err)


def run_animacion(generate_fn, p, job, progress=None):
    """El LLM genera el código Manim escena por escena y lo renderiza.

    progress(stage, done, total, detalle): callback de avance con ETA.
    Con backend groq se pausa 6s entre escenas (OTPM 1000).
    """
    if not generate_fn:
        return (False, "Necesita un backend LLM para generar el código de "
                       "escenas (Configuración).", [], None)
    chk = subprocess.run([sys.executable, "-c", "import manim"],
                         capture_output=True, text=True)
    if chk.returncode != 0:
        return (False, "Manim no está instalado en el entorno del panel. "
                       "Instálalo: pip install manim (ya viene en "
                       "requirements.txt; si usas INICIAR.bat, borra la "
                       "carpeta .venv y vuelve a correrlo).", [], None)
    rig = _rig_source()
    if not rig:
        return False, "No encuentro scripts/zenn_rig.py en el paquete.", [], None
    scenes = _parse_storyboard(job)
    if not scenes:
        return (False, "Sin escenas: genera primero el storyboard "
                       "(etapa 5) — de ahí salen VOZ y VISUAL por escena.",
                [], None)
    sdir = job / "scripts"
    sdir.mkdir(parents=True, exist_ok=True)
    (sdir / "zenn_rig.py").write_text(
        rig.read_text(encoding="utf-8"), encoding="utf-8")
    vdir = job / "video" / "scenes"
    vdir.mkdir(parents=True, exist_ok=True)
    media = job / "media"
    rig_text = _rig_api_text(sdir / "zenn_rig.py")

    prog = Progreso("animacion", progress)
    prog.start(len(scenes), "leyendo escenas")
    logs, arts, fallos = [], [], []
    fallos_quota = []  # escenas caídas por cuota del backend (no por código)
    # Estimación de consumo: el usuario debe dimensionar la cuota diaria.
    if getattr(generate_fn, "backend", "") == "groq":
        muestra = SCENE_PROMPT.format(cls="S00", rig=rig_text, sid="S00",
                                      voz="voz", visual="visual", secs=10)
        est = len(scenes) * (len(muestra) // 4 + 1200)
        logs.append(f"~{est // 1000}K tokens estimados en esta etapa "
                    f"({len(scenes)} escenas). Límite Groq gratuito: "
                    "200K/día. Si ya generaste guion+storyboard hoy, "
                    "reparte entre días o usa otro backend/Ollama local."
                    + (f" Con {len(scenes)} escenas NO cabe en un día: la "
                       "etapa se detendrá sola ante la cuota y reanudas "
                       "mañana (las hechas se omiten)." if est > 190000
                       else ""))
    done = 0
    paro_cuota, cls_cuota, det_cuota = False, "", ""
    for sc in scenes:
        sid, cls = sc["id"], sc["id"].upper()
        out = vdir / f"{sid}.mp4"
        if out.exists() and out.stat().st_size > 0:
            done += 1
            logs.append(f"{cls}: ya renderizada, se omite.")
            arts.append(str(out))
            prog.item(done, len(scenes), f"{cls} ya estaba")
            continue
        ok1, err, es_quota = _generar_y_renderizar_escena(
            generate_fn, sdir, media, vdir, job, sc, rig_text)
        if ok1:
            logs.append(f"{cls}: {err}")
            arts.append(str(out))
        else:
            fallos.append(cls)
            logs.append(f"{cls}: FALLO tras intentos: {err[-300:]}")
            if es_quota:
                # Cuota agotada: NO seguimos escena por escena fallando en
                # cascada ("brincando"). Se detiene la etapa aquí; reanudar
                # es un clic y las hechas se omiten solas.
                fallos_quota.append(cls)
                paro_cuota, cls_cuota = True, cls
                det_cuota = ("cuota DIARIA (TPD) agotada"
                             if any(w in err.lower()
                                    for w in ("tokens per day", "tpd"))
                             else "límite del backend (rate limit)")
                logs.append(f"⛔ {cls}: {det_cuota} — se DETIENE la etapa "
                            "aquí para no seguir fallando en cascada.")
                done += 1
                prog.item(done, len(scenes), f"{cls} cuota agotada")
                break
        done += 1
        prog.item(done, len(scenes),
                  f"{cls} lista" if ok1 else f"{cls} falló")
        if getattr(generate_fn, "backend", "") == "groq":
            time.sleep(6)  # OTPM 1000: no saturar tokens de salida/minuto
    # Estado real por escena: qué mp4 existe y qué huecos quedan.
    have = {p.stem.lower() for p in vdir.glob("*.mp4")
            if p.stat().st_size > 0}
    faltan = [s["id"].upper() for s in scenes if s["id"] not in have]
    n_have = len(scenes) - len(faltan)
    lista = ", ".join(faltan[:20]) + (f" …y {len(faltan) - 20} más"
                                      if len(faltan) > 20 else "")
    if paro_cuota:
        ok = False
        head = (f"⛔ Animación DETENIDA por cuota en {cls_cuota} "
                f"({det_cuota}): {n_have}/{len(scenes)} escenas con video. "
                f"Faltan {len(faltan)}: {lista}. No se siguió intentando "
                "para no quemar tiempo fallando en cascada."
                "\nOpciones: (1) reanuda cuando se resetee la cuota — las "
                "hechas se omiten solas; (2) cambia de backend en la barra "
                "lateral (Ollama local no tiene cuota); (3) si el proyecto "
                "tiene más escenas de las que caben en la cuota diaria, "
                "reparte la animación en 2 días.")
    elif not faltan:
        ok = True
        head = (f"Animación: {len(scenes)}/{len(scenes)} escenas "
                "renderizadas, sin huecos.")
    else:
        ok = False
        head = (f"Animación parcial: {n_have}/{len(scenes)} con video. "
                f"Faltan {len(faltan)}: {lista}. Reintenta la etapa o usa "
                "«Re-animar escena»; las ya hechas se omiten solas.")
    # Log completo persistente: cada ejecución queda en jobs/<id>/logs/
    # para revisarla después (el panel solo guarda la cola en la BD).
    logf = _guardar_log(job, "animacion", [head, "=" * 60] + logs)
    if logf:
        head += f"\n📄 Log completo de esta ejecución: {logf}"
    return ok, head + "\n" + "\n".join(logs[-25:]), arts, None


def run_reanimar_escena(generate_fn, p, job, sid, regen_code=True,
                        progress=None):
    """Re-anima UNA sola escena (p. ej. S07) sin tocar las demás.

    - Borra video/scenes/{sid}.mp4.
    - regen_code=True: borra también scripts/{sid}.py y regenera el código
      con el LLM (gasta tokens solo de esa escena), con validación y
      autorreparación.
    - regen_code=False: re-renderiza el scripts/{sid}.py existente
      (CERO tokens; útil si solo actualizaste el rig, p. ej. quitar mangas).
    Después hay que re-ejecutar la etapa 8 (Ensamblado) para regenerar el
    video final.
    """
    sid = sid.strip().lower()
    if not re.fullmatch(r"s\d+", sid):
        return False, f"Escena inválida: '{sid}'. Usa el formato S07.", [], None
    scenes = _parse_storyboard(job)
    sc = next((s for s in scenes if s["id"] == sid), None)
    if not sc:
        return (False, f"La escena {sid.upper()} no está en STORYBOARD.md.",
                [], None)
    rig = _rig_source()
    if not rig:
        return False, "No encuentro scripts/zenn_rig.py en el paquete.", [], None
    sdir = job / "scripts"
    sdir.mkdir(parents=True, exist_ok=True)
    (sdir / "zenn_rig.py").write_text(
        rig.read_text(encoding="utf-8"), encoding="utf-8")
    vdir = job / "video" / "scenes"
    vdir.mkdir(parents=True, exist_ok=True)
    media = job / "media"
    rig_text = _rig_api_text(sdir / "zenn_rig.py")
    out = vdir / f"{sid}.mp4"
    if out.exists():
        out.unlink()
    fpy = sdir / f"{sid}.py"
    if regen_code:
        if not generate_fn:
            return (False, "Regenerar código necesita un backend LLM "
                           "(Configuración) u Ollama local.", [], None)
        if fpy.exists():
            fpy.unlink()
    elif not fpy.exists():
        return (False, f"No hay código previo scripts/{sid}.py. Activa "
                       "'Regenerar código con LLM' o genera la escena en la "
                       "etapa 7.", [], None)
    prog = Progreso("reanimar", progress)
    prog.start(1, f"re-animando {sid.upper()}")
    ok1, err, es_quota = _generar_y_renderizar_escena(
        generate_fn, sdir, media, vdir, job, sc, rig_text,
        solo_render=not regen_code)
    prog.item(1, 1, f"{sid.upper()} lista" if ok1 else "falló")
    if ok1:
        log = (f"{sid.upper()}: {err}\n"
               "Ahora re-ejecuta la etapa 8 (Ensamblado) para regenerar el "
               "video final con esta escena corregida.")
        return True, log, [str(out)], None
    extra = ("\n⚠️ Fallo de CUOTA del backend, no de código." if es_quota else "")
    return False, f"{sid.upper()}: FALLO tras intentos: {err[-500:]}" + extra, [], None


# ---------- ensamblado: video + audio (audio manda) + SRT ----------
def _srt_time(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _wrap_card(txt, width=44):
    """Parte una tarjeta larga en 2 líneas equilibradas."""
    if len(txt) <= width:
        return txt
    words = txt.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width or not cur:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return "\n".join(lines[:2])


def _build_srt(items, durations):
    """SRT a nivel de frase: reparte la duración por caracteres."""
    cards, t = [], 0.0
    for it, dur in zip(items, durations):
        sents = [s.strip() for s in _SENT_SPLIT.split(it["text"]) if s.strip()]
        if not sents:
            sents = [it["text"]]
        total = sum(len(s) for s in sents) or 1
        cur = t
        for s in sents:
            d = dur * len(s) / total
            cards.append((cur, cur + d, _wrap_card(s)))
            cur += d
        t += dur
    out = []
    for i, (a, b, txt) in enumerate(cards, 1):
        out.append(f"{i}\n{_srt_time(a)} --> {_srt_time(b)}\n{txt}\n")
    return "\n".join(out)


def run_ensamblado(p, job, progress=None):
    """Une escenas + audios (el audio manda), SRT y versión subtitulada.

    progress(stage, done, total, detalle): callback de avance con ETA.
    """
    import shutil
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        return (False, "Falta ffmpeg/ffprobe en el PATH: instálalo para "
                       "poder ensamblar.", [], None)
    vdir = job / "video" / "scenes"
    archivos = sorted(vdir.glob("*.mp4")) if vdir.exists() else []
    if not archivos:
        return (False, "Sin videos de escenas: ejecuta antes la etapa 7 "
                       "(Animación).", [], None)
    # Garantía de duración: el video final debe cubrir TODAS las escenas del
    # storyboard. Si falta alguna, NO construimos un video corto en silencio:
    # fallamos con la lista para que se re-animen solo esas.
    sb_ids = [s["id"] for s in _parse_storyboard(job)]
    # v26 — pre-flight: si el storyboard cambió DESPUÉS del TTS (edición,
    # continuación, renumerado), vo.json y los audios ya no corresponden.
    # Fallar aquí con mensaje claro en vez del críptico "Falta el audio de Sxx".
    _vf = job / "vo.json"
    try:
        _vo_ids = {str(it.get("id", "")).lower()
                   for it in json.loads(_vf.read_text(encoding="utf-8"))} \
            if _vf.exists() else set()
    except Exception:
        _vo_ids = set()
    if sb_ids and set(sb_ids) != _vo_ids:
        _solo_sb = sorted(set(sb_ids) - _vo_ids)
        _solo_vo = sorted(_vo_ids - set(sb_ids))
        return (False,
                "El storyboard cambió después del TTS: vo.json ya no lo cubre. "
                + (f"En storyboard pero no en vo.json: "
                   f"{', '.join(s.upper() for s in _solo_sb)}. " if _solo_sb else "")
                + (f"En vo.json pero no en storyboard: "
                   f"{', '.join(s.upper() for s in _solo_vo)}. " if _solo_vo else "")
                + "Re-ejecuta la etapa 6 (sincroniza vo.json y genera "
                  "faltantes) y luego esta etapa.",
                [], None)
    if sb_ids:
        have = {sc.stem.lower() for sc in archivos if sc.stat().st_size > 0}
        faltan = [i.upper() for i in sb_ids if i not in have]
        if faltan:
            return (False,
                    "Faltan los videos de estas escenas: "
                    + ", ".join(faltan) + ". El video final quedaría más "
                    "corto que la narración. Re-ejecuta la etapa 7 "
                    "(Animación: omite solas las ya hechas) o usa "
                    "«Re-animar escena» para cada una, y luego repite esta "
                    "etapa.", [], None)
    # El storyboard manda: solo se ensamblan sus escenas, en su orden.
    # Los videos huérfanos (escenas borradas del storyboard) se ignoran con
    # aviso en vez de colarse al video final.
    scenes = ([vdir / f"{sid}.mp4" for sid in sb_ids
               if (vdir / f"{sid}.mp4").exists()] if sb_ids else archivos)
    huerfanos = [sc.stem.upper() for sc in archivos
                 if sc.stem.lower() not in sb_ids] if sb_ids else []
    prog = Progreso("ensamblado", progress)
    prog.start(len(scenes) + 2, "leyendo escenas")
    vo_file = job / "vo.json"
    items = (json.loads(vo_file.read_text(encoding="utf-8"))
             if vo_file.exists() else [])
    texts = {it["id"].lower(): it["text"] for it in items}
    segdir = job / "video" / "segments"
    segdir.mkdir(parents=True, exist_ok=True)
    segs, srt_items, srt_durs, logs = [], [], [], []
    for sc in scenes:
        sid = sc.stem.lower()
        au = _audio_path(job, sid)
        if not au.exists():
            # v26 — diagnóstico forense: si esto vuelve a pasar, el mensaje
            # debe decir EXACTAMENTE qué se buscó y qué hay en audio/.
            import difflib
            adir = job / "audio"
            presentes = sorted(p.name for p in adir.glob("*.mp3")) \
                if adir.exists() else []
            cerca = difflib.get_close_matches(au.name, presentes, n=3,
                                              cutoff=0.6)
            return (False,
                    f"Falta el audio de {sid.upper()} (etapa 6 · TTS).\n"
                    f"Ruta esperada: {au}\n"
                    f"La carpeta audio/ {'no existe' if not adir.exists() else f'existe y tiene {len(presentes)} mp3s'}."
                    + (f" Nombres parecidos: {', '.join(cerca)}." if cerca else
                       " Ningún nombre parecido.")
                    + (f" Primeros archivos: {', '.join(presentes[:6])}."
                       if presentes else "")
                    + "\nCausas posibles: el archivo se borró o se movió "
                      "después del TTS (antivirus, sincronización en la nube, "
                      "borrado manual); o el storyboard cambió después del TTS. "
                      "Si el archivo existe con otro nombre, renómbralo a "
                    f"{au.name}. Si está corrupto, bórralo y usa «🛠 Reparar "
                      "faltantes» con la escena en «Forzar».",
                    [], None)
        adur = _probe_duration(au)
        if adur <= 0:
            return False, f"No pude leer la duración de {au.name}.", [], None
        seg = segdir / f"{sid}.mp4"
        vf = (f"[0:v]tpad=stop_mode=clone:stop_duration=3600,"
              f"trim=duration={adur:.3f},setpts=PTS-STARTPTS,fps=30,"
              f"scale=1280:720,setsar=1[v]")
        r = subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", sc.name, "-i",
             f"../../audio/{sid}.mp3", "-filter_complex", vf,
             "-map", "[v]", "-map", "1:a", "-c:v", "libx264",
             "-preset", "medium", "-crf", "20", "-c:a", "aac",
             "-ar", "44100", f"../segments/{sid}.mp4"],
            cwd=str(vdir), capture_output=True, text=True, timeout=900)
        if r.returncode != 0:
            return False, f"ffmpeg falló en {sid}: {r.stderr[-400:]}", [], None
        segs.append(seg)
        srt_items.append({"id": sid, "text": texts.get(sid, "")})
        srt_durs.append(adur)
        vdur = _probe_duration(sc)
        aviso = (f" ⚠️ video {vdur:.1f}s < audio (relleno con imagen congelada)"
                 if vdur and vdur < 0.3 * adur else "")
        logs.append(f"{sid.upper()}: {adur:.1f}s{aviso}")
        prog.item(len(segs), len(scenes) + 2, f"{sid.upper()} unida")
    vout = job / "video"
    listf = segdir / "list.txt"
    listf.write_text("".join(f"file '{s.name}'\n" for s in segs),
                     encoding="utf-8")
    final = vout / "final.mp4"
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", "list.txt", "-c", "copy", "../final.mp4"],
        cwd=str(segdir), capture_output=True, text=True, timeout=900)
    if r.returncode != 0:
        return False, f"ffmpeg falló al concatenar: {r.stderr[-400:]}", [], None
    srt = _build_srt(srt_items, srt_durs)
    srt_path = vout / "final.srt"
    srt_path.write_text(srt, encoding="utf-8")
    prog.item(len(segs) + 1, len(segs) + 2, "subtítulos generados")
    sub = vout / "final_con_subtitulos.mp4"
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", "final.mp4", "-vf",
         "subtitles='final.srt':force_style='FontName=Gochi Hand,"
         "FontSize=17,Outline=2,Shadow=0,MarginV=26,Alignment=2'",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-c:a", "copy", "final_con_subtitulos.mp4"],
        cwd=str(vout), capture_output=True, text=True, timeout=1800)
    arts = [str(final), str(srt_path)]
    if r.returncode == 0:
        arts.append(str(sub))
    total = sum(srt_durs)
    prog.item(len(segs) + 2, len(segs) + 2, "video final listo")
    log = (f"Ensamblado OK: {len(segs)} escenas, {total:.0f}s totales "
           f"({total / 60:.1f} min).\n" + " · ".join(logs) +
           (f"\n⚠️ Videos huérfanos ignorados (no están en el storyboard): "
            f"{', '.join(huerfanos)}. Bórralos de video/scenes si ya no los "
            f"necesitas." if huerfanos else "") +
           ("\nVersión con subtítulos quemados generada."
            if r.returncode == 0 else
            "\nAVISO: no se pudo quemar subtítulos (revisa final.srt)."))
    logf = _guardar_log(job, "ensamblado", [log])
    if logf:
        log += f"\n📄 Log completo de esta ejecución: {logf}"
    return True, log, arts, None


# ---------- miniaturas (automático) ----------
