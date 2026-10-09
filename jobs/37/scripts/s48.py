from manim import *
from zenn_rig import *

class S48(Scene):
    def construct(self):
        self.add(fondo(INK))
        title = title_card("EL DÍA QUE NACIÓ EL MITO MODERNO", YELLOW)
        self.add(title)
        
        prota = protagonista(pos=DOWN*2, playera=PLAYERA_NARANJA, altura=2.2, expresion="mente_explotada", pose="de_pie")
        prota.shift(LEFT*3.5)
        sol_obj = sol(pos=RIGHT*4+UP*2, color=YELLOW)
        tierra = planeta(pos=RIGHT*4, radio=0.95, color=TEAL)
        reloj = reloj_pared(pos=LEFT*3+UP*2, hora_3=True)

        self.add(prota, reloj, tierra, sol_obj)
        self.wait(0.5)
        self.play(prota.animate.shift(RIGHT*2), run_time=0.8)
        cambiar_cara(prota, "decidido")
        self.wait(1.2)
        self.play(FadeOut(title))
        self.wait(0.5)