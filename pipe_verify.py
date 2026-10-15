"""Verificacion de artefactos, contratos de etapa y reparacion de faltantes."""
import json
import re
from pathlib import Path

from pipe_core import (BASE, _audio_path, _narracion_guion, _probe_duration,
                       count_words, find_script, job_dir_of, pget)
from pipe_storyboard import (_bloques_escena, _campo, _narracion_job,
                             _parse_storyboard, _voz_words,
                             run_continuar_storyboard)
from pipe_tts import (_ids_con_archivo, build_vo_json, run_tts_stage)

def verificar_elementos(p, job):
    """Valida que los artefactos de cada etapa estén completos y
    consistentes entre sí (el storyboard manda).

    Devuelve {"ok": bool, "detalle": {...}, "resumen": str}. Se usa al
    inicio de "Correr todo" y en el botón 🔍 Verificar elementos.
    """
    job = Path(job)
    scenes = _parse_storyboard(job)
    sb_ids = [s["id"] for s in scenes]
    det = {}
    cortas = [s["id"].upper() for s in scenes
              if s["voz"] and len(s["voz"].split()) < 5]
    # v27: escenas sin VOZ legible (formato no reconocido) — antes se
    # descartaban en silencio en build_vo_json y la reparación entraba en loop
    sin_voz = [s["id"].upper() for s in scenes if not s["voz"]]
    det["storyboard"] = {"total": len(sb_ids),
                         "ok": bool(sb_ids) and not sin_voz,
                         "faltan": [], "cortas": cortas, "sin_voz": sin_voz}
    # Calidad narrativa: repeticiones, doble final y citas sueltas.
    det["storyboard"]["repeticiones"] = _repeticiones(
        (job / "STORYBOARD.md").read_text(encoding="utf-8", errors="replace")
        if (job / "STORYBOARD.md").exists() else "")
    desp_id, desp_n = _doble_final(scenes)
    det["storyboard"]["doble_final"] = (desp_id, desp_n)
    det["storyboard"]["citas_sueltas"] = _citas_sueltas(scenes)
    # vo.json: debe cubrir las mismas escenas que el storyboard
    vo_ids = []
    vf = job / "vo.json"
    if vf.exists():
        try:
            vo_ids = [str(it.get("id", "")).lower()
                      for it in json.loads(vf.read_text(encoding="utf-8"))]
        except Exception:
            vo_ids = []
    faltan_vo = [i for i in sb_ids if i not in vo_ids]
    det["vo_json"] = {"total": len(vo_ids), "faltan": faltan_vo,
                      "ok": bool(sb_ids) and not faltan_vo}
    # audios (etapa 6) — v26: no basta que el archivo exista y no esté vacío;
    # un mp3 truncado (corte de luz, runner muerto a la mitad) pasa el filtro
    # de existencia pero es ilegible. Se prueban con ffprobe (si está).
    import shutil as _sh
    _tienen_au, _faltan_au = _ids_con_archivo(sb_ids, job / "audio", ".mp3")
    _ilegibles = []
    if _tienen_au and _sh.which("ffprobe"):
        _ilegibles = [i for i in _tienen_au
                      if _probe_duration(_audio_path(job, i)) <= 0]
    faltan_au = _faltan_au + _ilegibles
    det["audios"] = {"total": len(sb_ids),
                     "tienen": len(sb_ids) - len(faltan_au),
                     "faltan": faltan_au, "ok": bool(sb_ids) and not faltan_au,
                     "ilegibles": _ilegibles}
    # videos (etapa 7)
    _, faltan_vi = _ids_con_archivo(sb_ids, job / "video" / "scenes", ".mp4")
    det["videos"] = {"total": len(sb_ids),
                     "tienen": len(sb_ids) - len(faltan_vi),
                     "faltan": faltan_vi, "ok": bool(sb_ids) and not faltan_vi}
    # ensamblado (etapa 8)
    final = job / "video" / "final.mp4"
    det["ensamblado"] = {"ok": final.exists() and final.stat().st_size > 0,
                         "faltan": []}
    ok = all(v["ok"] for v in det.values())
    partes = []
    for clave, nombre in (("storyboard", "Storyboard"),
                          ("vo_json", "vo.json"), ("audios", "Audios"),
                          ("videos", "Videos"), ("ensamblado", "Ensamblado")):
        v = det[clave]
        marca = "✅" if v["ok"] else "❌"
        extra = ""
        if v["faltan"]:
            fs = ", ".join(i.upper() for i in v["faltan"][:8])
            extra = f" (faltan: {fs}{'...' if len(v['faltan']) > 8 else ''})"
        if clave == "storyboard":
            sbd = det["storyboard"]
            if sbd["cortas"]:
                cs = ", ".join(sbd["cortas"][:8])
                extra += f" [VOZ muy corta: {cs}]"
            if sbd["repeticiones"]:
                rp = "; ".join(f"{t} ({', '.join(e)})"
                               for t, e in sbd["repeticiones"][:3])
                extra += f" [⚠️ posible repetición: {rp}]"
            desp_id, desp_n = sbd["doble_final"]
            if desp_n:
                extra += (f" [⚠️ doble final: despedida en {desp_id} y "
                          f"{desp_n} escenas después]")
            if sbd["citas_sueltas"]:
                extra += (f" [cita suelta: "
                          f"{', '.join(sbd['citas_sueltas'][:5])}]")
            if sbd.get("sin_voz"):
                sv = sbd["sin_voz"]
                extra += (f" [SIN VOZ legible: {', '.join(sv[:8])}"
                          f"{'...' if len(sv) > 8 else ''} — ningún botón "
                          f"las arregla: edita STORYBOARD.md o etapa 5]")
        partes.append(f"{marca} {nombre}{extra}")
    return {"ok": ok, "detalle": det, "resumen": " · ".join(partes)}


