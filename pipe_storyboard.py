"""Storyboard y paquete de publicacion: parser de escenas, cobertura y continuacion."""
import json
import re
from pathlib import Path

from pipe_core import (BASE, MIN_PALABRAS_GUION, _audio_path,
                       _narracion_guion, _probe_duration, count_words,
                       estimate_minutes, find_script, job_dir_of, pget, run)



# ---------- storyboard (asistida) ----------
STORYBOARD_PROMPT = """Eres director de animación de un canal de divulgación con dibujos
minimalistas de colores vivos (estilo Zenn / Memorias de Pez).
Divide este guion en escenas numeradas. Por escena: el texto de narración LITERAL
y una descripción visual de 1 línea (qué personaje u objeto se ve, con qué
expresión y colores).

REGLA DE ORO — CORTAR, NO RESUMIR: tu trabajo es DIVIDIR el texto del
guion en bloques de 25-35 palabras, NO reescribirlo. Cada campo VOZ debe
ser un fragmento COPIADO TAL CUAL del guion, palabra por palabra, sin
cambiar ni una coma y sin saltarte ningún párrafo. Tú decides DÓNDE
CORTAR entre escenas; el texto se queda intacto. Si resumes o parafraseas,
la etapa se RECHAZA automáticamente (se exige 90% de cobertura palabra
por palabra y se cuenta).

REGLAS:
- RITMO POR DEFECTO: escenas CORTAS de 8-12 segundos (~25-35 palabras de VOZ
  por escena). Más cortes = más dinamismo = más retención. Parte el guion en
  TANTAS escenas como necesites (un video de 10 minutos → 50-60 escenas).
  PROHIBIDO meter 3 o más frases en una sola escena si puedes partirla en dos.
- PROTAGONISTA EN TODAS: el personaje principal (protagonista) aparece en
  cada escena como conductor. Varía su playera por bloque temático
  (naranja=intro, azul=presentación, verde=transmisión, roja=curiosidad,
  amarilla=pregunta, rosa=detalles, teal=cierre) y su expresión según la
  emoción de la narración.
- La PRIMERA escena es la bienvenida: tarjeta_canal() + el saludo del guion.
- La ÚLTIMA escena es la despedida del guion (tono cálido, cierre del canal).
- Cada escena: 2-4 elementos, nada encimado, nada cortado por los bordes,
  nada de texto en la franja inferior (ahí van los subtítulos).

Formato EXACTO por escena:
### S01
VOZ: <texto literal del guion>
VISUAL: <descripción>

GUION:
{script}
"""


def _partir_guion(script, max_palabras=650):
    """Parte el guion en trozos de ~max_palabras sin cortar párrafos.

    Un storyboard completo de un guion largo no cabe en el límite de
    salida de los modelos gratis (Groq: 1000 tokens duros): el modelo se
    corta a la mitad y el video sale truncado. Por partes, cada trozo sí
    cabe.
    """
    paras = [pp for pp in re.split(r"\n\s*\n", script) if pp.strip()]
    # Párrafo gigante sin saltos: córtalo por frases para que sí se parta.
    trozos = []
    for pp in paras:
        if len(pp.split()) > max_palabras:
            frases = re.split(r"(?<=[.!?…])\s+", pp)
            ac, cw = [], 0
            for fr in frases:
                w = len(fr.split())
                if cw + w > max_palabras and ac:
                    trozos.append(" ".join(ac))
                    ac, cw = [], 0
                ac.append(fr)
                cw += w
            if ac:
                trozos.append(" ".join(ac))
        else:
            trozos.append(pp)
    partes, actual, cuenta = [], [], 0
    for par in trozos:
        w = len(par.split())
        if cuenta + w > max_palabras and actual:
            partes.append("\n\n".join(actual))
            actual, cuenta = [], 0
        actual.append(par)
        cuenta += w
    if actual:
        partes.append("\n\n".join(actual))
    return partes


def _renumerar_desde(text, desde):
    """Si el modelo reinició la numeración en S01, la recorre desde `desde`.

    Mapea en orden de aparición: primera escena encontrada -> S(desde).
    """
    nums = [int(m.group(1)) for m in re.finditer(r"### S(\d+)", text)]
    if not nums or nums[0] == desde:
        return text
    vistos = []
    for nn in nums:
        if nn not in vistos:
            vistos.append(nn)
    mapa = {old: desde + i for i, old in enumerate(vistos)}
    return re.sub(r"### S(\d+)",
                  lambda m: f"### S{mapa[int(m.group(1))]:02d}", text)


