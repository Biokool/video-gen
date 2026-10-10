"""Marca del canal — UN SOLO LUGAR para nombre, voz y colores.

v25 (2026-10-09): renombre del canal El Porqué -> Indaga.
Si el nombre vuelve a cambiar, se cambia AQUÍ y en PROMPT_MAESTRO.md
(saludo/despedida del guion); el resto del panel lee estas constantes.

El emblema del canal vive en marca/indaga-emblema.png (relativo a panel/).
"""

NOMBRE_CANAL = "Indaga"
ESLOGAN = "Donde las respuestas sorprenden"

# Voz fija del canal (la usa PROMPT_MAESTRO.md en apertura/cierre del guion)
SALUDO = ("¡Hola! Bienvenidos a Indaga, donde cada pregunta "
          "se investiga a fondo.")
DESPEDIDA = ("Esto fue Indaga. Nos vemos en el próximo video... "
             "para la siguiente indagación.")

# CTA por defecto para descripciones de YouTube (etapa 10 / subida)
CTA_YOUTUBE = ("🔔 Suscríbete a Indaga para la siguiente indagación, "
               "cada semana.")

HASHTAGS = ["#ciencia", "#curiosidades", "#sabiasque"]

# Paleta oficial (emblema + banner)
COLORES = {
    "noche": "#011348",   # azul noche: fondos, misterio
    "ambar": "#FFB300",   # dorado: lupa, luz del descubrimiento
    "blanco": "#FFFFFF",
}

RUTA_EMBLEMA = "marca/indaga-emblema.png"  # relativo al directorio panel/