def reparar_faltantes(p, job, forzar="", conn=None, pid=None):
    """Repara los artefactos incompletos de un proyecto (lo que hacía el
    botón "🛠 Reparar faltantes" en app.py).

    v28: la lógica vive aquí (no en el UI) para poder probarla punta a punta
    sin Streamlit. `forzar` = "s34, s35": borra esos mp3 antes de reparar
    (el TTS omite lo existente). Si se dan conn/pid se actualiza la etapa
    "tts" en la BD. Devuelve (kind, texto) con kind en {"ok", "warning"}.
    """
    job = Path(job)
    # v26/v27: forzar = borrar primero; solo se aceptan ids de escena.
    # v28: se parte por comas, punto y coma y espacios; se ignora el resto
    # (el usuario pega texto del error como "s34, s35; audios: s34").
    forzados = []
    for tok in re.split(r"[,\s;]+", (forzar or "")):
        tok = tok.strip().lower().strip(".;:")
        if not re.fullmatch(r"s\d+", tok):
            continue
        au = _audio_path(job, tok)
        if au.exists():
            au.unlink()
        if tok.upper() not in forzados:
            forzados.append(tok.upper())
    rep = verificar_elementos(p, job)["detalle"]
    msgs = []
    # v28: los audios ilegibles (truncados) se regeneran solos. El TTS los
    # omitiría por "ya existían", así que se borran aquí: son archivos
    # generados e inservibles, no trabajo del usuario.
    for i in rep["audios"].get("ilegibles", []):
        au = _audio_path(job, i)
        if au.exists():
            au.unlink()
            msgs.append(f"audio corrupto {str(i).upper()} borrado para "
                        f"regenerar.")
    if forzados:
        msgs.append(f"forzados para regenerar: {', '.join(forzados)}.")
    # 1) vo.json desactualizado -> se sincroniza solo
    if not rep["vo_json"]["ok"]:
        n, origen, sin_voz = build_vo_json(p, job)
        msgs.append(f"vo.json sincronizado ({n} líneas).")
        # v27: escenas sin VOZ legible = la reparación NO puede arreglarlas
        if sin_voz:
            lista = ", ".join(s.upper() for s in sin_voz[:10])
            if len(sin_voz) > 10:
                lista += f" (+{len(sin_voz) - 10} más)"
            msgs.append(f"⚠️ {len(sin_voz)} escenas sin VOZ legible ({lista}): "
                        f"edita STORYBOARD.md con formato 'VOZ: ...' o "
                        f"re-ejecuta la etapa 5; ningún botón las puede generar.")
    # 2) audios faltantes -> etapa 6 (omite los existentes)
    if not rep["audios"]["ok"]:
        ok, log, arts, _ = run_tts_stage(p, job)
        if conn is not None and pid is not None:
            import db as _db
            _db.set_stage(conn, pid, "tts", "ok" if ok else "fallo", log, arts)
        msgs.append(("audios regenerados: " if ok else "TTS falló: ") + log[:200])
    # 3) videos faltantes -> se informa (etapa 7 es asistida)
    if not rep["videos"]["ok"]:
        fs = ", ".join(i.upper() for i in rep["videos"]["faltan"][:10])
        msgs.append(f"videos faltantes ({fs}): re-ejecuta la etapa 7 "
                    "(omite solas las ya hechas).")
    if not msgs:
        msgs.append("Nada que reparar: todo completo. ✅")
    # v26: re-verificar DESPUÉS de reparar — no declarar éxito si algo sigue
    # roto (el caso S34: el TTS decía "omitidos: 82" pero el ensamblado
    # seguía sin el archivo).
    rep2 = verificar_elementos(p, job)
    if not rep2["ok"]:
        falt = []
        for k in ("vo_json", "audios", "videos"):
            f = rep2["detalle"][k]["faltan"]
            if f:
                falt.append(f"{k}: {', '.join(i.upper() for i in f[:6])}")
        sv = rep2["detalle"]["storyboard"].get("sin_voz") or []
        if sv:
            falt.append(f"storyboard sin VOZ: {', '.join(sv[:6])}")
        msgs.append("⚠️ SIGUE INCOMPLETO tras reparar: " + "; ".join(falt)
                    + ". Revisa el mensaje: si un audio «existe» pero falla, "
                    "usa «Forzar» con esa escena.")
        return "warning", " ".join(msgs)
    return "ok", " ".join(msgs)