def _bloques_escena(text):
    """Divide el storyboard en bloques por escena (cada uno empieza con
    ### Snn)."""
    return [m.group(0) for m in
            re.finditer(r"(?m)^###\s*S\d+.*?(?=^###\s*S\d+|\Z)", text, re.S)]


def _valor_campo_linea(linea, nombre):
    """Si `linea` es un marcador VOZ:/VISUAL:, devuelve su valor crudo.

    v28: matcher tolerante (sustituye la regex monolítica case-sensitive de
    `_pat_campo`, que solo conocía 6 variantes y dejaba fuera formatos
    reales de los modelos). Gramática aceptada, insensible a
    mayúsculas/minúsculas:

        [viñeta/cita] [envoltorio] NOMBRE [envoltorio] : valor

    El envoltorio (`*`, `**`, `[`, `]`) puede ir antes o después del nombre
    y los dos puntos pueden ir dentro o fuera del bold. Cubre:
      VOZ: / **VOZ:** / **[VOZ]**: / **[VOZ:** / **[VOZ: / [VOZ]: /
      **VOZ**: / *VOZ:* / ***VOZ***: / VOZ : / Voz: / - VOZ: / > VOZ:
    (igual para VISUAL). Devuelve None si la línea no es un marcador.
    """
    m = re.match(rf"(?i)^[\s>\-–•\*\[\]]*{nombre}[\s\*\[\]]*:(?:\*+)?(.*)$",
                 linea.strip())
    return m.group(1) if m else None


def _limpia_valor(val):
    """Quita envoltorios **, [], "" de un valor de campo."""
    val = re.sub(r"^(\*\*|\[)+", "", val.strip()).strip()
    val = re.sub(r"(\*\*|\])+$", "", val).strip()
    if len(val) >= 2 and val[0] in "\"“" and val[-1] in "\"”":
        val = val[1:-1].strip()
    return val


def _buscar_en_guion(guion, frag, min_pal=3):
    """Recupera del guion el texto que empieza con `frag` (que quedó partido).

    v29.1: probado para el caso S10 del proyecto 35 (número «40» partido
    entre párrafos). Se conserva como utilidad, pero el llamador automático
    se descartó: era frágil (abreviaturas como «McManus, I. C.»). La
    recuperación efectiva para ese job se hace en reparar_faltantes (coser
    la VOZ partida con la escena siguiente).
    """
    frag = (frag or "").strip()
    if len(frag.split()) < min_pal or not guion:
        return ""
    pos = guion.find(frag)
    if pos < 0:
        return ""
    resto = guion[pos:pos + 1200]
    frases = re.split(r"(?<=[.!?])\s+", resto)
    salida = frases[0] if frases else ""
    if salida and salida[-1] not in ".!?" and len(frases) > 1:
        salida += " " + frases[1]
    return salida.strip()


def _campo(bloque, nombre, guion=""):
    """Extrae VOZ:/VISUAL: tolerando las variantes de formato de los
    modelos. Devuelve el texto limpio; "" si no hay marcador.

    Si el marcador quedó con la línea vacía (el modelo puso el texto en la
    línea siguiente), toma la primera línea no vacía que siga, siempre que
    no sea otro marcador ni un encabezado de escena.

    v29.1: si el valor queda demasiado corto (señal de que el párrafo se
    partió y el resto vive en la escena siguiente), intenta recuperarlo del
    guion con `guion` (texto de referencia). Sin guion, no hace nada.
    """
    lineas = bloque.splitlines()
    for i, ln in enumerate(lineas):
        v = _valor_campo_linea(ln, nombre)
        if v is None:
            continue
        v = _limpia_valor(v)
        if not v:
            for sig in lineas[i + 1:]:
                s = sig.strip()
                if not s or s.startswith("#"):
                    continue
                if _valor_campo_linea(s, "VOZ") is None \
                        and _valor_campo_linea(s, "VISUAL") is None:
                    v = _limpia_valor(s)
                break
        return v
    return ""


