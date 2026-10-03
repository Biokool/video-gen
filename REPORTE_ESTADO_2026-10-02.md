# Reporte de estado — Panel Zenn Factory (video-gen)

**Fecha:** 2026-10-02 23:50 (Europe/Madrid)  
**Alcance:** validación de backends nuevos, Ollama, y ejecución del pipeline del proyecto 3  
**Repo:** https://github.com/Biokool/video-gen (`main`)

---

## 1. Resumen ejecutivo

| Bloque | Estado |
|---|---|
| Backends nuevos (Token Harbor, FreeLLMAPI, DeepSeek) | **OK y en GitHub** — el proyecto 4 (`qwen3.8-flash:free`) funciona con Token Harbor |
| Ollama local (7 modelos de chat) | **OK** — validados con `think:false`; helper `ARRANCAR_OLLAMA.bat` en GitHub |
| Panel (Streamlit, :8501) | **APAGADO ahora** (estaba OK hasta ~23:40; hay que relanzarlo con `INICIAR.bat`) |
| Servidor Ollama (:11434) | **APAGADO ahora** (relanzar con `ARRANCAR_OLLAMA.bat`) |
| Proyecto 3 «materia oscura» | **Etapa animación FALLIDA: 18/24 escenas** — faltan **S17, S19, S21, S22, S23, S24** |
| Etapas siguientes (ensamblado, miniatura, paquete) | pendientes (esperan a que animación termine) |
| Código nuevo sin subir | `pipeline.py` (firmas reales del rig + FIX_PROMPT con rig) + scripts de escenas de `jobs/3` — **commiteado y subido con este reporte** |

---

## 2. Proyecto 3 — estado real

```
tema=ok  investigacion=ok  guion=ok  verificacion=ok  storyboard=ok  tts=ok
animacion=FALLO (18/24)   ensamblado=pendiente  miniatura=pendiente  paquete=pendiente
```

- Backend del proyecto al cierre: **`tokenharbor` / modelo (auto)** (se fue cambiando durante los reintentos, ver §4).
- Escenas renderizadas: **18/24** en `jobs/3/video/scenes/` → S01–S16, S18, S20.
- Faltan: **S17, S19, S21, S22, S23, S24**.
- Los scripts .py de TODAS las escenas existen en `jobs/3/scripts/` (S20 y S24 son nuevos/no trackeados antes de este commit).
- Audio TTS completo (`jobs/3/audio/*.mp3`) → no hay que regenerar nada de voz.
- Al terminar animación, `run_all` sigue solo hasta `ensamblado` (ffmpeg) y `miniatura`; después se **detiene esperando tu aprobación de miniatura** para `paquete`.

### Cómo reanudar (una sola orden)

```powershell
F:\__AGENCIA_AIMA\__MUSE\video-gen\.venv\Scripts\python.exe C:\Users\mauri\AppData\Local\Temp\opencode\run_project.py 3
```
(o «Correr todo» en el panel). Las escenas ya renderizadas **se omiten**; solo reintenta las 6 que faltan.

---

## 3. Qué se estaba corriendo

