from manim import *
from zenn_rig import *

class S33(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        banda = banda_titulo("EL DÍA QUE NACIÓ EL MITO MODERNO", color=ORANGE)
        prota = protagonista(pos=DOWN*1.2 + LEFT*3.0, playera="amarilla", altura=2.6, expresion="pensando", pose="de_pie")
        self.play(FadeIn(banda, shift=DOWN*0.5), run_time=0.8)
        self.play(FadeIn(prota, shift=UP*0.5), run_time=0.8)
        self.wait(1.5)
        # cambiar_cara() devuelve un VGroup (no una Animation): se transforma
        # creando una nueva versión del protagonista con la expresión deseada.
        prota_sorpresa = protagonista(pos=DOWN*1.2 + LEFT*3.0, playera="amarilla", altura=2.6, expresion="sorpresa", pose="de_pie")
        self.play(Transform(prota, prota_sorpresa), run_time=0.6)
        self.play(prota.animate.move_to(DOWN*1.2 + LEFT*2.5), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(banda), FadeOut(prota), run_time=0.8)