def _normalizar_campos(text):
    """Reescribe cualquier variante de marcador al formato estándar
    VOZ: / VISUAL: para que el archivo quede limpio.

    v28: usa el mismo matcher tolerante de `_campo`, así lo que se parsea
    es exactamente lo que se normaliza (antes había dos definiciones que
    podían divergir). Si el marcador tenía la línea vacía, jala la primera
    línea de contenido siguiente.
    """
    lineas = text.splitlines()
    consumidas = set()
    out = []
    for i, ln in enumerate(lineas):
        if i in consumidas:
            continue
        nuevo = None
        for nombre in ("VOZ", "VISUAL"):
            v = _valor_campo_linea(ln, nombre)
            if v is None:
                continue
            v = _limpia_valor(v)
            if not v:
                for j in range(i + 1, len(lineas)):
                    s = lineas[j].strip()
                    if not s or s.startswith("#"):
                        continue
                    if _valor_campo_linea(s, "VOZ") is None \
                            and _valor_campo_linea(s, "VISUAL") is None:
                        v = _limpia_valor(s)
                        consumidas.add(j)
                    break
            nuevo = f"{nombre}: {v}"
            break
        out.append(nuevo if nuevo is not None else ln)
    cola = "\n" if text.endswith("\n") else ""
    return "\n".join(out) + cola


def _voz_words(text, guion=""):
    """Palabras totales en los campos VOZ: del storyboard.

    v29.1: `guion` (narración de referencia) permite recuperar VOZ partidas
    igual que `_campo`, para que la cobertura no cuente de menos.
    """
    return sum(len(_campo(b, "VOZ", guion).split())
               for b in _bloques_escena(text))


def _limpiar_parte(text):
    """Quita la basura que los modelos débiles agregan: preámbulos
    ("¡Excelente!..."), separadores "---" y falsos conteos de palabras.
    Devuelve el texto desde la primera escena; si no hay escenas, "".
    """
    m = re.search(r"(?m)^### S\d+", text)
    if not m:
        return ""
    text = text[m.start():]
    lineas = []
    for ln in text.split("\n"):
        s = ln.strip()
        if s == "---" or s.startswith("**Recuento de palabras"):
            continue
        lineas.append(ln)
    return "\n".join(lineas).strip()


def _ultima_voz(text):
    """Últimas ~15 palabras de la última VOZ: ancla para continuar."""
    voces = [_campo(b, "VOZ") for b in _bloques_escena(text)]
    voces = [v for v in voces if v]
    if not voces:
        return ""
    return " ".join(voces[-1].split()[-15:])


def _quitar_repetidas(text, desde):
    """Quita escenas con número < `desde` (el modelo a veces repite la
    escena ancla al continuar)."""
    bloques = re.split(r"(?m)^(?=### S\d+)", text)
    buenos = [b for b in bloques
              if not re.match(r"### S(\d+)", b)
              or int(re.match(r"### S(\d+)", b).group(1)) >= desde]
    return "".join(buenos).strip()


def _escenas_validas(text, parte_words):
    """Chequeo de formato por parte: empieza con escena y trae un número
    razonable de escenas para las palabras del trozo."""
    if not text:
        return False
    n = len(re.findall(r"(?m)^### S\d+", text))
    esperado = max(5, int(parte_words / 40))
    return n >= esperado


def _prompt_parte(i, n_partes, parte, siguiente):
    """Prompt del storyboard para una parte, con objetivo de cobertura."""
    pw = len(parte.split())
    objetivo = int(pw * 0.9)
    bordes = ""
    if i == 0:
        bordes = ("Esta es la PRIMERA parte: la primera escena es la "
                  "bienvenida (tarjeta_canal + saludo del guion). ")
    if i == n_partes - 1:
        bordes += ("Esta es la ÚLTIMA parte: termina con la despedida "
                   "final del guion (tono cálido, cierre del canal).")
    return (
        f"PARTE {i + 1} de {n_partes} del guion "
        f"(esta parte tiene ~{pw} palabras). Genera el storyboard SÓLO "
        f"de esta parte. {bordes}La primera escena es S{siguiente:02d} "
        f"(continúa la numeración, NO reinicies en S01).\n"
        f"OBJETIVO MEDIBLE: los campos VOZ sumados deben tener al menos "
        f"{objetivo} palabras (90% de esta parte). Cuéntalas antes de "
        f"responder. Empieza DIRECTAMENTE con ### S{siguiente:02d}, sin "
        f"preámbulos ni comentarios.\n\n" +
        STORYBOARD_PROMPT.format(script=parte[:6000]))