Procesos en background (todos lanzados desenganchados con `Invoke-CimMethod Win32_Process.Create`, log en `%TEMP%\opencode\`):

| Log | Backend | Inicio | Resultado |
|---|---|---|---|
| `run_p3.log` | groq `qwen/qwen3.8-27b` | 21:12 | 21:38 — **12/24**, `RESULTADO: error animacion` |
| `run_p3b.log` | groq | 22:42 | (duplicado, matado a los pocos min) |
| `run_p3c.log` | groq | 22:48 | 23:08 — **16/24**, `RESULTADO: error animacion` |
| `run_p3d.log` | gemini `gemini-2.5-flash` | 23:12 | 23:16 — **18/24**, `RESULTADO: error animacion` |
| `run_p3e.log` | gemini (+ prompts mejorados) | 23:20 | 23:25 — **18/24**, `RESULTADO: error animacion` |
| `run_p3f.log` | tokenharbor (auto) | 23:26 | **sin RESULTADO** — proceso muerto (diagnóstico abortado); no validado |

Logs de etapa completos: `panel.db → stages.log` (proyecto 3, stage `animacion`); copia de trabajo en
`C:\Users\mauri\AppData\Local\Temp\opencode\log_animacion_p3.txt`.

---

## 4. Por qué falla: causas raíz (todas las rondas)

### 4.1 Ronda 1 (21:12, groq) → 12/24 — **Ollama apagado**
Los fallos no fueron de Groq:
```
S06/S13/S15…S24: FALLO tras intentos: Ollama no responde en http://localhost:11434
(<urlopen error [WinError 10061] conexión rechazada>). ¿Está corriendo `ollama serve`?
```
Causa: durante esa ventana yo maté Ollama para probar `ARRANCAR_OLLAMA.bat`, y **la generación estaba apuntando a Ollama** (el `gen` no usó el backend groq del proyecto). Coincide con que el usuario estaba probando modelos locales en el sidebar.  
**Arreglado para corridas externas:** `run_project.py` fija `backend = p["model_backend"]` al arrancar (hoy `tokenharbor`).  
**Arreglado para Ollama:** `ARRANCAR_OLLAMA.bat` la arranca en modo CPU y `INICIAR.bat` lo llama solo.

### 4.2 Ronda 2 (22:48, groq) → 16/24 — **Groq OTPM + código inventado**
- Groq OTPM = 1000 tok/min → `MAX_TOKENS["groq"] = 950` + espera y reintento (`llm.py`). Con 950 tokens el código de escena se **trunca** → validación «El código no usa el rig (falta `from zenn_rig import *` o la clase Sxx)» → agota 3 intentos (S16, S17, S21, S24).
- Errores de render por **kwargs inventados** (el prompt solo traía un resumen en prosa del rig):
  ```
  s19.py:16 in construct
      figs = stick_group(n=2, pos=[-2,0,0], direction=[2,0,0])
  TypeError: stick_group() got an unexpected keyword argument 'pos'
  ```
  (la firma real es `stick_group(n, center=ORIGIN, spacing=1.4, height=2.0, color=INK, seed=7)`)
- S15/S22/S23: errores de import/escritura parcial (había **dos** procesos `run_project` vivos a la vez).

### 4.3 Rondas 3 y 4 (23:12 y 23:20, gemini) → 18/24 — **cuota Gemini agotada**
```
S17/S19/S21/S22/S23/S24: FALLO tras intentos: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details...
```
Los primeros intentos con Gemini sí funcionaron (S15 y S16 pasaron de 16→18), pero la **cuota gratuita diaria/por minuto de Gemini se agotó** y las 6 escenas restantes murieron todas con 429 en los 3 intentos.  
Nota: `_is_rate_limit()` de `llm.py` no reconoce esta frase, así que no espera ni cambia de modelo: falla directo.

### 4.4 Ronda 5 (23:26, tokenharbor) → sin resultado
Se lanzó con `model_backend='tokenharbor'`, `model_id=''` (cadena automática de `:free`). El proceso **ya no está vivo** y no escribió `RESULTADO`; el diagnóstico de latencia se cortó (abortado). **Queda sin validar.**

### 4.5 Fenómeno observado y descartado: procesos de Python duplicados
Cada arranque muestra 2 procesos (`.venv\Scripts\python.exe` → hijo `…\uv\python\…` con los mismos argumentos). Ocurre igual con Streamlit (`streamlit.exe`), así que es un **trampolín del venv creado por uv**, no una corrida doble. El patrón de logs (una sola línea de cabecera, un solo `RESULTADO`) lo confirma.

---

## 5. Cambios de código hechos en esta sesión

### Ya en GitHub
| Commit | Contenido |
|---|---|
| `573bf9f` | Pipeline completo: animación Manim, ensamblado, INICIAR.bat, rig, fonts, PROMPT_MAESTRO |
| `8aa2cf2` | Backends Token Harbor / FreeLLMAPI / DeepSeek + motor TTS multi-voz |
| `209db10` | Ollama `think:false` + cortes de cuota Groq (MAX_TOKENS 950, backoff) |
| `0bcc3e1` | `ARRANCAR_OLLAMA.bat` (modo CPU, driver 546.29 no compila PTX) + tabla de modelos locales en DOCUMENTACION.md |
| `16ecb0b` | `ARRANCAR_OLLAMA.bat`: `exit /b` en vez de `goto` (cmd perdía el label al llamarlo desde INICIAR.bat) |

### Incluidos en el commit de este reporte
- **`pipeline.py`**:
  - `_rig_api_text()` — extrae con `ast` las **firmas reales** de `zenn_rig.py` y las antepone al prompt (evita kwargs inventados como `pos=`/`direction=`).
  - `FIX_PROMPT` ahora recibe `{rig}` (antes el modelo «arreglaba» a ciegas, sin ver la API real) + instrucción explícita de no inventar parámetros.
  - `run_animacion` usa `rig_text` en la generación y en la reparación.
- **`jobs/3/scripts/s*.py`**: regenerados por las rondas con Gemini (S15, S16 … y nuevos `s20.py`, `s24.py`).

---

## 6. Backends disponibles (claves en `panel.db`)

| Backend | Clave | Uso ahora mismo |
|---|---|---|
| gemini | ✅ | **cuota 429 agotada** — no usar hasta que se recupere |
| groq | ✅ | usable, pero OTPM 1000 → código truncado si se pide mucho; mejor `openai/gpt-oss-120b` |
| tokenharbor | ✅ | **pendiente de validar** (corrida 5 sin resultado) |
| openrouter | ✅ | buena alternativa (modelos `:free` de la PREFERRED) |
| mistral | ✅ | alternativa |
| freellmapi | ✅ | router local `localhost:3001/v1` (si está levantado) |
| deepseek | ✅ | de pago (saldo) |
| cerebras / cohere | ❌ | sin clave |
| ollama | — | local, CPU ~5–6 tok/s; hay que relanzar `ARRANCAR_OLLAMA.bat` |

**Recomendación para terminar las 6 escenas:** `tokenharbor` (auto) → si responde mal, `openrouter` → en último caso `groq` con `openai/gpt-oss-120b`, o local `gemma4:e4b`.

---

## 7. Pendientes / siguiente paso inmediato

1. Relanzar el panel (`INICIAR.bat`) y Ollama (`ARRANCAR_OLLAMA.bat`) — ambos están apagados.
2. Reanudar el proyecto 3 hasta completar **S17, S19, S21, S22, S23, S24** (backend sugerido: tokenharbor o openrouter).
3. Dejar que sigan `ensamblado` y `miniatura`; **aprobar la miniatura** en el panel para desbloquear `paquete`.
4. Mejora sugerida en `llm.py`: que `_is_rate_limit()` reconozca `code 429 / exceeded your current quota` y salte de backend en vez de fallar los 3 intentos.

---

*Generado automáticamente durante la sesión de operación del panel.*
