#!/usr/bin/env python3
"""Unitarios de funciones puras del pipeline (v29.2).

Cubre lo que antes solo se validaba de forma indirecta en el E2E:
_narracion_guion, build_vo_json (dedupe/sin_voz), _partir_guion,
_renumerar_desde, _audio_path/_ids_con_archivo, verificar_elementos,
fmt_mmss, count_words, estimate_minutes.

Sin red, sin keys, sin ffmpeg real (verificar_elementos parchea el probe).

Uso:  python3 test_pipeline_unit.py
Sale con código 1 si algún check falla.
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path
from unittest import mock

PANEL = Path(__file__).resolve().parent.parent / "panel"
if not (PANEL / "pipeline.py").exists():
    PANEL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PANEL))
import pipeline as P  # noqa: E402
import pipe_verify  # noqa: E402

RESULTS = []


def check(nombre, cond, detalle=""):
    RESULTS.append((nombre, bool(cond), detalle))
    print(("  ✅ " if cond else "  ❌ ") + nombre +
          (f" — {detalle}" if detalle and not cond else ""))
    return bool(cond)


# ================================================================ narracion
def test_narracion_guion_quita_markup():
    guion = """## BLOQUE 1 · Intro (0:00–0:45)

[VISUAL: animación de portada con el título]

¿Alguna vez te preguntaste por qué la gente escribe con la mano izquierda?

## FUENTES
- Smith (2020)
- Doe (2021)
"""
    out = P._narracion_guion(guion)
    check("narracion: quita [VISUAL]", "[VISUAL" not in out)
    check("narracion: quita timecodes", "0:00" not in out)
    check("narracion: quita seccion FUENTES", "Smith" not in out and
          "FUENTES" not in out)
    check("narracion: conserva la frase narrada",
          "¿Alguna vez te preguntaste" in out)
    check("narracion: quita encabezados ##",
          not any(ln.startswith("##") for ln in out.splitlines()))


def test_narracion_guion_lineas_sueltas():
    guion = """---
[ESCENA: plano general]
Texto narrado normal.
[PLANO: detalle]
Otra frase que sí se narra.
"""
    out = P._narracion_guion(guion)
    check("narracion: quita [ESCENA:", "[ESCENA" not in out)
    check("narracion: quita [PLANO:", "[PLANO" not in out)
    check("narracion: quita ---", "---" not in out)
    check("narracion: conserva ambas frases",
          "Texto narrado" in out and "Otra frase" in out)


def test_narracion_guion_no_quita_narracion_real():
    guion = """## BLOQUE 2 · Desarrollo (1:00–3:30)

[VISUAL: gráfico de barras]

La mano dominante se relaciona con la corteza motora contralateral.