def run_storyboard(generate_fn, p, job):
    if not generate_fn:
        return (False, "Necesita un backend LLM: configura una key en "
                       "Configuración o usa Ollama local.", [], None)
    sp = find_script(p)
    if not sp:
        return False, "Sin guion: primero genera el borrador (etapa guion).", [], None
    script = Path(sp).read_text(encoding="utf-8", errors="replace")
    # v29.1: se cuenta y se parte SOLO la narración (sin markup de producción
    # ni secciones FUENTES/MINIATURAS): ver _narracion_guion.
    narracion = _narracion_guion(script)
    guion_words = count_words(narracion)
    # Anti-truncado ESTRUCTURAL (3 capas): además del chequeo de cobertura,
    # los guiones largos se generan POR PARTES. Un storyboard completo de
    # ~1800 palabras no cabe en la salida de los modelos gratis y el modelo
    # se corta a la mitad (jobs/37: 53%). Por partes sí cabe.
    # El tamaño del trozo se adapta al backend: con límite de salida bajo
    # (Groq: 1000 tokens) los trozos son más chicos para que cada parte quepa.
    backend = getattr(generate_fn, "backend", "") or ""
    try:
        import llm as _llm
        mt = _llm.MAX_TOKENS.get(backend, 8192)
    except Exception:
        mt = 8192
    trozo = 350 if mt <= 1000 else 650
    partes = (_partir_guion(narracion, trozo) if guion_words > 1000
              else [script])
    textos, model, siguiente = [], "", 1
    for i, parte in enumerate(partes):
        parte_words = len(parte.split())
        objetivo = int(parte_words * 0.9)
        if len(partes) > 1:
            prompt_base = _prompt_parte(i, len(partes), parte, siguiente)
        else:
            prompt_base = STORYBOARD_PROMPT.format(script=script[:12000])
        # Continuación AUTOMÁTICA por parte: genera, mide, y si falta
        # cobertura continúa desde la última escena (anclada en su VOZ)
        # hasta llegar al 90% o agotar 3 intentos. Así el 80% que salió
        # bien no se regenera: solo se completa lo que faltó.
        trozos_p, ultimo, vw_p = [], siguiente, 0
        for intento in range(3):
            if intento == 0:
                prompt = prompt_base
            else:
                ancla = _ultima_voz("\n\n".join(trozos_p))
                faltan = max(0, objetivo - vw_p)
                temas_p = _temas_cubiertos("\n\n".join(textos) + "\n\n" +
                                           "\n\n".join(trozos_p), tope=8)
                no_rep = (f" Ya cubriste estos temas, NO los repitas: "
                          f"{', '.join(temas_p)}." if temas_p else "")
                prompt = (
                    f"CONTINUACIÓN de la PARTE {i + 1} de {len(partes)}: ya "
                    f"generaste hasta S{ultimo - 1:02d} (su VOZ terminaba en: "
                    f"\"...{ancla}\"). Continúa el storyboard desde el punto "
                    f"del guion donde te quedaste, SIN repetir escenas.{no_rep} "
                    f"Empieza DIRECTAMENTE con ### S{ultimo:02d}, sin "
                    f"preámbulos. Te faltan ~{faltan} palabras de VOZ para "
                    f"llegar al objetivo de {objetivo} (copia literal, sin "
                    f"resumir).\n\nGuion de esta parte:\n{parte[:6000]}")
            try:
                text, model = generate_fn(
                    prompt, system="Eres director de animación minimalista.")
            except Exception as e:
                if intento == 0 and not trozos_p:
                    return False, (
                        f"Error del modelo en parte {i + 1}/{len(partes)}: "
                        f"{e}"), [], None
                break  # conserva lo generado hasta ahora
            text = _limpiar_parte(text)
            text = _normalizar_campos(text)
            text = _renumerar_desde(text, ultimo)
            text = _quitar_repetidas(text, ultimo)
            if not text.strip():
                break
            trozos_p.append(text)
            nums = [int(m.group(1))
                    for m in re.finditer(r"### S(\d+)", text)]
            if nums:
                ultimo = max(nums) + 1
            vw_p = _voz_words("\n\n".join(trozos_p))
            if vw_p >= objetivo and _escenas_validas("\n\n".join(trozos_p),
                                                     parte_words):
                break
        text = "\n\n".join(trozos_p)
        textos.append(text)
        nums = [int(m.group(1)) for m in re.finditer(r"### S(\d+)", text)]
        if nums:
            siguiente = max(nums) + 1
    text = "\n\n".join(textos)
    out = job / "STORYBOARD.md"
    out.write_text(text, encoding="utf-8")
    n = text.count("### S")
    # Anti-truncado ESTRUCTURAL: si el storyboard no cubre el guion, la etapa
    # FALLA (no avisa y sigue). Un storyboard cortado = video cortado.
    # Umbral 90%: con 70% un guion de 1300 palabras pierde ~400 (casi 3 min).
    voz_words = _voz_words(text, narracion)
    if guion_words > 0 and voz_words < 0.9 * guion_words:
        return False, (
            f"⛔ STORYBOARD TRUNCADO: cubre ~{voz_words} palabras de "
            f"{guion_words} del guion (mínimo 90%). Si continuara, el video "
            f"saldría cortado (como el proyecto 18: 3 min en vez de 9). "
            f"Opciones: 1) pulsa «↪️ Continuar storyboard» aquí abajo para "
            f"que el modelo complete las escenas faltantes desde "
            f"S{n + 1:02d} sin regenerar desde cero; 2) reintenta la etapa "
            f"con otro backend."), [str(out)], None
    return True, (f"Storyboard con {model}: {n} escenas en {out} "
                  f"(~{voz_words} palabras de VOZ)."), [str(out)], None


