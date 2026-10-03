# Zenn Factory — Panel «El Porqué» · Documentación completa

**Qué es:** una fábrica local de videos de divulgación científica estilo
Zenn (una pregunta por video, 8–12 minutos, monigotes animados, fuentes
reales). Todo corre en tu máquina: panel web local (Streamlit + SQLite),
guiones con LLM gratuitos o locales, voz neuronal, animación Manim,
subtítulos y miniaturas — punta a punta con tres aprobaciones tuyas:
**tema, guion y miniatura**.

```
Tema → Investigación → Guion ✋ → Storyboard → Voz → Animación →
Ensamblado (+SRT) → Miniaturas ✋ → Paquete de publicación → (Short ✋)
                              ✋ = puerta de aprobación humana
```

---

## 1. Instalación

**Requisitos:** Windows 10/11 · Python 3.11 (o `uv`) · ffmpeg en el PATH ·
internet para los LLM en nube y la voz Edge · Ollama (opcional, modelos
locales).

1. Descomprime el ZIP en tu carpeta (p. ej. `video-gen/`). **No borres tu
   `panel.db`**: ahí viven tus proyectos y tus API keys.
2. Doble clic en `INICIAR.bat`. Crea `.venv`, instala dependencias
   (incluye Manim y los motores de voz), crea la BD la primera vez y abre
   **http://localhost:8501**.
3. En **Configuración**: pega tus API keys y elige modelo y voz por
   defecto.

> Actualizar de una versión anterior = descomprimir encima, sin tocar
> `panel.db`, y correr `INICIAR.bat` (instala lo que falte solo).

## 2. Modelos LLM (guion, storyboard, escenas, miniaturas)

Orden de preferencia del router (con fallback automático en cadena):

| # | Backend | Tier gratuito | Modelos destacados |
|---|---------|---------------|--------------------|
| 1 | Google AI Studio (Gemini) | ~1.500 req/día Flash, sin tarjeta | gemini-2.5-flash |
| 2 | Groq | 1.000 req/día por modelo | openai/gpt-oss-120b, qwen3.8-27b |
| 3 | Token Harbor | solo ids `:free` (7×24 h por cuenta) | catálogo descubierto filtrado por `:free` |
| 4 | FreeLLMAPI | 10.000 tokens al crear la key | glm-5.2, glm-4.7, kimi-k3, qwen3.8-max-preview |
| 5 | DeepSeek oficial | de pago (tarifa por token) | deepseek-chat, deepseek-reasoner |
| 6 | Cerebras | ~1M tokens/día, el más rápido | lineup rotativo |
| 7 | OpenRouter `:free` | 50 req/día (1.000 con $10) | nemotron-3-super, gemma-4 |
| 8 | Mistral (Experiment) | ~1B tok/mes (aceptas training) | mistral-large |
| 9 | Cohere (trial) | 1.000 llamadas/mes | command-r |
| 10 | Ollama local | ∞, sin internet | qwen3.6, video-factory-qwen |

- **Token Harbor** (`https://tokenharbor.ai/v1`, key `thk_live_…`): el combo
  **solo** muestra ids que terminan en `:free`; los de pago jamás entran en
  la cadena, así que no se descuadra la wallet.
- **FreeLLMAPI** (`https://api.freellmapi.ai/v1`, key `sk_live_…`): todo su
  catálogo sale de la bolsa de 10.000 tokens gratis.
- **DeepSeek oficial** (`https://api.deepseek.com/v1`): el único de pago de
  la lista, para cuando quieras `deepseek-chat` sin intermediarios.
- Las tres claves se pegan en **Configuración → Claves de LLM**, igual que
  el resto; el panel descubre los modelos con `/models` en cuanto hay key.

- ⚠️ **Gemini:** si activas facturación en el proyecto de Google,
  **pierdes el tier gratuito**. Déjalo sin facturación.
- **Groq** bloquea el User-Agent por defecto de Python (HTTP 403/1010);
  el panel ya envía un UA de navegador (corregido en v3/v4).
- Con tu hardware (GTX 1050 4 GB, i7-7700HQ, 32 GB RAM) Ollama va en
  **CPU**: el punto dulce es un modelo de ~14B cuantizado; los de 27–32B
  generan a 2–3 tok/s (un guion puede tardar 10–15 min). Para código de
  escenas Manim, tus mejores locales son `qwen3.6` y
  `video-factory-qwen`.