Estudios de imagen muestran asimetrías en el cuerpo calloso.
"""
    out = P._narracion_guion(guion)
    check("narracion: conserva parrafos narrados",
          "corteza motora" in out and "cuerpo calloso" in out)


def test_narracion_guion_vacio():
    check("narracion: vacio → vacio", P._narracion_guion("") == "")
    check("narracion: solo markup → vacio",
          P._narracion_guion("## FUENTES\n- x\n") == "")


# ================================================================ palabras
def test_count_words():
    check("count_words: basico", P.count_words("hola mundo") == 2)
    check("count_words: con acentos y ñ",
          P.count_words("pingüino señor") == 2)
    check("count_words: ignora numeros", P.count_words("123 456") == 0)
    check("count_words: vacio", P.count_words("") == 0)


def test_estimate_minutes():
    check("estimate_minutes: 155 ppm", abs(P.estimate_minutes(155) - 1.0) < 1e-9)
    check("estimate_minutes: 0", P.estimate_minutes(0) == 0.0)


def test_fmt_mmss():
    check("fmt_mmss: 0", P.fmt_mmss(0) == "00:00")
    check("fmt_mmss: 90", P.fmt_mmss(90) == "01:30")
    check("fmt_mmss: None→00:00", P.fmt_mmss(None) == "00:00")


# ================================================================ partir
def test_partir_guion_respeta_parrafos():
    parrafo = " ".join(["palabra"] * 100)
    script = f"{parrafo}\n\n{parrafo}\n\n{parrafo}"
    partes = P._partir_guion(script, max_palabras=150)
    check("partir: ≥2 partes", len(partes) >= 2)
    check("partir: ninguna parte excede max*1.3",
          all(len(pt.split()) <= 150 * 1.3 for pt in partes))


def test_partir_guion_corta_parrafo_gigante():
    frase = "Esta es una frase de prueba para el corte. "
    parrafo = frase * 120  # ~960 palabras, supera max_palabras=650
    partes = P._partir_guion(parrafo, max_palabras=650)
    check("partir: parrafo gigante → varias partes", len(partes) > 1)
    check("partir: no pierde texto (uniones ≈ original)",
          sum(len(pt.split()) for pt in partes) >= 0.95 * len(parrafo.split()))


def test_partir_guion_vacio():
    check("partir: vacio → lista vacia", P._partir_guion("") == [])


# ================================================================ renumerar
def test_renumerar_desde():
    text = "### S01\na\n### S02\nb\n### S03\nc\n"
    out = P._renumerar_desde(text, 45)
    check("renumerar: S01→S45", "### S45" in out)
    check("renumerar: S03→S47", "### S47" in out)
    out2 = P._renumerar_desde(out, 48)
    check("renumerar: segunda pasada no rompe S45", "### S45" in out2 or
          "### S48" in out2)


# ================================================================ audio path
def test_audio_path():
    with tempfile.TemporaryDirectory() as td:
        job = Path(td)
        ap = P._audio_path(job, "S07")
        check("audio_path: minusculas", str(ap).endswith("audio/s07.mp3") or
              str(ap).endswith("audio\\s07.mp3"))
        ap2 = P._audio_path(job, "s07")
        check("audio_path: idempotente", ap == ap2)


def test_ids_con_archivo():
    with tempfile.TemporaryDirectory() as td:
        carpeta = Path(td)
        (carpeta / "s01.mp3").write_bytes(b"x" * 100)
        (carpeta / "s02.mp3").write_bytes(b"")  # vacio → faltante
        (carpeta / "s04.mp3").write_bytes(b"y" * 50)
        tienen, faltan = P._ids_con_archivo(
            ["s01", "s02", "s03", "s04"], carpeta, ".mp3")
        check("ids_con_archivo: tienen correctos", tienen == ["s01", "s04"])
        check("ids_con_archivo: faltan correctos", faltan == ["s02", "s03"])


# ================================================================ vo.json
def test_build_vo_json_dedupe():
    with tempfile.TemporaryDirectory() as td:
        job = Path(td)
        sb = """### S01
**VOZ:** Primera escena con narración suficientemente larga.
**VISUAL:** animación A

### S01
**VOZ:** Duplicado repetido que debe descartarse del vo.json.
**VISUAL:** animación B

### S02
**VOZ:** Segunda escena distinta con narración también suficientemente larga.
**VISUAL:** animación C
"""
        (job / "STORYBOARD.md").write_text(sb, encoding="utf-8")
        n, origen, sin_voz = P.build_vo_json({"id": 1, "kind": "largo",
                                              "title": "t"}, job)
        check("vo_json: dedupe → 2 items", n == 2, f"n={n}")
        check("vo_json: origen=storyboard", origen == "storyboard")
        check("vo_json: sin_voz vacio", sin_voz == [])
        data = json.loads((job / "vo.json").read_text(encoding="utf-8"))
        ids = [d["id"] for d in data]
        check("vo_json: ids únicos", ids == ["s01", "s02"], str(ids))
        check("vo_json: conserva primera aparicion",
              "Primera escena" in data[0]["text"])


def test_build_vo_json_sin_voz_reportado():
    with tempfile.TemporaryDirectory() as td:
        job = Path(td)
        sb = """### S01
**VOZ:** Escena con voz legible y narración suficientemente larga.
**VISUAL:** ok