def run_continuar_storyboard(generate_fn, p, job):
    """Continúa un storyboard truncado desde la última escena existente.

    No regenera desde cero: pide al modelo solo las escenas faltantes
    (las partes del guion aún sin cubrir) y las agrega a STORYBOARD.md.
    Devuelve (ok, log, artefactos, None).
    """
    if not generate_fn:
        return (False, "Necesita un backend LLM.", [], None)
    sb = job / "STORYBOARD.md"
    if not sb.exists():
        return False, "No hay STORYBOARD.md: corre la etapa storyboard.", [], None
    text = sb.read_text(encoding="utf-8", errors="replace")
    nums = [int(m.group(1)) for m in re.finditer(r"### S(\d+)", text)]
    if not nums:
        return False, "El storyboard no tiene escenas ### Sxx.", [], None
    n = max(nums)
    sp = find_script(p)
    script = Path(sp).read_text(encoding="utf-8", errors="replace") if sp else ""
    # v29.1: continuar también en lenguaje de NARRACIÓN (sin markup), para que
    # el modelo no re-cree bloques de producción ni la sección FUENTES.
    narracion = _narracion_guion(script) if script else ""
    # Anti-repetición: el modelo tiende a re-contar la parte más narrable
    # (proyecto 37: Wagner 4 veces). Se le prohíben los temas ya cubiertos.
    temas = _temas_cubiertos(text)
    no_repetir = (f"\nTEMAS YA CUBIERTOS (PROHIBIDO repetirlos o re-contarlos "
                  f"desde cero): {', '.join(temas)}.\n" if temas else "")
    prompt = (
        f"Este storyboard quedó TRUNCADO en S{n:02d}. Continúa desde "
        f"S{n + 1:02d} cubriendo ÚNICAMENTE las partes del guion que aún no "
        f"tienen escena, hasta la despedida final del guion (tono cálido, "
        f"cierre del canal). Mismo formato exacto por escena:\n"
        f"### SXX\nVOZ: <texto literal del guion>\nVISUAL: <descripción>\n\n"
        f"REGLAS: escenas de 8-12s (~25-35 palabras de VOZ); PROTAGONISTA en "
        f"todas; NO repitas escenas ya existentes.{no_repetir}\n"
        f"STORYBOARD EXISTENTE (referencia, no lo repitas):\n{text[-6000:]}\n\n"
        f"GUION (narración):\n{narracion[:12000]}")
    try:
        new_text, model = generate_fn(
            prompt, system="Eres director de animación minimalista.")
    except Exception as e:
        return False, f"Error del modelo: {e}", [], None
    # Quédate solo con bloques nuevos (número > n)
    partes = re.split(r"(?m)^(?=### S\d+)", new_text)
    nuevos = []
    for bl in partes:
        m = re.match(r"### S(\d+)", bl.strip())
        if m and int(m.group(1)) > n:
            nuevos.append(bl.strip())
    if not nuevos:
        return False, ("El modelo no devolvió escenas nuevas (S{n + 1:02d}+). "
                       "Reintenta con otro backend."), [str(sb)], None
    nuevos = [_normalizar_campos(bl) for bl in nuevos]
    with open(sb, "a", encoding="utf-8") as f:
        f.write("\n\n" + "\n\n".join(nuevos) + "\n")
    total = n + len(nuevos)
    # Revalida cobertura
    full = sb.read_text(encoding="utf-8", errors="replace")
    voz_words = _voz_words(full)
    guion_words = count_words(narracion)
    if guion_words > 0 and voz_words < 0.7 * guion_words:
        return False, (
            f"Se agregaron {len(nuevos)} escenas (total S{total:02d}) pero la "
            f"cobertura sigue baja (~{voz_words}/{guion_words} palabras). "
            f"Pulsa «↪️ Continuar storyboard» otra vez."), [str(sb)], None
    return True, (f"Storyboard completado con {model}: {len(nuevos)} escenas "
                  f"nuevas, total {total} (S01–S{total:02d})."), [str(sb)], None


