#!/usr/bin/env python3
"""Prueba PUNTA A PUNTA del panel Zenn Factory (v29.1).

Valida el algoritmo de corrida garantizada SIN necesitar keys de LLM ni
red: el LLM se mockea (respuestas deterministas), y el TTS y el render usan
ffmpeg real para producir artefactos válidos. Lo que SÍ es código real:
verificación, contratos, reparación, rotación de backends (llm.generate con
low-level mockeado), continuación automática, pre-flight del ensamblado y
pyflakes (nombres indefinidos: el bug `re` de v27).

Uso:  python3 test_panel_e2e.py
Sale con código 1 si algún escenario falla.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

PANEL = Path(__file__).resolve().parent.parent / "panel"
if not (PANEL / "pipeline.py").exists():
    # layout del ZIP: los archivos del panel van en la raíz
    PANEL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PANEL))
import pipeline as P          # noqa: E402
import tts_engine             # noqa: E402
import llm as _llm            # noqa: E402

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
RESULTS = []


def check(nombre, cond, detalle=""):
    RESULTS.append((nombre, bool(cond), detalle))
    print(("  ✅ " if cond else "  ❌ ") + nombre +
          (f" — {detalle}" if detalle and not cond else ""))
    return bool(cond)


# ---------------- mocks ----------------
def mp3_silencio(path, segundos):
    subprocess.run([FFMPEG, "-v", "error", "-y", "-f", "lavfi", "-i",
                    "anullsrc=r=44100:cl=mono", "-t", f"{segundos:.2f}",
                    "-q:a", "9", "-acodec", "libmp3lame", str(path)],
                   check=True)


def mp4_color(path, segundos=2):
    subprocess.run([FFMPEG, "-v", "error", "-y", "-f", "lavfi", "-i",
                    f"color=c=navy:s=1280x720:d={segundos}",
                    "-pix_fmt", "yuv420p", str(path)], check=True)


def mock_speak_batch(items, voice, audio_dir, language="es", progress=None):
    """Imita tts_engine.speak_batch INCLUYENDO su lógica de omitir
    existentes (existe + tamaño>0). Genera silencios reales con ffmpeg."""
    audio_dir = Path(audio_dir)
    audio_dir.mkdir(parents=True, exist_ok=True)
    ok, omit = 0, 0
    for it in items:
        f = audio_dir / f"{it['id'].lower()}.mp3"
        if f.exists() and f.stat().st_size > 0:
            omit += 1
            continue
        mp3_silencio(f, max(1.0, 0.35 * len(it["text"].split())))
        ok += 1
    return True, f"TTS mock: {ok}/{len(items)} OK | omitidos: {omit}"


def mock_render(generate_fn, sdir, media, vdir, job, sc, rig_text,
                solo_render=False):
    mp4_color(Path(vdir) / f"{sc['id']}.mp4", 2)
    return True, "mock render", False


_real_subprocess_run = subprocess.run


def fake_subprocess_run(cmd, **kw):
    # run_animacion verifica "import manim": lo fingimos instalado.
    if isinstance(cmd, list) and cmd[-2:] == ["-c", "import manim"]:
        return SimpleNamespace(returncode=0, stdout="", stderr="")
    return _real_subprocess_run(cmd, **kw)


class MockLLMStoryboard:
    """generate_fn determinista: convierte el guion en escenas.

    modo="completo": cubre ~100% del guion en la primera llamada.
    modo="trunco": la primera llamada cubre ~40%; las continuaciones
    (prompt con "CONTINUACIÓN") cubren el resto desde la escena indicada.
    """

    def __init__(self, guion_words, modo="completo", por_escena=25):
        self.words = guion_words
        self.modo = modo
        self.por_escena = por_escena
        self.consumidas = 0
        self.llamadas = 0
        self.backend = "mock"

    def __call__(self, prompt, system=""):
        self.llamadas += 1
        if "CONTINUACIÓN" in prompt:
            m = re.search(r"DIRECTAMENTE con ### S(\d+)", prompt)
            desde = int(m.group(1)) if m else 1
            # la continuación cubre lo que faltó: extiendo al 100%
            self.restantes = self.words
        else:
            desde = 1
            if self.modo == "trunco" and self.llamadas == 1:
                total = int(len(self.words) * 0.4)
            else:
                total = len(self.words)
            self.restantes = self.words[:total]
            self.consumidas = 0
        bloques, n = [], desde
        while self.consumidas < len(self.restantes):
            trozo = self.restantes[self.consumidas:
                                   self.consumidas + self.por_escena]
            self.consumidas += len(trozo)
            voz = " ".join(trozo)
            bloques.append(f"### S{n:02d}\nVOZ: {voz}\n"
                           f"VISUAL: protagonista, escena {n}.")
            n += 1
        return "\n\n".join(bloques), "mock-model"


def nuevo_proyecto(tag):
    tmp = Path(tempfile.mkdtemp(prefix=f"e2e_{tag}_"))
    p = {"id": tag, "title": f"Proyecto E2E {tag}", "job_dir": str(tmp),
         "voice": "mock:voz", "language": "es", "kind": "largo"}
    return p, tmp


def escribe_guion(tmp, n_palabras=160):
    palabras = [f"palabra{i}" for i in range(n_palabras)]
    # guion con algo de estructura para que el conteo sea realista
    texto = ("# Guion de prueba\n\n" +
             " ".join(palabras[:n_palabras // 2]) + "\n\n" +
             " ".join(palabras[n_palabras // 2:]) + "\n")
    (tmp / "GUION.md").write_text(texto, encoding="utf-8")
    return [w for w in re.sub(r"^#.*$", "", texto, flags=re.M).split()]


# ---------------- escenarios ----------------
def s1_happy_path():
    print("\n[S1] happy path: storyboard → tts → animación → ensamblado")
    p, tmp = nuevo_proyecto("s1")
    words = escribe_guion(tmp)
    tts_engine.speak_batch = mock_speak_batch
    P._generar_y_renderizar_escena = mock_render
    subprocess.run = fake_subprocess_run
    try:
        llm = MockLLMStoryboard(words, modo="completo")
        ok, log, _, _ = P.correr_etapa_garantizada(p, "storyboard", llm)
        check("storyboard ok con contrato", ok, log[-200:])
        n_esc = len(P._parse_storyboard(tmp))

        ok, log, _, _ = P.correr_etapa_garantizada(p, "tts")
        check("tts ok con contrato", ok, log[-200:])

        ok, log, _, _ = P.correr_etapa_garantizada(p, "animacion", llm)
        check("animación ok con contrato", ok, log[-200:])

        ok, log, _, _ = P.correr_etapa_garantizada(p, "ensamblado")
        check("ensamblado ok con contrato", ok, log[-200:])
        final = tmp / "video" / "final.mp4"
        srt = tmp / "video" / "final.srt"
        check("final.mp4 existe y no vacío",
              final.exists() and final.stat().st_size > 0)
        n_srt = srt.read_text(encoding="utf-8").count("-->") if srt.exists() \
            else 0
        check(f"srt cubre las {n_esc} escenas", n_srt == n_esc,
              f"srt={n_srt} escenas={n_esc}")
    finally:
        subprocess.run = _real_subprocess_run
        shutil.rmtree(tmp, ignore_errors=True)


def s2_rotacion_por_cuota():
    print("\n[S2] llm.generate rota de backend cuando se agota la cuota")
    orig_gemini = _llm._gemini_generate
    orig_oai = _llm._openai_chat
    orig_desc = _llm._descubierto
    llamadas = {"gemini": 0, "groq": 0}
    try:
        def fake_gemini(key, model, prompt, system):
            llamadas["gemini"] += 1
            raise _llm.LLMError("429 RESOURCE_EXHAUSTED: quota exceeded "
                                "for gemini-2.5-flash")
        def fake_oai(base, key, model, prompt, system, max_tokens=8192,
                     backend=""):
            llamadas["groq"] += 1
            return "TEXTO_DEL_BACKEND_DE_RESPALDO"
        _llm._gemini_generate = fake_gemini
        _llm._openai_chat = fake_oai
        _llm._descubierto = lambda b, k: []
        texto, modelo = _llm.generate(
            "hola", backend="gemini", keys={"gemini": "k1", "groq": "k2"})
        check("rotó a groq y devolvió su texto",
              texto == "TEXTO_DEL_BACKEND_DE_RESPALDO" and "groq" in modelo,
              f"modelo={modelo}")
        check("gemini se intentó antes de rotar", llamadas["gemini"] > 0)
        # caso negativo: todos caídos → error fuerte, no silencio
        _llm._openai_chat = lambda *a, **k: (_ for _ in ()).throw(
            _llm.LLMError("429 quota exceeded"))
        try:
            _llm.generate("hola", backend="gemini",
                          keys={"gemini": "k1", "groq": "k2"})
            check("todos caídos → LLMError", False, "no lanzó excepción")
        except _llm.LLMError as e:
            check("todos caídos → LLMError fuerte", "Ningún modelo" in str(e))
    finally:
        _llm._gemini_generate = orig_gemini
        _llm._openai_chat = orig_oai
        _llm._descubierto = orig_desc


def s3_truncado_se_completa():
    print("\n[S3] storyboard truncado → continuación automática lo completa")
    p, tmp = nuevo_proyecto("s3")
    words = escribe_guion(tmp, 200)
    try:
        llm = MockLLMStoryboard(words, modo="trunco")
        ok, log, _, _ = P.correr_etapa_garantizada(p, "storyboard", llm)
        check("continuación automática completó (ok)", ok, log[-160:])
        check("hubo >1 llamada al modelo (reintento real)",
              llm.llamadas > 1, f"llamadas={llm.llamadas}")
        vw, gw = P._cobertura_storyboard(p, tmp)
        check(f"cobertura ≥90% ({vw}/{gw})", gw > 0 and vw >= 0.9 * gw)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def s4_sin_voz_falla_fuerte():
    print("\n[S4] escenas sin VOZ → falla FUERTE, sin loop infinito")
    p, tmp = nuevo_proyecto("s4")
    (tmp / "STORYBOARD.md").write_text(
        "### S01\nVOZ: Escena normal uno.\nVISUAL: x.\n\n"
        "### S02\nNarración: formato que el parser no conoce.\nVisual: y.\n",
        encoding="utf-8")
    tts_engine.speak_batch = mock_speak_batch
    try:
        ok, log, _, _ = P.run_tts_stage(p, tmp)
        check("tts falla (no ok silencioso)", not ok)
        check("el mensaje lista la escena", "S02" in log, log[:120])
        check("el mensaje muestra el formato crudo", "Narración:" in log)
        kind, txt = P.reparar_faltantes(p, tmp)
        check("reparar NO declara éxito", kind == "warning", kind)
        check("reparar dice que ningún botón las arregla",
              "ningún botón" in txt)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def s5_audio_corrupto_se_regenera():
    print("\n[S5] audio corrupto → se detecta, se borra y se regenera solo")
    p, tmp = nuevo_proyecto("s5")
    words = escribe_guion(tmp, 120)
    tts_engine.speak_batch = mock_speak_batch
    try:
        llm = MockLLMStoryboard(words)
        ok, _, _, _ = P.correr_etapa_garantizada(p, "storyboard", llm)
        assert ok
        ok, _, _, _ = P.correr_etapa_garantizada(p, "tts")
        assert ok
        # corrompo un mp3 (existe, tamaño>0, ilegible): el caso S34
        audios = sorted((tmp / "audio").glob("*.mp3"))
        victima = audios[1]
        victima.write_bytes(victima.read_bytes()[:100])
        rep = P.verificar_elementos(p, tmp)["detalle"]
        check("verificar marca el corrupto como ilegible",
              victima.stem in rep["audios"]["ilegibles"])
        # reparar_faltantes (v28) lo borra y regenera SIN forzar manual.
        # Nota: devuelve "warning" porque los VIDEOS siguen faltando (la
        # etapa 7 es asistida y solo se informa); lo que importa es que los
        # audios queden bien, verificado por el contrato de abajo.
        kind, txt = P.reparar_faltantes(p, tmp)
        check("reparación regeneró el audio (solo videos pendientes)",
              "audios:" not in txt and "vo_json:" not in txt, txt[:150])
        ok, _ = P.validar_etapa("tts", p, tmp)
        check("contrato tts vuelve a cumplirse", ok)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def s6_drift_preflight():
    print("\n[S6] storyboard editado tras TTS → pre-flight con diff exacto")
    p, tmp = nuevo_proyecto("s6")
    words = escribe_guion(tmp, 120)
    tts_engine.speak_batch = mock_speak_batch
    P._generar_y_renderizar_escena = mock_render
    subprocess.run = fake_subprocess_run
    try:
        llm = MockLLMStoryboard(words)
        assert P.correr_etapa_garantizada(p, "storyboard", llm)[0]
        assert P.correr_etapa_garantizada(p, "tts")[0]
        assert P.correr_etapa_garantizada(p, "animacion", llm)[0]
        # edito el storyboard DESPUÉS del TTS (agrego escena)
        with open(tmp / "STORYBOARD.md", "a", encoding="utf-8") as f:
            f.write("\n### S99\nVOZ: Escena agregada después.\nVISUAL: z.\n")
        ok, log, _, _ = P.run_ensamblado(p, tmp)
        check("ensamblado falla (no ensambla incompleto)", not ok)
        check("el mensaje trae el diff exacto",
              "S99" in log and "vo.json" in log, log[:160])
        check("no es el críptico 'Falta el audio'",
              "Falta el audio" not in log)
    finally:
        subprocess.run = _real_subprocess_run
        shutil.rmtree(tmp, ignore_errors=True)


def s7_sin_nombres_indefinidos():
    print("\n[S7] pyflakes: sin nombres indefinidos (regresión del bug `re`)")
    try:
        from pyflakes.api import check as _pc
        from pyflakes.reporter import Reporter
        import io
    except ImportError:
        print("  ⏭️  pyflakes no instalado: escenario omitido "
              "(pip install pyflakes para activarlo)")
        return
    errores = []
    for nombre in ("pipeline.py", "app.py"):
        path = PANEL / nombre
        out, err = io.StringIO(), io.StringIO()
        _pc(path.read_text(encoding="utf-8"), nombre, Reporter(out, err))
        f821 = [l for l in (out.getvalue() + err.getvalue()).splitlines()
                if "undefined name" in l]
        errores.extend(f821)
    check("cero undefined names en pipeline.py/app.py", not errores,
          "; ".join(errores[:3]))


def s8_precheck_bloquea():
    print("\n[S8] la corrida garantizada no arranca sin insumos")
    p, tmp = nuevo_proyecto("s8")
    try:
        ok, log, _, _ = P.correr_etapa_garantizada(p, "tts")
        check("tts sin storyboard → bloqueado con mensaje claro",
              not ok and "no arranca" in log and "storyboard" in log,
              log[:140])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def s9_run_all_verde():
    print("\n[S9] run_all completo: 8 etapas en orden, veredicto honesto")
    import db as _db
    work = Path(tempfile.mkdtemp(prefix="e2e_runall_"))
    tts_engine.speak_batch = mock_speak_batch
    P._generar_y_renderizar_escena = mock_render
    subprocess.run = fake_subprocess_run
    try:
        conn = _db.connect(str(work / "t.db"))
        _db.init_db(str(work / "t.db"))
        pid = _db.add_project(conn, "E2E run_all", kind="largo",
                              voice="mock:voz", language="es")
        p = dict(_db.get_project(conn, pid))
        p["job_dir"] = str(work / "job")
        Path(p["job_dir"]).mkdir(parents=True, exist_ok=True)
        _db.ensure_stages(conn, pid,
                          ["tema", "investigacion", "guion", "verificacion",
                           "storyboard", "tts", "animacion", "ensamblado",
                           "paquete"])
        _db.ensure_approvals(conn, pid)
        _db.set_approval(conn, pid, "tema", "aprobado")
        _db.set_approval(conn, pid, "guion", "aprobado")
        words = escribe_guion(Path(p["job_dir"]))
        llm = MockLLMStoryboard(words, modo="completo")
        motivo, detalle = P.run_all(conn, p, llm)
        # debe llegar hasta el gate de miniatura (todo lo automático hecho)
        check("run_all llega al gate de miniatura",
              motivo == "gate" and detalle == "miniatura",
              f"{motivo} {detalle}")
        estados = {s["stage"]: s["status"]
                   for s in _db.list_stages(conn, pid)}
        for etapa in ("storyboard", "tts", "animacion", "ensamblado"):
            check(f"etapa {etapa} ok con contrato",
                  estados.get(etapa) == "ok", estados.get(etapa))
        check("final.mp4 existe",
              (Path(p["job_dir"]) / "video" / "final.mp4").exists())
    finally:
        subprocess.run = _real_subprocess_run
        shutil.rmtree(work, ignore_errors=True)


def s10_cobertura_ignora_markup():
    print("\n[S10] cobertura mide la narración, no el markup de producción")
    p, tmp = nuevo_proyecto("s10")
    # Guion con markup (headers, [VISUAL:], timecodes) y secciones que NO se
    # narran (FUENTES/MINIATURAS). v29.1: ese texto no debe contar.
    narracion = [f"narracion{i}" for i in range(100)]
    guion = (
        "# Guion de prueba\n\n"
        "## APERTURA (0:00–0:30)\n"
        "[VISUAL: saludo_fijo, banda_titulo, personaje(stick_point)]\n"
        + " ".join(narracion) + "\n\n"
        "[VISUAL: matraz, reloj_montage(feto_desarrollo)]\n\n"
        "## FUENTES\n"
        "- Autor, A. (2020). Un título de fuente que no se narra jamás. Journal.\n"
        "- Otro, B. (2021). Otra fuente larga que tampoco se narra nunca. J.\n\n"
        "## MINIATURAS (3 ideas)\n"
        "1. Texto: monigote con dos cerebros y flechas de colores.\n")
    (tmp / "GUION.md").write_text(guion, encoding="utf-8")
    try:
        n = P.count_words(P._narracion_guion(guion))
        check("la narración excluye [VISUAL]/headers/timecodes/FUENTES",
              n == len(narracion), f"narracion={n} esperado={len(narracion)}")
        # cuadrado: un storyboard que cubra esa narración da ≥90%
        esc = []
        i = 0
        while i < len(narracion):
            esc.append(f"### S{len(esc)+1:02d}\nVOZ: "
                       f"{' '.join(narracion[i:i+25])}\nVISUAL: x.")
            i += 25
        (tmp / "STORYBOARD.md").write_text("\n\n".join(esc), encoding="utf-8")
        vw, gw = P._cobertura_storyboard(p, tmp)
        check(f"cobertura real ≥90% ({vw}/{gw})",
              gw == len(narracion) and vw >= 0.9 * gw)
        ok, det = P.validar_etapa("storyboard", p, tmp)
        check("contrato storyboard ok (sin falso TRUNCADO)", ok, det)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    print("=" * 64)
    print("E2E Zenn Factory v29.1 — ffmpeg:", FFMPEG)
    print("=" * 64)
    s1_happy_path()
    s2_rotacion_por_cuota()
    s3_truncado_se_completa()
    s4_sin_voz_falla_fuerte()
    s5_audio_corrupto_se_regenera()
    s6_drift_preflight()
    s7_sin_nombres_indefinidos()
    s8_precheck_bloquea()
    s9_run_all_verde()
    s10_cobertura_ignora_markup()
    print("\n" + "=" * 64)
    fallos = [r for r in RESULTS if not r[1]]
    print(f"{len(RESULTS) - len(fallos)}/{len(RESULTS)} checks pasaron")
    if fallos:
        print("FALLARON:")
        for n, _, d in fallos:
            print(f"  - {n} {d}")
        sys.exit(1)
    print("TODO VERDE ✅")


if __name__ == "__main__":
    main()
