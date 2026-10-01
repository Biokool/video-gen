# Panel Zenn Factory

Tablero visual local para operar el canal **El Porqué**: bandeja de temas,
pipeline por proyecto con 3 puertas de aprobación, configuración por video
(largo / corto-recorte / corto-standalone) y combo multi-backend
(Gemini, Groq, Cerebras, OpenRouter gratis, Mistral, Cohere ↔ Ollama local).

## Requisitos

- Python 3.10+
- Ollama corriendo en `localhost:11434` si quieres usar modelos locales
- FFmpeg (para recortes de shorts)
- Claves (opcionales según uso): `GEMINI_API_KEY`, `GROQ_API_KEY`,
  `CEREBRAS_API_KEY`, `OPENROUTER_API_KEY`, `MISTRAL_API_KEY`,
  `COHERE_API_KEY`, `YOUTUBE_API_KEY` — se guardan en el SQLite local
  del panel, no salen de tu máquina. Basta con configurar un backend
  en la nube u Ollama local.

## Instalación y arranque

```bash
cd ~/workspace/zenn-factory/panel
pip install -r requirements.txt
python3 seed.py        # una sola vez: carga el piloto ya producido
streamlit run app.py  # abre http://localhost:8501
```

## Qué hace cada vista

- **📥 Bandeja de temas**: añade temas manuales o genera 8 propuestas con el
  modelo elegido en el combo. Aprobar crea el proyecto (puerta 1: tema).
- **🎬 Proyectos**: lista con tipo y progreso. El detalle muestra el tablero
  de etapas (▶ ejecutar lo automático, ✔ marcar hecho lo manual),
  la puerta 2 (guion: leer, aprobar, pedir cambios o reescribir con crítica)
  y la puerta 3 (elegir miniatura entre las generadas).
- **⚙️ Configuración**: voz/idioma por defecto y claves.

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
| Ollama local | ilimitado (tu hardware) | lista dinámica de `ollama list` |

- **ollama**: el combo muestra lo que tengas instalado; nada está hardcodeado.
- Las claves se guardan en el SQLite local del panel (Configuración),
  no salen de tu máquina. Ojo: el gratis de Mistral exige aceptar que
  entrenen con tus datos; el de Gemini pierde el gratis si activas
  facturación en el proyecto.
- Consumo real del pipeline: ~5–10 llamadas por video (borrador, crítico,
  temas amortizados). Cualquiera de estos tiers sobra para 2 videos/semana.

## Convenciones de `jobs/<slug>/`

- `GUION.md` — guion aprobado (la puerta 2 lo lee de aquí).
- `vo.json` — `[{"id":"s01","text":"..."}]` para el TTS automático.
- `audio/`, `video/` — artefactos que el panel referencia.
- `scripts/*.py` — escenas Manim (la animación se marca manual: el código
  de escenas lo genera el agente o tú, el panel lo registra).

## Notas honestas

- Las etapas marcadas `manual`/`asistida` no se ejecutan solas: el panel las
  rastrea y te deja marcarlas. Lo automático real hoy: TTS, verificación de
  referencias (DOI/PMID), miniaturas y recorte vertical.
- La calidad del guion no la garantiza ningún modelo: sale del proceso
  borrador → crítico → tu aprobación (puerta 2).