# ---------- paquete de publicación (asistida) ----------
PAQUETE_PROMPT = """Eres el editor de un canal de YouTube de divulgación científica en español (estilo Zenn).
Genera el paquete de publicación COMPLETO para el video "{title}", con EXACTAMENTE este formato.

REGLAS DE FORMATO (obligatorias: romperlas daña la credibilidad del canal):
- PROHIBIDO markdown: nada de **, ##, ### ni *cursivas*. YouTube lo muestra como texto crudo y se ve como error de automatización.
- Los encabezados dentro de las secciones son texto plano con emoji, p. ej. "🔍 LO QUE VERÁS:".
- Viñetas con "•", nunca con guiones.

TITULOS (máx 60 caracteres cada uno, INCLUYENDO el sufijo):
1. <opción 1: fórmula pregunta directa, afirmación fuerte, número o superlativo + palabra clave al frente. Gancho honesto, sin clickbait falso. Ej: "¿Por qué los mosquitos siempre te pican a TI?">
2. <opción 2>
3. <opción 3>
A las 3 opciones agrégales al final " | En {dur_min} minutos" (promesa de duración, fórmula de Memorias de Pez; el total con sufijo no pasa de 60 caracteres: acorta el título base si hace falta).

DESCRIPCION:
<líneas 1-2: el gancho en segunda persona — la pregunta del video + qué se lleva el espectador. Es lo que se ve sin desplegar: lo más importante de todo>
<1 línea de valor: qué aprenderá, con la palabra clave>

LO QUE VERAS:
<4-6 líneas, cada una empezando con "•", puntos concretos del video>

CAPITULOS:
<elige 5-8 cortes de la LISTA DE MARCAS de abajo, formato "m:ss Título corto". La primera marca debe ser 0:00. Usa solo marcas de la lista.>

FUENTES:
<las fuentes reales citadas en el guion/investigación, una por línea, formato "Autor (año). Título.">

CTA:
<1 línea invitando a suscribirse, p. ej: "🔔 Suscríbete a Indaga para la siguiente indagación, cada semana.">

PREGUNTA:
<1 pregunta abierta para los comentarios, sin repetir el título, terminada en "👇">

HASHTAGS: <#tag1 #tag2 #tag3 — de 3 a 5, el primero = la palabra clave principal en minúsculas>
TAGS: <12-15 etiquetas separadas por comas, en minúsculas, ESPECÍFICAS (nada de "mundo", "ciencia" solos), la primera = la frase clave exacta>
COMENTARIO FIJADO: <pregunta abierta distinta a la de PREGUNTA, que invite a responder>
POST COMUNIDAD: <2-3 líneas anunciando el video con la pregunta del tema>
SHORT SUGERIDO: <escena de la lista (Sxx) que mejor funciona sola en 30-45s y por qué>
PANTALLA FINAL: <texto y tipo de video a enlazar>

LISTA DE MARCAS (inicio de cada escena, no inventes otras):
{marks}

GUION (extracto):
{script}
"""


