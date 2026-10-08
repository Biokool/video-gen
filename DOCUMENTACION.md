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
| Gemini 429 «exceeded your current quota» | El panel ya no quema los 3 intentos: salta solo al siguiente modelo de la cadena |
| Código de escena sale cortado (Groq) | OTPM 1000: el panel pide escenas compactas (1200 tokens) y pausa 6 s entre escenas; si una escena falla por eso, reintenta la etapa (las hechas se omiten) |
| No sé si está corriendo o cuánto falta | v5: el sidebar muestra **▶ CORRIENDO** en rojo, cada etapa larga abre un panel con **barra de progreso y ETA** («S12/24 · ~3m20s restantes») y al terminar guarda la **duración** en su tarjeta |

## 10. Estructura de archivos

```
video-gen/
├─ app.py · db.py · llm.py · pipeline.py · seed.py
├─ tts_engine.py · tts_runner.py     ← voces
├─ INICIAR.bat · ARRANCAR_OLLAMA.bat · requirements.txt · PROMPT_MAESTRO.md
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

## 12. Cambios v5 (2026-10-03)

- **Progreso visible con ETA:** TTS, animación, ensamblado y miniaturas
  reportan elemento por elemento («S12/24 · ~3m20s restantes»); el
  sidebar muestra **▶ CORRIENDO** y bloquea doble-clic; cada tarjeta de
  etapa guarda su **duración** al terminar.
- **Cuotas inteligentes:** `_rate_kind()` distingue «esperar» (cuota por
  minuto → reintenta el mismo modelo) de «saltar» (cuota diaria /
  facturación, p. ej. el 429 de Gemini → pasa al siguiente modelo sin
  quemar intentos).
- **Groq OTPM:** presupuesto de 1200 tokens por escena, prompt de código
  compacto y pausa de 6 s entre escenas.
- **Backends nuevos** (de la sesión 2026-10-02): Token Harbor, FreeLLMAPI
  y DeepSeek oficial + `ARRANCAR_OLLAMA.bat` (Ollama en modo CPU: el
  driver NVIDIA 546.29 no compila PTX).
- **Firmas reales del rig** en los prompts (`ast` sobre zenn_rig.py):
  el modelo ya no inventa parámetros.
- Selector de **voz amable** también en la config de cada proyecto.

## 12. Cambios v6 (2026-10-03)

- **Composición anti-encimados:** el rig trae `banda_titulo()`,
  `titulo_seguro()` y `etiqueta()` con **auto-ajuste** (el texto se encoge
  solo: imposible que se corte en los bordes) y `etiqueta()` nunca baja a
  la zona de subtítulos (y ≥ −1.85). El prompt de escenas incluye reglas
  de COMPOSICIÓN obligatorias: zona de subtítulos reservada (y < −2.4),
  un elemento grande por zona, ≥1.5 unidades de separación, nada tapa nada.
- **Estilo más ilustrado** (referencia Memorias de Pez): `personaje()`
  (cuerpo de color + cara), `pez()`, `matraz()`, `ojo_grande()`,
  `tarjeta_canal()` para apertura/cierre, y paleta MOSTAZA/CORAL/
  AZUL_MARINO/CREMA.
- **Guion con retención:** PROMPT_MAESTRO v2 — saludo fijo de apertura +
  hook en 15 s, 3–4 picos de información, open loops por bloque, matices
  de narración, mezcla ciencia + cultura alternativa, despedida fija
  ("...para resolver el siguiente porqué"). El storyboard usa la primera
  escena para la bienvenida y la última para la despedida; la crítica
  revisa apertura, picos, cierre y **ortografía** (tildes).
- **Aviso ortográfico automático:** la verificación lista palabras con
  è/ò/à/ù (no existen en español) antes del TTS.
- **Temas:** el generador mezcla curiosidades científicas, cultura
  alternativa y preguntas cotidianas, con formato de título de alto CTR.

## 13. Cambios v6.1 (2026-10-03)

- **Bug de cuotas Groq:** el error `tokens per day (TPD)` se clasificaba
  como límite temporal (`wait`) en vez de cuota diaria (`skip`): el panel
  esperaba 30 s y reintentaba el MISMO modelo agotado 3 veces por escena.
  Ahora `tokens per day`/`tpd` → `skip` (verificado con el mensaje real).
- **Transparencia de consumo:** la etapa de animación estima los tokens al
  inicio (`~N escenas × ~2.6K tokens`) y avisa del límite Groq gratuito
  (200K/día). Si todas las fallas son de cuota, el resumen lo dice
  explícito y sugiere cambiar de backend o reanudar otro día.
- Integrados los cambios de Chino: catálogos de modelos gratuitos
  renovados en vivo (2026-10-03) e INICIAR.bat con detección de panel
  ya corriendo.

## 14. Cambios v6.2 (2026-10-03)

- **Ritmo por defecto:** el storyboard ahora pide escenas CORTAS de 8–12
  segundos (~25–35 palabras de VOZ, ~50–60 escenas por video de 10 min).
  Más cortes = más dinamismo = más retención. Es el comportamiento
  estándar, no una opción.
- **Anti-truncado:** la etapa de storyboard verifica cobertura (palabras de
  VOZ vs. palabras del guion); si cubre menos del 70%, avisa explícito
  para reintentar con otro backend.
- Nota honesta: más escenas = más tokens (~2.6K por escena). Con 50–60
  escenas, Groq gratis (200K/día) se agota en un video; la estimación de
  tokens al inicio de la animación lo muestra. Estrategia: repartir etapas
  entre días, rotar backends u Ollama local para animación.

## 15. Cambios v7 (2026-10-04)

- **Protagonista oficial** (rig v4, según character sheets del canal):
  `protagonista(pos, playera, altura, expresion, pose)` — cabezón de ojos
  grandes, playera de color, extremidades negras. 15 expresiones
  (feliz, alegria_pura, triste, enojado, sorpresa, mente_explotada,
  pensando, confundido, miedo, decidido, euforico, cansado, dormido,
  nervioso, sarcastico), 5 poses (de_pie, senalando, brazos_cruzados,
  caminando, corriendo), 10 colores de playera. `cambiar_cara(prota,
  tipo)` cambia la expresión en el acto; `version_prota(n)` ataja las
  versiones de la sheet (1=intro naranja … 8=final teal). Es OBLIGATORIO
  en todas las escenas (storyboard + prompt de escenas).
- **Miniaturas** con el protagonista (`prota_thumb` en PIL): cabezón +
  playera de color por variante, cara siempre legible en cualquier fondo.
- **Temas que venden:** TOPIC_PROMPT con las 6 fórmulas ganadoras
  analizadas de Ink Explainer / Simple Paint / theblurb / Aussie Finance
  (pregunta con hueco, 2ª persona + secreto, cifra + quiebre,
  supervivencia, superlativo honesto, comportamiento animal) + formato
  serie "en cada nivel de X". Informe completo en
  `docs/ANALISIS_CANALES.md`. Diferenciadores: español (hueco vacío),
  fuentes reales citadas, ritmo 8–12s, playera por tema.

## 16. Cambios v7.1 (2026-10-04)

- **Protagonista alargado** (rig v4.1, más fiel a las character sheets):
  piernas y brazos largos, torso estrecho, cuello negro, mangas pequeñas.
  Proporciones: cabeza 40% de la altura, piernas ~38%.
- **Contrato `playera` por string:** el LLM puede usar
  `playera="naranja"` / `"azul"` / `"verde"` / `"roja"` / `"amarilla"` /
  `"rosa"` / `"teal"` / `"morada"` / `"negra"` / `"blanca"`
  (también valen las constantes `PLAYERA_*`). El RIG_API del prompt de
  escenas ya documenta el string en español.
- **Miniaturas PIL** con las mismas proporciones alargadas.

## 17. Cambios v7.2 (2026-10-04)

- **Sin mangas:** la playera es torso redondeado limpio, brazos negros
  directos al hombro (las mangas separadas se veían raras).
- **Cara con más definición:** ojos más grandes y juntos (como las
  sheets), pupilas y brillo mayores, bocas ~20% más grandes y más bajas
  (la boca abierta ya no tapa las pupilas), cejas más gruesas.
- Miniaturas PIL igual: sin mangas, ojos más grandes.

## 18. Cambios v8 (2026-10-04)

**Anti-encimados (garantizado por construcción):**
- El validador de código de escena rechaza por AST más de UNA llamada a
  `banda_titulo()/titulo_seguro()/title_card()/tarjeta_canal()/callout()`
  por escena → cuenta como intento y dispara autorreparación. Las bandas
  ya no pueden taparse entre sí.
- El protagonista (`protagonista()`/`version_prota()`) ahora sí es
  obligatorio por construcción: el código sin él se rechaza.
- `callout()` y `split_screen()` ahora auto-ajustan el texto (antes
  `callout` podía salirse de la pantalla y cortarse en los bordes).

**Reloj maestro y duración garantizada:**
- La etapa 8 (Ensamblado) compara el storyboard contra los mp4 existentes:
  si falta alguna escena, FALLA con la lista exacta en vez de construir
  un video corto en silencio.
- Aviso cuando un video de escena dura <30% de su audio (el ensamblado
  rellena con imagen congelada; conviene regenerar esa escena).

**Re-animar una escena:**
- Nuevo botón en la etapa 7: escribe `S07` y re-anima solo esa escena.
  Con «Regenerar código con LLM» activado gasta tokens de 1 escena;
  desactivado re-renderiza el `.py` existente con CERO tokens (ideal tras
  actualizar el rig). Después re-ejecuta la etapa 8.

## 19. Cambios v9 (2026-10-04)

**Caso real proyecto 25 (89 escenas, Groq 200K TPD):**
- 89 escenas × ~2.8K tokens ≈ 250K > 200K: en Groq gratis un proyecto así
  NO termina en un día. El panel ahora lo dice por adelantado en la
  estimación y propone repartir en 2 días u Ollama local.

**Alto en seco por cuota:**
- Antes: al agotarse la cuota, la etapa seguía escena por escena fallando
  en cascada ("brincando", 18 min quemados). Ahora: al primer fallo de
  cuota/rate-limit la etapa 7 se DETIENE, dice en qué escena paró y cuántas
  faltan. Reanudar es un clic (las hechas se omiten solas).

**Log completo por ejecución:**
- Cada corrida de animación, ensamblado y TTS guarda su log ÍNTEGRO en
  `jobs/<id>/logs/<etapa>_AAAAMMDD_HHMMSS.log` (qué se hizo, qué se omitió,
  qué falló y por qué). El panel muestra la ruta en el resumen.

**Huecos visibles:**
- El resumen de la etapa 7 ahora reporta el estado real: "X/89 escenas
  con video. Faltan N: S03, S06, …" en vez de solo la cola del log.

## 20. Cambios v9.1 (2026-10-04)

**Bug crítico de miniaturas (NameError: prota_thumb):**
- Causa: en `thumbnails/generate_thumbnails.py`, `def prota_thumb` quedó
  definido DESPUÉS del bloque `if __name__ == "__main__": sys.exit(main())`.
  Como el panel corre el script como programa (no importado), el `sys.exit`
  se ejecutaba antes de que el `def` existiera → NameError en `render()`.
  En pruebas importadas sí pasaba, por eso no se detectó antes.
- Fix: el bloque del protagonista (PLAYERA_T + `prota_thumb`) ahora va
  ANTES del guard. Verificado corriendo el script como el panel lo hace
  (`python generate_thumbnails.py 999`): 3/3 miniaturas 1280×720 OK.
- Lección: todo script que el panel ejecute como subproceso debe probarse
  como `__main__`, no solo importado.

**Pie de versión dinámico:**
- El sidebar decía "Panel v7" fijo desde v7. Ahora usa
  `pipeline.PANEL_VERSION` (v9.1); subir la constante en cada release.

## 21. Cambios v10 (2026-10-04)

**Layout garantizado: la banda ya no tapa al protagonista.**
- Causa raíz de las capturas: el LLM ponía `banda_titulo()` en y=2.55 y al
  protagonista en el centro (cabeza en y≈3.0) → la banda tapaba la cara.
  El validador de "una sola banda" no cubría la posición.
- Nuevo chequeo por AST (`_checar_banda_vs_prota`): si hay
  `banda_titulo()/titulo_seguro()` y la cabeza del protagonista
  (pos.y + altura - 0.02, como en el rig) entra a la zona de la banda →
  se rechaza y autorrepara. Incluye un mini-evaluador de coordenadas
  Manim (ORIGIN/LEFT/RIGHT/UP/DOWN, tuplas, np.array, +,-,*); si `pos` no
  es evaluable, se deja pasar.
- Regla canónica en el prompt y en RIG_API: con banda arriba, el
  protagonista va ABAJO (`pos=DOWN*1.2+LEFT*3.5`, `altura=2.6`); sin banda
  puede ir al centro. Independiente del modelo: ya no importa si el
  modelo "sigue" la regla, el validador la impone.
- Extra: `Text()` crudo con `font_size>60` se rechaza (era el texto
  cortado en los bordes, p. ej. "OPTIMO: 2-6 m"). Usar las funciones del
  rig, que se auto-ajustan.
- Verificación: 11/11 casos unitarios + render E2E de escena conforme
  (banda arriba, protagonista abajo, sin encimado).

## 22. Cambios v11 (2026-10-04)

### 🚀 Publicar en YouTube (nuevo)

**Requisito clave:** la API key de YouTube solo sirve para *leer* datos
(búsquedas, sugerencias). *Subir* videos exige **OAuth 2.0** con la cuenta
del canal. No hay forma de publicar solo con la key.

**Instalación (una sola vez):**
1. `pip install -r requirements.txt` (agrega `google-api-python-client` y
   `google-auth-oauthlib`; sin ellas, la sección Publicar muestra qué
   falta en vez de tronar).
2. En [Google Cloud Console](https://console.cloud.google.com/) (puedes
   usar el mismo proyecto de tu API key):
   - **APIs y servicios → Biblioteca** → habilita **YouTube Data API v3**.
   - **APIs y servicios → Credenciales → Crear credenciales → ID de
     cliente de OAuth** → tipo **Aplicación de escritorio**.
   - Descarga el JSON, renómbralo a `client_secret.json` y colócalo en la
     carpeta `youtube/` junto a `app.py` (créala si no existe).
3. En el panel, dentro del proyecto: sección **🚀 Publicar en YouTube** →
   **Paso 1** → **🔗 Conectar mi canal de YouTube**. Se abre el navegador
   una vez para autorizar; se guarda `youtube/token.json` (se renueva solo).

**Uso (por video):**
- **Paso 2 · Contenido:** el panel pre-llena título, descripción y
  etiquetas desde tu `PAQUETE.md` (etapa 10); puedes editarlos ahí mismo.
  Eliges el video (por defecto `final_con_subtitulos.mp4`) y la privacidad:
  **privado** (solo tú), **oculto** (solo con enlace) o **público**.
  Recomendado: súbelo privado, revísalo en YouTube Studio y luego hazlo
  público.
- **Paso 3 · Subir:** botón **⬆️ Subir video a YouTube** con barra de
  progreso real (subida reanudable por chunks de 8 MB: si se corta el
  internet, reintenta sin empezar de cero). Al terminar muestra la URL
  (`https://youtu.be/…`) y la guarda en el proyecto.