### S02
**VISUAL:** esta escena no tiene VOZ reconocible
"""
        (job / "STORYBOARD.md").write_text(sb, encoding="utf-8")
        n, origen, sin_voz = P.build_vo_json({"id": 2, "kind": "largo",
                                              "title": "t"}, job)
        check("vo_json: sin_voz incluye s02", sin_voz == ["s02"],
              str(sin_voz))
        check("vo_json: solo s01 en items", n == 1, f"n={n}")


# ================================================================ verificar
def _job_completo(td):
    job = Path(td) / "jobs"
    (job / "video" / "scenes").mkdir(parents=True)
    (job / "audio").mkdir(parents=True)
    sb = """### S01
**VOZ:** Primera escena con narración suficientemente larga para el test.
**VISUAL:** animación A

### S02
**VOZ:** Segunda escena distinta con narración también suficientemente larga.
**VISUAL:** animación B
"""
    (job / "STORYBOARD.md").write_text(sb, encoding="utf-8")
    (job / "vo.json").write_text(
        json.dumps([{"id": "s01", "text": "x" * 60},
                    {"id": "s02", "text": "y" * 60}]), encoding="utf-8")
    for sid in ("s01", "s02"):
        (job / "audio" / f"{sid}.mp3").write_bytes(b"\xff\xfb" + b"\x00" * 200)
        (job / "video" / "scenes" / f"{sid}.mp4").write_bytes(b"\x00" * 500)
    (job / "video" / "final.mp4").write_bytes(b"\x00" * 1000)
    return job


def test_verificar_elementos_todo_ok():
    with tempfile.TemporaryDirectory() as td:
        job = _job_completo(td)
        with mock.patch.object(pipe_verify, "_probe_duration",
                               return_value=5.0):
            rep = P.verificar_elementos({"kind": "largo"}, job)
        check("verificar: ok=True con todo presente", rep["ok"] is True,
              rep["resumen"])


def test_verificar_elementos_faltan_audios():
    with tempfile.TemporaryDirectory() as td:
        job = _job_completo(td)
        (job / "audio" / "s02.mp3").unlink()
        with mock.patch.object(pipe_verify, "_probe_duration",
                               return_value=5.0):
            rep = P.verificar_elementos({"kind": "largo"}, job)
        check("verificar: ok=False con audio faltante", rep["ok"] is False)
        check("verificar: reporta s02 faltante",
              "s02" in rep["detalle"]["audios"]["faltan"])


def test_verificar_elementos_audio_vacio():
    with tempfile.TemporaryDirectory() as td:
        job = _job_completo(td)
        (job / "audio" / "s01.mp3").write_bytes(b"")
        with mock.patch.object(pipe_verify, "_probe_duration",
                               return_value=5.0):
            rep = P.verificar_elementos({"kind": "largo"}, job)
        check("verificar: mp3 vacio cuenta como faltante",
              "s01" in rep["detalle"]["audios"]["faltan"])


def test_verificar_elementos_audio_ilegible():
    with tempfile.TemporaryDirectory() as td:
        job = _job_completo(td)
        with mock.patch.object(pipe_verify, "_probe_duration",
                               side_effect=lambda p: 0.0):
            rep = P.verificar_elementos({"kind": "largo"}, job)
        check("verificar: probe 0 → ilegible", rep["ok"] is False)
        check("verificar: lista ilegibles",
              len(rep["detalle"]["audios"]["ilegibles"]) >= 1)


# ================================================================ main
def main():
    print("=" * 60)
    print("UNITARIOS DE FUNCIONES PURAS · pipeline")
    print("=" * 60)
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        print(f"\n[{name}]")
        try:
            fn()
        except Exception as e:
            check(f"{name}: excepción inesperada", False, repr(e))
    total = len(RESULTS)
    fails = [r for r in RESULTS if not r[1]]
    print("\n" + "=" * 60)
    print(f"{total - len(fails)}/{total} checks pasaron")
    if fails:
        print("FALLAS:")
        for n, _, d in fails:
            print(f"  ❌ {n} — {d}")
        sys.exit(1)
    print("TODO VERDE ✅")
    sys.exit(0)


if __name__ == "__main__":
    main()
