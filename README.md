# Panel Zenn Factory

Tablero visual local para operar el canal **El Porqué**: bandeja de temas,
pipeline por proyecto con 3 puertas de aprobación, configuración por video
(largo / corto-recorte / corto-standalone) y combo multi-backend
(Gemini, Groq, Cerebras, OpenRouter gratis, Mistral, Cohere ↔ Ollama local).

## Requisitos

- Python 3.10+
- Manim (viene en `requirements.txt`): renderiza la animación. Es la
  dependencia pesada del paquete (~200 MB con sus librerías).
- Ollama corriendo en `localhost:11434` si quieres usar modelos locales
- FFmpeg + ffprobe en el PATH (TTS, ensamblado y recortes)
- Claves (opcionales según uso): `GEMINI_API_KEY`, `GROQ_API_KEY`,
  `CEREBRAS_API_KEY`, `OPENROUTER_API_KEY`, `MISTRAL_API_KEY`,
  `COHERE_API_KEY`, `YOUTUBE_API_KEY` — se guardan en el SQLite local
  del panel, no salen de tu máquina. Basta con configurar un backend
  en la nube u Ollama local.

## Instalación y arranque

**Windows (repo video-gen):** doble clic en `INICIAR.bat` — crea el entorno,
instala dependencias, siembra la base y abre el panel.

**Manual (cualquier sistema):**

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 seed.py        # una sola vez: carga el piloto ya producido
streamlit run app.py  # abre http://localhost:8501
```

## El flujo (así de simple)

1. **📥 Bandeja**: añade un tema (manual o generado) y pulsa **Aprobar**.
   Se crea el proyecto (puerta: tema).
2. **🎬 Proyectos** → abre el proyecto → pulsa **▶ Correr todo**.
   El pipeline avanza solo, etapa por etapa, en orden:
   investigación → guion → verificación → storyboard → TTS →
   miniaturas → paquete.
3. Se **detiene solo** cuando te necesita:
   - **Puerta 1 · Guion**: el borrador queda generado; léelo y pulsa
     «Aprobar guion». Después vuelve a «Correr todo».
   - **Etapas manuales** (animación Manim, ensamblado): hazlas y pulsa
     «✔ Marcar hecho» en su etapa.
   - **Puerta 2 · Miniatura**: elige una de las 3 miniaturas ilustradas
     antes de cerrar el paquete.
4. Arriba del tablero siempre verás **«Siguiente paso»**: qué toca ahora
   y por qué. Las etapas van numeradas (1/10, 2/10…) en su orden real.

## Qué hace cada vista

- **📥 Bandeja de temas**: añade temas manuales o genera 8 propuestas con el
  modelo elegido en el combo. Aprobar crea el proyecto (puerta 1: tema).
- **🎬 Proyectos**: lista con tipo y progreso. El detalle muestra el tablero
  de etapas numerado (▶ ejecutar una, ✔ marcar hecho lo manual),
  el botón «Correr todo», la puerta del guion (leer, aprobar, pedir cambios
  o reescribir con crítica) y la puerta de miniatura (elegir entre las
  generadas).
- **⚙️ Configuración**: voz/idioma por defecto y claves de los 7 backends.

## Tipos de proyecto

| Tipo | Pipeline |
|---|---|
| `largo` | 10 etapas, 16:9, 8–12 min |
| `corto-recorte` | recorte vertical 1080×1920 de un largo (segmento a elegir, subtítulos quemados) |
| `corto-standalone` | guion propio de 30–60 s, mismo pipeline en vertical |

## Combo de modelos (sidebar)

Siete backends con capa gratuita (verificada 2026-09/10), en orden de
preferencia: calidad de español + cuota + velocidad. El set gratis rota en
todos los proveedores: el panel descubre modelos vía API cuando hay key y,
si uno falla (404/429/límite), intenta el siguiente de la cadena.

| Backend | Gratis | Modelos preferidos |
|---|---|---|
| Gemini (Google AI Studio) | ~1.500 req/día en Flash, sin tarjeta | `gemini-2.5-flash` (+ descubrimiento) |
| Groq | 1.000 req/día, 200K tok/día por modelo | `qwen/qwen3.6-27b`, `openai/gpt-oss-120b` |
| Cerebras | ~1M tok/día, el más rápido | `zai-glm-4.7`, `gpt-oss-120b` (lineup rotativo) |
| OpenRouter :free | 50 req/día (1.000 con $10 de crédito) | nemotron-3-super → gemma-4-31b → llama-3.3-70b → `openrouter/free` |
| Mistral (La Plateforme) | plan Experiment (~1B tok/mes) | `mistral-small/medium/large-latest` |
| Cohere (trial) | 1.000 llamadas/mes | `command-a-03-2025`, `command-r-plus` |
| Cloudflare Workers AI | plan Free: 10.000 neuronas/día (21 modelos OK) | `@cf/meta/llama-3.3-70b-instruct-fp8-fast`, `@cf/qwen/qwen3.8-27b` |
| NVIDIA API catalog | 10 de 80 ids responden en la cuenta | `nvidia/nemotron-3-super-120b-a12b`, `z-ai/glm-5.3` |
| Ollama local | ilimitado (tu hardware) | lista dinámica de `ollama list` |

- **ollama**: el combo muestra lo que tengas instalado; nada está hardcodeado.
- Las claves se guardan en el SQLite local del panel (Configuración),
  no salen de tu máquina. Ojo: el gratis de Mistral exige aceptar que
  entrenen con tus datos; el de Gemini pierde el gratis si activas
  facturación en el proyecto.
- Consumo real del pipeline: ~5–10 llamadas por video (borrador, crítico,
  temas amortizados). Cualquiera de estos tiers sobra para 2 videos/semana.

## Convenciones de `jobs/<id>/`

- `INVESTIGACION.md` — informe con fuentes (etapa 2).
- `GUION.md` — borrador y guion aprobado (la Puerta 1 lo lee de aquí).
- `STORYBOARD.md` — escenas numeradas con descripción visual.
- `PAQUETE.md` — título, descripción, capítulos y tags de publicación.
- `vo.json` — `[{"id":"s01","text":"..."}]` para el TTS automático.
- `audio/`, `video/` — artefactos que el panel referencia.
- `scripts/*.py` — escenas Manim (la animación se marca manual: el código
  de escenas lo genera el agente o tú, el panel lo registra).

## Notas honestas

- Automático real hoy: investigación, borrador de guion, verificación de
  referencias (DOI/PMID), storyboard, TTS (crea `vo.json` solo desde el
  storyboard), **animación** (el LLM genera el código Manim escena por
  escena y lo renderiza, con autorreparación si una escena falla),
  **ensamblado** (el audio manda; genera `final.mp4`, `final.srt` y
  `final_con_subtitulos.mp4`), miniaturas ilustradas, recorte vertical
  y paquete de publicación.
- La animación de un video largo tarda: renderizar 15–40 escenas puede
  tomar varios minutos según tu CPU. Las escenas ya renderizadas se
  omiten al reintentar.
- La calidad del guion y de las escenas no la garantiza ningún modelo:
  sale del proceso borrador → crítico → tu aprobación (Puerta 1) y de
  revisar el storyboard antes de animar.