### Modelos locales instalados (validados 2026-10-02)

Lánzalos con **`ARRANCAR_OLLAMA.bat`** (o desde `INICIAR.bat`, que lo
llama solo): fuerza `OLLAMA_LLM_LIBRARY=cpu`, porque el driver NVIDIA
546.29 de 2023 no compila el PTX de los builds CUDA actuales →
*"PTX JIT compilation failed"* y **ningún modelo arranca**. Con driver
560+ puedes borrar esas dos líneas y usar la GTX 1050.

| Modelo | Peso | Generación | Para qué sirve |
|---|---|---|---|
| `qwen3.5:4b` | 3,2 GB (4,7B) | ~5,9 tok/s | el más rápido: borradores, ideas, resúmenes |
| `gemma4:e4b` / `gemma4` | 8,9 GB (8B) | ~5,3–5,8 tok/s | guiones y texto general (buena calidad ES) |
| `gemma-test` | 8,9 GB (8B) | ~5,8 tok/s | alias de prueba de gemma4 |
| `gemma4:12b` | 7,0 GB (11,9B) | ~2,3 tok/s | mejor calidad, pero lento |
| `qwen3.6` | 22,3 GB (36B MoE) | ~3,6 tok/s (+78 s de carga) | escenas Manim; solo para llamadas puntuales |
| `video-factory-qwen` | 8,9 GB (8B) | ~5,6 tok/s | fine-tune: devuelve JSON `scene_description`/`narration`, **no** texto libre |
| `nomic-embed-text` | 0,3 GB | — | embeddings; no aparece en el combo |

Cómo usarlos desde la app: **sidebar 🎛 Modelo → Backend «Ollama ·
local» → Modelo** (el combo lista lo instalado, menos embeddings) →
«Guardar como predeterminado» → «Correr todo». El panel les pide
`think: false`: sin eso los modelos híbridos (qwen3.x/gemma4) se
piensen la respuesta entera y `content` vuelve vacío.

## 3. Voces: que suene humano (y hombre o mujer)

La voz del proyecto es un *spec* `motor:voz`, elegido en
**Configuración → Motor de voz / Voz** (aplica a proyectos nuevos; cada
proyecto guarda la suya).

| Motor | Calidad | Internet | Coste | Voces ES |
|-------|---------|----------|-------|----------|
| **Edge Neural** (default) | La más humana: neurales de Microsoft | Sí | Gratis, sin key | Dalia ♀ MX · Jorge ♂ MX · Elvira ♀ ES · Álvaro ♂ ES |
| **Kokoro 82M** | Natural, local | No | Gratis | Dora ♀ ES · Alex ♂ ES · Santa ♂ ES |
| **Piper** | Correcta, algo robótica, rapidísima en CPU | No | Gratis | Sharvard ♀ ES · Claude ♀ MX · DaveFX ♂ ES · Ald ♂ MX |
| Aria (Meta) | Legacy, solo entorno Hatch | — | — | Aria ♀ |

**Por qué suena menos “IA” ahora:**
1. Voces **neurales** de verdad (Edge) en vez de síntesis básica.
2. **Normalización de volumen** automática (ffmpeg `loudnorm` a −16 LUFS)
   al generar cada audio: sin saltos ni plano “de robot”.
3. La narración va **por frases** (una tarjeta por frase): pausas
   naturales del propio modelo neural.
4. Truco de guion: frases cortas y puntuación expresiva (¿? ¡! …) — el
   motor neural la convierte en entonación.

**Kokoro (opcional, 100% local):** no viene en `requirements.txt` porque
descarga ~2 GB (PyTorch). Para activarlo:
```
.venv\Scripts\pip install kokoro soundfile
```
y instala **espeak-ng** (https://github.com/espeak-ng/espeak-ng/releases,
el `.msi` de Windows). Sin espeak-ng, el español de Kokoro falla.

**Piper** descarga la voz elegida automáticamente la primera vez
(carpeta `piper_voices/`).

## 4. Las 10 etapas, en orden