def _scene_marks(job):
    """Marcas de tiempo reales por escena desde los audios TTS."""
    vo = job / "vo.json"
    if not vo.exists():
        return "(sin audios todavía: capítulos aproximados por escena)"
    items = json.loads(vo.read_text(encoding="utf-8"))
    lines, t = [], 0.0
    for it in items:
        au = _audio_path(job, it["id"])
        dur = _probe_duration(au) if au.exists() else 0.0
        m, s = divmod(int(t), 60)
        lines.append(f"{m}:{s:02d} {it['id'].upper()} — "
                     f"{it['text'][:60]}...")
        t += dur
    return "\n".join(lines)


def run_paquete(generate_fn, p, job):
    if not generate_fn:
        return (False, "Necesita un backend LLM: configura una key en "
                       "Configuración o usa Ollama local.", [], None)
    sp = find_script(p)
    script = ""
    if sp:
        script = Path(sp).read_text(encoding="utf-8", errors="replace")[:6000]
    inv = job / "INVESTIGACION.md"
    if inv.exists():
        script += "\n\nINVESTIGACIÓN:\n" + inv.read_text(
            encoding="utf-8", errors="replace")[:3000]
    # Duración real del video (para el sufijo "| En N minutos" de los
    # títulos, fórmula de Memorias de Pez): final.mp4 si existe, si no
    # suma de los audios TTS.
    dur_min = 10
    final = job / "video" / "final_con_subtitulos.mp4"
    if not final.exists():
        final = job / "video" / "final.mp4"
    if final.exists():
        d = _probe_duration(final)
        if d:
            dur_min = max(1, int(round(d / 60)))
    else:
        t = 0.0
        try:
            for it in json.loads((job / "vo.json").read_text(
                    encoding="utf-8")):
                au = _audio_path(job, it["id"])
                if au.exists():
                    t += _probe_duration(au) or 0.0
        except Exception:
            pass
        if t > 60:
            dur_min = max(1, int(round(t / 60)))
    try:
        text, model = generate_fn(
            PAQUETE_PROMPT.format(title=p["title"], script=script,
                                  marks=_scene_marks(job),
                                  dur_min=dur_min),
            system="Eres un editor de YouTube preciso y directo.")
    except Exception as e:
        return False, f"Error del modelo: {e}", [], None
    out = job / "PAQUETE.md"
    out.write_text(text, encoding="utf-8")
    return True, f"Paquete generado con {model} en {out}.", [str(out)], None


# ---------- TTS multi-motor (automático) ----------
def _narracion_job(job):
    """Narración del guion de un job (para recuperar VOZ partidas)."""
    for name in ("GUION.md", "GUION_PILOTO.md", "guion.md"):
        c = Path(job) / name
        if c.exists():
            return _narracion_guion(
                c.read_text(encoding="utf-8", errors="replace"))
    return ""


def _parse_storyboard(job):
    sb = job / "STORYBOARD.md"
    scenes = []
    if not sb.exists():
        return scenes
    text = sb.read_text(encoding="utf-8", errors="replace")
    guion = _narracion_job(job)
    for m in re.finditer(r"###\s*(S\d+)(.*?)(?=###\s*S\d+|\Z)", text, re.S):
        scenes.append({"id": m.group(1).lower(),
                       "voz": _campo(m.group(2), "VOZ", guion),
                       "visual": _campo(m.group(2), "VISUAL")})
    return scenes


def _temas_cubiertos(text, tope=10):
    """Nombres propios y title_cards ya usados en el storyboard.
    Se pasan al prompt de continuación para PROHIBIR que el modelo los
    repita (proyecto 37: Wagner/Doepler se contó 4 veces)."""
    temas = []
    for m in re.finditer(r"title_card\(([^)]+)\)", text):
        t = m.group(1).strip().strip("\"'")
        if t and t.lower() not in [x.lower() for x in temas]:
            temas.append(t)
    from collections import Counter
    palabras = re.findall(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{3,}", text)
    comunes = {"Pero", "Porque", "Cuando", "Como", "Este", "Esta", "Para",
               "Entre", "Sobre", "Desde", "Hasta", "Porque", "Aunque",
               "Entonces", "Así", "Piénsalo", "Imagina"}
    for pal, cnt in Counter(palabras).most_common(tope * 2):
        if cnt >= 3 and pal not in comunes and \
                pal.lower() not in [x.lower() for x in temas]:
            temas.append(pal)
        if len(temas) >= tope:
            break
    return temas


