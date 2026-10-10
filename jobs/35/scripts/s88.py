from manim import *
from zenn_rig import *

class S88(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5,
            playera=PLAYERA_AZUL,
            altura=2.6,
            expresion="sorpresa",
            pose="senalando"
        )
        
        self.play(FadeIn(prota), run_time=1.0)
        
        c = callout(
            "¡El factor sorpresa: el azar!",
            color=ORANGE,
            pos=RIGHT*3.4 + UP*1.0
        )
        
        d = dado = Cube().scale(0.6).set_color(TEAL).shift(RIGHT*3.4 + DOWN*0.8)
        
        self.play(FadeIn(c), Create(d), run_time=1.5)
        
        self.play(
            d.animate.rotate(PI/2, axis=UP+RIGHT),
            run_time=2.0
        )
        
        cambiar_cara(prota, "mente_explotada")
        
        self.wait(3.5)
        
        self.play(
            FadeOut(prota),
            FadeOut(c),
            FadeOut(d),
            run_time=1.0
        )