| # | Etapa | Qué hace | Salida |
|---|-------|----------|--------|
| 1 | Investigación | LLM redacta contexto y ángulos | `INVESTIGACION.md` |
| 2 | Guion | Borrador con PROMPT_MAESTRO → **apruebas tú** ✋ | `GUION.md` |
| 3 | (crítica) | Botón «Reescribir con crítica»: 2ª pasada | `GUION.md` |
| 4 | Storyboard | Escenas S01… con VOZ: y VISUAL: | `STORYBOARD.md` |
| 5 | Voz | Crea `vo.json` solo y narra con el motor elegido | `audio/*.mp3` |
| 6 | Animación | El LLM genera código Manim por escena con el rig; render + autorreparación (2 reintentos con el error) | `video/scenes/*.mp4` |
| 7 | Ensamblado | El audio manda: concat + SRT por frases + versión con subtítulos quemados | `final.mp4`, `final.srt`, `final_con_subtitulos.mp4` |
| 8 | Miniaturas | 3 variantes ilustradas → **eliges tú** ✋ | `thumb_<id>_*.png` |
| 9 | Paquete | Todo el material de publicación (ver §7) | `PAQUETE.md` |
| 10 | Short | Recorte vertical 1080×1920 del largo | `short.mp4` |

**«Correr todo»** avanza en orden y **se detiene** en las puertas
(guion y miniatura) y si algo falla, con la causa en pantalla. Las
escenas ya renderizadas no se repiten al reintentar.

## 5. Sistema visual v2 (rig)

`scripts/zenn_rig.py` es la librería de dibujo. El LLM **solo** puede
usar el rig (si genera monigotes “a mano”, el panel lo rechaza sin
gastar render y le pide corregirlo).

- **Monigote con cara:** `expresion(fig, tipo)` — normal, feliz,
  preocupado, sorpresa, triste, miedo, dormido.
- **Props con color:** `perro()`, `gato()`, `dino()`, `fuego()`,
  `lapida()`, `curva()` (gráfica con punto rojo), `planeta()`,
  `casco_vikingo()`, `hueso()`, `vela()`, `moneda_dorada()` + los
  clásicos (reloj, calendario, pastel, casa, oficina…).
- **Fondos:** `fondo(INK)` + `estrellas()` + `luna()` para noche/espacio
  (monigotes en `color=WHITE`).
- El prompt de escenas exige **2–4 elementos por escena**, expresión
  acorde a la narración y movimiento (entradas, caminar, señalar).
- Manim es **CPU-bound**: tu GTX 1050 no interviene; un video de
  15–40 escenas tarda minutos, no horas.

**Subtítulos:** parte inferior centrada, fuente Gochi Hand **tamaño 17**
(antes 24 — demasiado grandes), contorno fino, tarjetas de 1 frase
(máx. 2 líneas de ~44 caracteres). El `.srt` suelto sirve además como
transcripción para YouTube (SEO: súbelo como subtítulos del video).

## 6. Miniaturas v3

- 3 variantes generadas con Pillow (estilo dibujado a mano, con jitter):
  fondos amarillo / negro / blanco, poses distintas y **cara expresiva**
  en el monigote (feliz / sorpresa / preocupado).
- **Props detallados nuevos:** cara de perro, cabeza de T-Rex con
  dientes, dragón echando fuego, curva con punto rojo, lápida, luna —
  además de reloj, cerebro, tierra, cohete, agujero negro, etc.
- Reglas que el sistema aplica solo:
  - Texto de **3–5 palabras** que **siempre incluye el sustantivo clave**
    del tema (nada de frases cortadas en “…CAYERAS EN UN”).
  - Legible a 120 px: texto enorme, objeto grande, alto contraste.
  - El concepto lo propone el LLM; sin LLM hay fallback por palabras
    clave del título.

## 7. Publicación: el paquete viral

La etapa **Paquete** genera en `PAQUETE.md` todo lo necesario, con las
prácticas actuales de YouTube ya aplicadas:

- **3 títulos** (≤60 caracteres útiles, palabra clave al frente, gancho
  honesto — el CTR sin retención no sirve).
- **Descripción estilo Zenn:** 2 líneas de gancho (lo visible sin
  desplegar) → resumen → **“LO QUE VERÁS”** → capítulos → **fuentes**
  → 3 hashtags. Zenn cierra además con una línea de *keywords*.
- **Capítulos reales:** marcas calculadas de los audios (no inventadas);
  eliges 5–8. Los capítulos crean *key moments* en Google.
- **Comentario fijado:** una pregunta abierta que invite a responder
  (no repite el título).
