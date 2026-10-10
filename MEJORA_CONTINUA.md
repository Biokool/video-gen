# Mejora continua — Indaga

Plan para que cada video salga mejor que el anterior, de forma
sistemática y no por accidente. Dos carriles: **automático** (el panel
lo revisa solo) y **manual** (el loop publicar → medir → ajustar).

## 1. Chequeos automáticos (el panel ya los hace)

Cada vez que generas o verificas un storyboard, el panel revisa:

| Chequeo | Dónde | Qué evita |
|---|---|---|
| Cobertura ≥90% por parte | Etapa 5 | Videos cortados (proyecto 18: 3 min) |
| Continuación automática | Etapa 5 | Partes al 80% que se quedan cortas |
| Formato VOZ/VISUAL tolerante | Etapa 5, 6, 7, 8 | Escenas invisibles (S48-S54) |
| **Anti-repetición**: temas ya cubiertos prohibidos en continuaciones | Etapa 5 | Contar 4 veces lo mismo (proyecto 37: Wagner) |
| **Detector de repetición**: title_cards duplicados, nombres en bloques separados | 🔍 Verificar | Enterarse después de publicado |
| **Doble final**: despedida + escenas después | 🔍 Verificar | El video "termina dos veces" |
| **Citas sueltas**: VOZ que es solo `(Autor, año)` | 🔍 Verificar | Narración rota en TTS |
| VOZ muy corta (<5 palabras) | 🔍 Verificar | Escenas truncadas (S54) |
| Elementos completos (vo.json/audios/videos) | Correr todo | "Falta el audio de S48" |
| Ensamblado filtra por storyboard | Etapa 8 | Videos de escenas borradas colados |

Si un chequeo nuevo se necesita, se agrega aquí y en `pipeline.py`.

## 2. Loop manual: publicar → medir → ajustar

Después de publicar cada video (48h después, con datos):

1. **Medir**: CTR (miniatura+título), retención a 30s, retención media,
   comentarios (qué citan).
2. **Diagnosticar** con la scorecard de abajo.
3. **Ajustar**: UN cambio por video en `PROMPT_MAESTRO.md` o en el panel.
   Nunca dos cambios a la vez (si no, no sabes qué funcionó).

### Scorecard por video

- Hook: ¿el giro/promesa sale antes de los 15s? (sí/no)
- Ritmo: ¿algún tramo >60s sin pico informativo ni giro visual?
- Repetición: ¿algún tema se cuenta 2+ veces? (verificación automática)
- Final: ¿la despedida es lo último? (verificación automática)
- Visual: ¿cambio visual cada 5-8s?
- Comentarios: ¿qué frase/escena citan? (esa es tu fórmula: repítela)

## 3. Benchmark competitivo (revisar 1 vez al mes)

Canales de referencia del nicho y qué robarles:

- **Memorias de Pez** (2.7M): dibujo simple + humor constante + lenguaje
  de todos los días. Robar: un chiste o giro cada ~60s.
- **Quantum Fracture** (3.9M): estructura pregunta → experimento mental →
  respuesta. Robar: el "¿qué pasaría si...?" por video (ya en el generador
  de temas).
- **CdeCiencia** (4.95M): ritmo rapidísimo, cero relleno. Robar: si una
  escena no agrega dato nuevo o giro, se borra.
- **La Hiperactina** (2.6M): analogías con la vida cotidiana. Robar: una
  analogía doméstica por bloque (ya en PROMPT_MAESTRO).

Regla de oro competitiva: **un tema = un bloque**. Si el guion menciona
a Wagner 5 veces está bien; si el storyboard le dedica 4 bloques
separados, es repetición. El panel lo detecta; el humano lo decide.

## 4. Registro de cambios

Cada ajuste al playbook se anota en DOCUMENTACION.md con fecha, causa
(video que lo motivó) y verificación. Nada se cambia "porque sí".
