from manim import *
from zenn_rig import *

class S55(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        # Se respeta la regla de una sola llamada a banda_titulo / callout / título en la misma animación o escena según la advertencia.
        # Quitamos la banda_titulo para dejar solo el callout y el contenido visual limpio.
        prota = version_prota(2, pos=DOWN*1.2+LEFT*3.5)
        self.play(
            FadeIn(prota),
            run_time=1.0
        )
        
        c = callout("¡Es fascinante!", color=ORANGE, pos=RIGHT*3.5+UP*1.0)
        p = planeta(pos=RIGHT*3.5+DOWN*1.0, radio=1.2, color=TEAL)
        
        self.play(
            FadeIn(c),
            Create(p),
            run_time=1.5
        )
        
        self.wait(1.5)