def _cobertura_storyboard(p, job):
    """(palabras_VOZ, palabras_guion) para el contrato de la etapa 5."""
    sp = find_script(p)
    guion_words = 0
    narracion = ""
    if sp:
        script = Path(sp).read_text(encoding="utf-8", errors="replace")
        # v29.1: cobertura contra la NARRACIÓN del guion, no contra el guion
        # crudo con markup (incluirlo volvía el 90% imposible -> falso TRUNCADO).
        narracion = _narracion_guion(script)
        guion_words = count_words(narracion)
    sb = Path(job) / "STORYBOARD.md"
    voz_words = (_voz_words(sb.read_text(encoding="utf-8", errors="replace"),
                            narracion) if sb.exists() else 0)
    return voz_words, guion_words


# v28 — contratos de etapa: lo que cada etapa DEBE dejar producido para que
# la corrida pueda avanzar. Si el contrato no se cumple, la corrida no avanza
# en silencio: repara una vez o se detiene con mensaje accionable.
CONTRATO_ETAPAS = {
    "storyboard": "STORYBOARD.md existe, sin escenas sin VOZ y cobertura ≥90% del guion",
    "tts": "vo.json cubre el storyboard y cada escena tiene audio válido (existe, no vacío, duración legible)",
    "animacion": "cada escena del storyboard tiene su mp4 válido",
    "ensamblado": "video/final.mp4 existe y dura ≈ suma de audios (±15%)",
}
# Insumos obligatorios antes de arrancar cada etapa.
_PRE_ETAPA = {
    "tts": ["storyboard"],
    "animacion": ["tts"],
    "ensamblado": ["tts", "animacion"],
}


def validar_etapa(stage, p, job):
    """Verifica el contrato de salida de una etapa. Devuelve (ok, detalle).

    Es la pieza que faltaba: antes cada etapa "terminaba" y la siguiente
    asumía que todo estaba bien (origen de los loops S34/S48). Ahora el
    avance es contractual.
    """
    job = Path(job)
    det = verificar_elementos(p, job)["detalle"]
    if stage == "storyboard":
        if not (job / "STORYBOARD.md").exists():
            return False, "no existe STORYBOARD.md"
        sv = det["storyboard"].get("sin_voz") or []
        if sv:
            return False, (f"{len(sv)} escenas sin VOZ legible "
                           f"({', '.join(sv[:8])})")
        vw, gw = _cobertura_storyboard(p, job)
        if gw > 0 and vw < 0.9 * gw:
            return False, f"cobertura {vw}/{gw} palabras (<90%)"
        return True, (f"{det['storyboard']['total']} escenas, "
                      f"cobertura {vw}/{gw}")
    if stage == "tts":
        if det["vo_json"]["faltan"]:
            return False, ("vo.json no cubre: "
                           + ", ".join(det["vo_json"]["faltan"][:8]))
        if det["audios"]["faltan"]:
            return False, ("audios faltan/ilegibles: "
                           + ", ".join(str(x).upper()
                                       for x in det["audios"]["faltan"][:8]))
        return True, (f"{det['audios']['tienen']}/{det['audios']['total']} "
                      "audios válidos")
    if stage == "animacion":
        if det["videos"]["faltan"]:
            return False, ("videos faltan: "
                           + ", ".join(det["videos"]["faltan"][:8]))
        return True, (f"{det['videos']['tienen']}/{det['videos']['total']} "
                      "videos")
    if stage == "ensamblado":
        final = job / "video" / "final.mp4"
        if not (final.exists() and final.stat().st_size > 0):
            return False, "no existe video/final.mp4"
        try:
            items = json.loads((job / "vo.json").read_text(encoding="utf-8"))
            suma = sum(_probe_duration(_audio_path(job, it.get("id", "")))
                       for it in items)
        except Exception:
            suma = 0
        dur = _probe_duration(final)
        if suma > 0 and dur > 0 and abs(dur - suma) > 0.15 * suma:
            return False, (f"final.mp4 dura {dur:.0f}s pero los audios suman "
                           f"{suma:.0f}s (se esperaba ±15%)")
        return True, f"final.mp4 {dur:.0f}s"
    return True, "etapa sin contrato: vale el resultado de execute_stage"