- **Desconectar:** borra `token.json` desde el mismo panel.

**Cuota y límites:** cada subida cuesta ~1600 unidades del cupo diario
(10.000 por defecto) → ~6 videos/día. Para 2 videos/semana sobra.
**Secretos:** `youtube/client_secret.json` y `youtube/token.json` NUNCA
van al ZIP ni a git (la carpeta `youtube/` está excluida del paquete).

### 📊 Medidor de tokens (nuevo)

**Qué mide:** cada llamada a un modelo de IA (qué backend, qué modelo, en
qué proyecto y etapa, tokens de entrada/salida) se registra en
`usage.jsonl` (raíz del panel). Empieza a contar desde esta versión; lo
anterior no se puede reconstruir.

**Vista 📊 Medidor (sidebar):**
- Métricas: llamadas, tokens de entrada, de salida, total y **costo
  aproximado en USD**.
- Gráfica de dona: **reparto % por modelo** (qué modelo generó qué
  porcentaje).
- Barras: **tokens por proyecto**.
- Tabla de detalle por modelo (llamadas, entrada/salida, %, USD).
- **💲 Precios de referencia:** USD por millón de tokens (entrada, salida),
  **aproximados y editables** en el propio panel. Los tiers gratuitos,
  modelos `:free` y Ollama local cuestan 0.