- **Post de comunidad** anunciando el video.
- **Short sugerido:** la escena con más gancho para recortar (30–45 s).
- **Pantalla final:** qué enlazar al terminar.

**El triángulo del empaque** (la regla que más mueve el CTR):
*texto de la miniatura = gancho del título = primera frase del video.*
Si uno de los tres promete otra cosa, la retención se cae.

**Checklist al publicar:**
1. Título de las 3 opciones + miniatura elegida (coherentes entre sí).
2. Descripción pegada completa; capítulos con primera marca `0:00`.
3. Sube `final.srt` como subtítulos en español (además del video).
4. Fija el comentario generado. Responde comentarios la primera hora.
5. Publica el Short-recorte 24–48 h después, enlazando al largo.
6. Cadencia: **2 videos/semana**, mismo horario. Juzga el canal tras
   **20–30 videos**, no antes.
7. Métricas que mandan: **CTR** (miniatura+título) y **retención**
   (gancho de los primeros 30 s y ritmo visual).

## 8. Nombres para el canal (5 alternativas a «El Porqué»)

| Nombre | Por qué funciona | Riesgo |
|--------|------------------|--------|
| **¿Y Eso Por Qué?** | Es la frase exacta que la audiencia dice y busca; formato pregunta = clic | Handle largo (@YEsoPorque) |
| **Mente Preguntona** | Marca propia, memorable, tono familiar amplio | Menos “buscable” al inicio |
| **Por Qué Será** | Coloquial mexicano, muy pegajoso, corto | Puede sonar a cumbia/chisme |
| **Duda Científica** | Describe el nicho; “científica” posiciona en búsquedas de ciencia | Suena a tarea escolar |
| **La Pregunta del Día** | Promete hábito diario; formato claro | Genérico; competencia de medios |

**Mi recomendación:** si el objetivo nº 1 es que el algoritmo y las
búsquedas te encuentren, **«¿Y Eso Por Qué?»** gana (la pregunta ES la
búsqueda). Si prefieres marca a largo plazo, quédate con **«El
Porqué»** y compensa con títulos siempre en forma de pregunta. Verifica
handle y que no exista un canal grande con el nombre antes de cambiar.

## 9. Solución de problemas

| Síntoma | Causa / arreglo |
|---------|-----------------|
| Etapa marca error sin causa clara | El log de la etapa trae el motivo (v2+): léelo antes de reintentar |
| Groq devuelve 403/1010 | User-Agent bloqueado por Cloudflare — ya corregido; actualiza el panel |
| “No encuentro Manim” | Corre `INICIAR.bat`: instala `requirements.txt` si falta algo |
| La voz Edge falla | Sin internet o endpoint ocupado: reintenta, o cambia a Piper/Kokoro (locales) |
| Kokoro falla en español | Falta espeak-ng en el sistema (ver §3) |
| Ensamblado falla | ffmpeg/ffprobe no están en el PATH |
| El LLM ignora el rig | El panel lo detecta y reintenta solo (máx. 2 por escena); si persiste, cambia de modelo (gpt-oss-120b y qwen3.6 obedecen mejor) |
| Puerto 8501 ocupado | Cierra el otro Streamlit o cambia `--server.port` |

## 10. Estructura de archivos

```
video-gen/
├─ app.py · db.py · llm.py · pipeline.py · seed.py
├─ tts_engine.py · tts_runner.py     ← voces
├─ INICIAR.bat · requirements.txt · PROMPT_MAESTRO.md
├─ panel.db                          ← TUS datos y keys (no compartir)
├─ scripts/zenn_rig.py               ← librería de dibujo
├─ fonts/GochiHand.ttf
├─ thumbnails/generate_thumbnails.py
└─ jobs/<id>/  GUION.md · STORYBOARD.md · vo.json · audio/ ·
              scripts/ · video/ (final.mp4, final.srt, …) · PAQUETE.md
```

## 11. Hoja de ruta

- [ ] Conector real de sugerencias con YouTube Data API (cuota gratis).
- [ ] Shorts independientes verticales generados (hoy: recorte del largo).
- [ ] Validación de fuentes contra PubMed/Crossref (hoy: extracción).
- [ ] Énfasis de palabras sincronizado en pantalla (word-timing).
- [ ] A/B de miniaturas con las 3 variantes tras publicar.

*Versión del panel: v4 (voces multi-motor, rig v2, subtítulos pulidos,
miniaturas v3, paquete viral).*
