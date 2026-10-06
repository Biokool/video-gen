from manim import *
from zenn_rig import *

class S02(Scene):
    def construct(self):
        self.add(fondo(INK))
        banda_titulo("Resaca mental", color=YELLOW)

        prota = version_prota(1, pos=DOWN * 1.5 + LEFT * 3)
        self.play(FadeIn(prota, shift=RIGHT))
        phone = caja("Móvil", pos=UP * 0.5 + RIGHT * 2, width=0.8)
        self.play(FadeIn(phone, scale=0.8))

        self.wait(0.5)
        arr = arrow(prota.get_center(), phone.get_center(), color=INK, width=8)
        self.play(Create(arr))
        self.wait(0.3)

        cambiar_cara(prota, "pensando")
        self.wait(2)

        self.play(FadeOut(arr), FadeOut(phone), FadeOut(prota))