def _auto_reparar(stage, p, job, generate_fn):
    """UN intento de reparación automática tras un contrato incumplido."""
    if stage == "storyboard":
        vw, gw = _cobertura_storyboard(p, job)
        sv = verificar_elementos(p, job)["detalle"]["storyboard"].get("sin_voz")
        if sv:
            return ("sin auto-reparación: hay escenas sin VOZ legible "
                    "(formato); lo debe arreglar un humano en STORYBOARD.md")
        if gw > 0 and vw < 0.9 * gw and generate_fn:
            ok, log, _, _ = run_continuar_storyboard(generate_fn, p, job)
            return f"continuación automática: {'ok' if ok else 'falló'}"
        return "sin auto-reparación aplicable"
    if stage in ("tts", "ensamblado"):
        kind, txt = reparar_faltantes(p, job)
        return f"reparar_faltantes ({kind})"
    if stage == "animacion":
        return "reintento (omite las ya renderizadas)"
    return "sin auto-reparación"


def _repeticiones(text):
    """Detecta posible repetición de temas: title_cards duplicados o nombres
    propios que aparecen en 2+ bloques de escenas separados (>10 escenas).
    Devuelve lista de (tema, [escenas])."""
    reps = []
    cards = {}
    for b in _bloques_escena(text):
        mh = re.match(r"###\s*(S\d+)", b)
        if not mh:
            continue
        for m in re.finditer(r"title_card\(([^)]+)\)", b):
            t = m.group(1).strip().strip("\"'").lower()
            if t:
                cards.setdefault(t, []).append(mh.group(1).upper())
    for t, escenas in cards.items():
        if len(escenas) > 1:
            reps.append((f"title_card({t})", escenas))
    bloques = _bloques_escena(text)
    esc_por_pal = {}
    for i, b in enumerate(bloques):
        for pal in set(re.findall(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{3,}", b)):
            esc_por_pal.setdefault(pal, []).append(i + 1)
    comunes = {"Pero", "Porque", "Cuando", "Como", "Este", "Esta", "Para",
               "Entre", "Sobre", "Desde", "Hasta", "Aunque", "Entonces",
               "Así", "Vikingo", "Vikingos", "Vikinga", "Protagonista"}
    for pal, escenas in esc_por_pal.items():
        if pal in comunes or len(escenas) < 3:
            continue
        # agrupa en clusters (hueco >5 = otro bloque)
        clusters, actual = [], [escenas[0]]
        for e in escenas[1:]:
            if e - actual[-1] > 5:
                clusters.append(actual)
                actual = [e]
            else:
                actual.append(e)
        clusters.append(actual)
        clusters = [c for c in clusters if len(c) >= 2]
        if len(clusters) >= 2:
            reps.append((pal, [f"S{c[0]:02d}-S{c[-1]:02d}" for c in clusters]))
    return reps


_DESPEDIDA_PAT = re.compile(
    r"esto fue el porqu[eé]|esto fue indaga|nos vemos en el pr[oó]ximo|"
    r"para resolver el siguiente porqu[eé]|para la siguiente indagaci[oó]n|"
    r"seguimos indagando|no olvides.*suscri|"
    r"dale.{0,20}me gusta.{0,20}suscr", re.I)


def _doble_final(scenes):
    """Si hay despedida/CTA y después más escenas, el video 'termina dos
    veces'. Devuelve (escena_despedida, n_posteriores)."""
    idx = None
    for i, s in enumerate(scenes):
        if _DESPEDIDA_PAT.search(s["voz"]):
            idx = i
    if idx is not None and idx < len(scenes) - 1:
        return scenes[idx]["id"].upper(), len(scenes) - idx - 1
    return None, 0


def _citas_sueltas(scenes):
    """Escenas cuya VOZ es solo una cita bibliográfica (suenan rotas en TTS)."""
    return [s["id"].upper() for s in scenes
            if re.match(r"^\(.*\d{4}.*\)\.?$", s["voz"].strip())]