**Cómo funciona por dentro:** `llm.py` captura el `usage` que reporta cada
API (`LAST_USAGE`; best-effort: si el backend no lo reporta, queda en
blanco) y `pipeline.execute_stage` lo registra con proyecto y etapa. El
medidor no interrumpe nada si falla.

*Versión del panel: v11 (Publicar en YouTube + Medidor de tokens).*

## 23. Cambios v12 (2026-10-04)

### 🖼️ Miniatura sí se sube (fix)

El bug reportado (video publicado sin miniatura): el uploader nunca llamaba
a la API de miniaturas. Ahora el **Paso 3** es "Miniatura y subida":
- Selector con las 3 miniaturas del proyecto (por defecto, la aprobada en
  la puerta) + vista previa.
- Tras subir el video se llama a `thumbnails().set` automáticamente.
- Si el canal no está verificado (youtube.com/verify), YouTube rechaza la
  miniatura pero el video queda publicado; el panel lo avisa sin tronar.
- El mapeo de privacidad UI→API (`privado→private`, `oculto→unlisted`,
  `público→public`) quedó integrado (antes la API recibía "privado" crudo).

### 📱 Cortos del video / estrategia Shorts (nuevo)

Nueva sección **📱 Cortos del video (Shorts)** en cada proyecto largo:
- **Sugerencia automática:** lee `SHORT SUGERIDO: Sxx` del PAQUETE.md y
  calcula los timestamps reales desde los audios TTS (botón "Usar
  sugerencia"). O manual: inicio/fin en mm:ss.
- **✂️ Generar corto vertical:** recorte 1080×1920 con subtítulos quemados
  (usa el SRT del video largo). YouTube clasifica como Short todo vertical
  de ≤3 min automáticamente.
- **Subida como Short:** cada corto generado tiene su título (pre-llenado
  con el del largo + #Shorts), descripción con palabras clave (reusa los
  tags del largo + enlace al video completo) y selector de privacidad
  (recomendado: público). Se registra el ID subido por corto.
- Estrategia: 1-2 Shorts por video largo traen visitas nuevas al largo.

### 🕒 Programar publicación (nuevo)

En el Paso 2, checkbox **"Programar publicación"** + fecha/hora: el video
se sube como privado y YouTube lo hace público solo a la hora elegida.
Útil para la cadencia de 2 videos/semana.

### 📝 Paquete de publicación v2 (research de 7 canales)

Se analizaron Ink Explainer, Aussie Finance, GoodEnoughAnimation, Rico
Animations, thedailyblurb, CasuallyFinance y un video animado de
referencia, comparados contra el video publicado del canal. Hallazgos
aplicados:
- **Orden canónico de la descripción:** gancho (2 líneas) → 🔍 LO QUE
  VERÁS: → ⏱ CAPÍTULOS: → 📚 FUENTES: → CTA suscripción → pregunta de
  engagement → hashtags (3-5) al final.
- **PROHIBIDO markdown** en la salida (`**`, `##`): YouTube lo muestra
  como texto crudo y se ve como error de automatización (esto rompía los
  headers del video publicado).
- **Los CAPÍTULOS ahora sí llegan a la descripción** (el parser viejo los
  descartaba) y los **HASHTAGS van al final del cuerpo** (antes solo
  caían al campo de tags, invisibles sobre el título).
- El parser limpia artefactos markdown y reconstruye paquetes viejos al
  formato canónico (probado con formato viejo y nuevo).
- Títulos: pregunta/afirmación fuerte/número/superlativo + keyword al
  frente, ≤60 caracteres. Tags: 12-15, minúsculas, específicos.

*Versión del panel: v12 (miniatura en subida + Shorts + programar + paquete v2).*

## 24. Cambios v13 (2026-10-05)

### ⛔ Storyboard truncado ahora FALLA la etapa (era solo un aviso)

Causa raíz del video de 3 min (proyecto 18): el guion tenía 6 bloques
(~9:30 planeados) pero el storyboard solo cubrió 10 escenas (40% del
guion). v12 lo detectaba pero solo lo escribía en el log y el pipeline
seguía → video corto silencioso. Ahora la etapa **falla ruidosamente**.

**↪️ Continuar storyboard (nuevo):** si la etapa falla por truncado, aparece
el botón «↪️ Continuar storyboard» en la etapa: pide al modelo SOLO las
escenas faltantes (desde S{N+1}, sin regenerar desde cero — ahorra tokens)
y las agrega a STORYBOARD.md. Revalida cobertura; si sigue baja, se puede
pulsar otra vez (iterativo).

**Nudge de longitud en Puerta 1:** si el guion tiene <900 palabras en un
proyecto largo, la puerta muestra advertencia (objetivo 8–12 min ≈
1200–1800 palabras) antes de aprobar.

### 🚫 Publicar exige PAQUETE.md (nuevo gate)

Si no existe `PAQUETE.md`, la sección Publicar muestra error bloqueante
("corre la etapa 10 primero") en vez de rellenar título="El Porqué" y
descripción vacía en silencio. Si el paquete parece incompleto, avisa
antes de subir.

### 📊 Medidor: estimación cuando el backend no reporta uso (fix)

La cadena de registro funcionaba, pero si el backend no devuelve `usage`
en su respuesta, todo quedaba en cero ("no funciona"). Ahora
`llm._set_usage` **estima por longitud** (≈4 chars/token) y marca el
registro como estimado. El Medidor muestra cuántas llamadas fueron
estimadas y hace cuánto fue el último registro (diagnóstico visible).

*Versión del panel: v13 (storyboard anti-truncado + gate de paquete + medidor con estimación).*

## 25. Cambios v14 (2026-10-06)

### 🖼️ Layout garantizado por construcción (fix de encimados y cortes)

Causa raíz de las capturas del proyecto 32: el LLM generaba
`callout(..., font_size=96)` (bandas gigantes) y luego `.move_to(RIGHT*4...)`
que las sacaba de la resolución. El validador v10 no lo atrapaba: solo
revisaba `Text()` crudo y la geometría de `banda_titulo`, no de `callout`.

**Rig (`scripts/zenn_rig.py`) — blindaje estructural:**
- Nuevo `_Seguro(VGroup)`: cualquier `.move_to()/.shift()` posterior queda
  recortado al encuadre automáticamente. Es imposible sacar un texto de la
  resolución por código (probado con render real).
- Nuevo `_encuadrar()`: mete el elemento al marco seguro (x ±6.9,
  y de -2.3 a 3.6, sin invadir subtítulos).
- `callout()` ahora es COMPACTO: `font_size` 96→60 por defecto,
  `ancho_max` 11.9→7.0, nuevo parámetro `pos=` y devuelve `_Seguro`.
- `etiqueta()`, `banda_titulo()`, `titulo_seguro()` también devuelven
  `_Seguro` (clamp automático).

**Validador (`pipeline.py`) — dos chequeos nuevos:**
- `font_size>72` rechazado en `callout/etiqueta/banda_titulo/titulo_seguro`
  (antes solo se revisaba `Text()` crudo).
- `_checar_solape_texto()`: sigue `.move_to()/.shift()` (encadenados o en
  sentencias separadas), calcula la caja final del callout/etiqueta y la
  del protagonista, y RECHAZA si se enciman — con instrucción concreta
  ("pon el callout al lado contrario con pos=") para la autorreparación.

**Prompt:** `callout()` documentado con `pos=` y regla "al lado contrario
del protagonista, nunca encima".

**Escenas viejas:** las ya renderizadas conservan el código viejo. Hay que
re-animarlas con el botón «🔁 Re-animar escena» (con LLM) y reensamblar.
Lista de escenas afectadas por proyecto (patrón `font_size>72` o
`.move_to()/.shift()` en textos): se entrega con el ZIP.

*Versión del panel: v14 (layout por construcción: _Seguro + validador de solape).*

## 26. Cambios v15 (2026-10-06) — pack visual + CTR (todo gratis)

Tras el research de canales del nicho (Memorias de Pez, Quantum Fracture,
CdeCiencia, Robot de Platón) y el análisis de @CausayMarca. Nicho
confirmado: curiosidad científica generalista en español ("Zenn en
español", hueco vacío).

**Rig (`scripts/zenn_rig.py`):**
- Nuevos props: `adn(pos, escala)`, `grafica_barras(pos, valores, ancho,
  etiquetas)`, `lupa(pos, escala)` — más vocabulario visual científico.
- `fondo_papel()`: fondo crema cálido opcional (self.add(fondo_papel()));
  look editorial tipo Memorias de Pez. Default sigue blanco.

**Miniaturas (CTR):**
- El LLM ahora propone también EXPRESION (sorpresa/feliz/preocupado según
  la emoción del tema) y PLAYERA por variante; el render las aplica por
  concepto. Fallback con keywords (miedo/peligro → preocupado, etc.).
- Texto gancho: el fallback elige hasta 4 palabras con más peso (cifras y
  sustantivos largos primero) en vez de las primeras 5.

**Pipeline:**
- Títulos del PAQUETE: sufijo " | En N minutos" (fórmula Memorias de Pez);
  N = duración real del video (final.mp4 o suma de audios TTS).
- TOPIC_PROMPT: la mezcla ahora incluye 1 EXPERIMENTO MENTAL
  "¿Qué pasaría si...?" por tanda (formato de 5,6M vistas del Robot de
  Platón): 3 ciencia + 2 cultura + 1 cotidiana + 1 experimento + 1 serie.
- FUENTES: el prompt del paquete ya las pedía del guion/investigación; se
  mantienen en el formato canónico 📚 FUENTES.

**Monetización:** el umbral YPP se duplica el 1-feb-2027 (8.000 h). Sprint:
2 videos/semana sin pausa. RPM realista del nicho en español: $1-3.

*Versión del panel: v15 (pack visual + CTR).*

## 27. Cambios v16 (2026-10-07) — fix content=null de proveedores

Reporte: etapa 5/10 Storyboard falló con `Error del modelo: 'NoneType'
object has no attribute 'strip'` tras 58s.

Causa raíz: algunos proveedores (modelos gratis saturados, filtro de
contenido o corte por max_tokens) devuelven `choices[0].message.content =
null`. En `_openai_chat()` y `_openrouter_generate()` el `.strip()` se
aplicaba directo sobre ese null → `AttributeError`, que NO es `LLMError`
y por tanto no lo capturaba `generate()`: la cadena no avanzaba al
siguiente modelo y la etapa moría con un mensaje críptico.

Fix: extracción null-safe en ambos backends; si el contenido viene
vacío/null se lanza `LLMError("contenido vacío (content=null)")` y la
cadena avanza al siguiente modelo como fue diseñada. Aplica a groq,
cerebras, mistral, tokenharbor, freellmapi, cloudflare, deepseek
(vía `_openai_chat`) y openrouter. Los demás backends ya eran seguros
(ollama, gemini, cohere auditados).

Verificado con mocks: null → LLMError, la cadena avanza al siguiente
modelo, y el caso normal sigue funcionando.

*Versión del panel: v16 (content=null ya no mata la etapa).*

## 28. Cambios v17 (2026-10-07) — fix videos cortos (4-5 min en vez de 8+)

Reporte: los videos salen de 4-5 minutos aunque el objetivo es 8+.

Causa raíz (doble fuga, medida en jobs/27 y jobs/32):
1. El guion nace corto: el prompt pide 1300-1900 palabras pero el modelo
   entrega 900-1160 y nada lo obliga a corregir (draft de un solo intento,
   crítico sin rechazo, Puerta 1 avisaba solo si <900). jobs/27: 900
   palabras; jobs/32: 1161.
2. El storyboard recorta 18-26%: el prompt dice "texto LITERAL" pero el
   modelo resume/parafrasea, y el chequeo v13 exigía solo 70% de cobertura
   (70% de 900 = 630 palabras ≈ 4 min). jobs/27: 665 palabras VOZ (74%)
   → ~4.6 min; jobs/32: 947 (82%) → ~6.5 min.

Fix estructural:
- `MIN_PALABRAS_GUION = 1300`: `run_guion_draft` expande automáticamente
  (hasta 2 intentos, con datos de la investigación, sin paja) si el
  borrador sale corto. El "🤖 Reescribir con crítica" también apunta a 1300.
- Puerta 1: si el guion tiene <1300 palabras, la aprobación se BLOQUEA
  (botón deshabilitado + error explicativo); entre 1300-1500 hay aviso.
- Storyboard: cobertura mínima 70% → 90%, y regla de oro "VOZ LITERAL,
  sin resumir" en el prompt (resumir = rechazo automático).

Verificado: expansión 900→1399 en 2 intentos; jobs/27 (74%) ahora falla
correctamente; 95% pasa.

*Versión del panel: v17 (guiones de 1300+ palabras, cobertura 90%).*

## 29. Cambios v18 (2026-10-07) — storyboard por partes + reintentos de conexión

Reporte: etapa 5 fallaba con ⛔ STORYBOARD TRUNCADO (961/1799 palabras,
53%) y "gemini-flash-latest: Remote end closed connection without
response" tras ~1 min.

Causa raíz doble:
1. Un storyboard completo de ~1800 palabras no cabe en la salida de los
   modelos gratis (Groq: 1000 tokens duros) y las conexiones largas se
   caen: el modelo se corta a la mitad (jobs/37: 53%). El botón
   «Continuar» era reactivo, no preventivo.
2. Los cortes de conexión no estaban clasificados para reintento:
   `_rate_kind` devolvía None y el fallo se registraba como duro sin
   reintentar.

Fix:
- `run_storyboard` ahora PARTE guiones de >1000 palabras en trozos de
  ~650 (sin cortar párrafos) y genera cada parte por separado, con
  numeración continua (S01...Snn) y `_renumerar_desde` por si el modelo
  reinicia en S01. La primera parte incluye la bienvenida y la última la
  despedida. El chequeo de 90% aplica al resultado unido.
- `_rate_kind`: "remote end closed", "connection reset/aborted",
  "timed out/timeout", "temporary failure" → "wait" (reintenta hasta 3
  veces con espera, como la cuota por minuto).
- Mensaje final "Ningún modelo respondió" ahora sugiere soluciones:
  modo auto, cambiar de backend, esperar 2-3 min.

Verificado: guion de 1799 palabras → 3 partes, 30 escenas S01-S30
continuas, 1620 palabras VOZ (90%); errores de conexión → wait.

*Versión del panel: v18 (storyboard por partes, reintentos de conexión).*

## 30. Cambios v19 (2026-10-08) — validación de cobertura POR PARTE

Reporte: la etapa 5 seguía fallando (⛔ TRUNCADO: 960/1274 palabras, 75%,
jobs/37) aun con el storyboard por partes de v18.

Causa raíz: no era (solo) corte de tokens — el modelo COMPRIME en vez de
copiar literal: 16-21 palabras por escena en lugar de 25-35, y salta
párrafos (la parte 1 cubrió su trozo al 64%). La validación era solo
global; cada parte se daba por buena sin revisarla.

Fix:
- Validación POR PARTE: tras generar cada trozo se mide su cobertura
  (VOZ vs palabras del trozo); si baja de 90%, se reintenta UNA vez con
  instrucción explícita ("tu versión anterior cubrió solo X de Y
  palabras: REPÍTELA copiando literal sin resumir"). Se queda la mejor
  versión de cada parte.
- El prompt de cada parte ahora incluye su conteo de palabras y el
  objetivo medible (≥90%), con orden de contarlo antes de responder.
- Regla de oro reformulada: "CORTAR, NO RESUMIR — tú decides DÓNDE CORTAR
  entre escenas; el texto se queda intacto".
- `_partir_guion` ahora también corta párrafos gigantes sin saltos de
  línea (por frases), para que el peor caso también se parta.

Verificado con mocks: guion sin párrafos → 3 partes; partes comprimidas →
reintento literal → 60 escenas S01-S60 continuas, cobertura 107%.

*Versión del panel: v19 (cobertura validada por parte, no solo global).*

## 31. Cambios v19.1 (2026-10-08) — bloqueo de red y rotación entre backends

Reporte: etapa 5 (storyboard) falló en 2s con
`Ningún modelo de 'groq' respondió / HTTP 403: Access denied. Please
check your network settings.`

Causa: **Groq estaba bloqueando la IP** (venía de una VPN): el 403 salía
en `/models` y en los 4 modelos, así que reintentar o rotar dentro de
Groq no servía de nada. Al quitar la VPN volvió a responder
(`/models` 200, 11 ids).

Fix en `llm.py`:

- `_rate_kind` añade `'blocked'`: "access denied" / "check your network"
  / "not available in your region" → no se reintenta y se corta esa
  cadena entera (antes caía como error duro y seguía perdiendo el tiempo
  con el mismo backend). Un 403 genérico de un modelo concreto pasa a
  `'skip'` (salta al siguiente modelo, no aborta el backend).
- **Rotación automática de backend**: si el backend elegido no respondió
  (bloqueo, cuota, 404…), `generate()` prueba los demás backends
  gratuitos con key (orden `BACKEND_ORDER`, 3 modelos por backend,
  excluidos `deepseek` —de pago— y `ollama` —necesita su modelo—) y
  devuelve `"<modelo> · <backend>"` cuando uno responde. El mensaje de
  error final ya no recomienda un "modo auto" que no existe: sugiere
  esperar, cambiar de backend en el panel y revisar la key.

Verificado: `rate_kind("HTTP 403: Access denied…") = blocked`;
`generate(backend="groq", model="openai/gpt-oss-120b")` → OK 0.7s;
con la key de OpenRouter corrupta → rotó solo a `gemini-2.5-flash · gemini`
(8.1s); sin alternativas → mensaje claro. Panel reiniciado (health ok).

*Versión del panel: v19.1 (rotación automática entre backends).*
