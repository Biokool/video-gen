from manim import *
from zenn_rig import *

class S08(Scene):
    def construct(self):
        self.add(fondo_papel())

        banda = banda_titulo("DISEÑO PRÁCTICO EN COMBATE", color=TEAL)
        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.5,
            playera="verde",
            altura=2.2,
            expresion="decidido",
            pose="brazos_cruzados"
        )

        casco_real = casco_vikingo(pos=RIGHT * 0.5 + UP * 0.2, escala=1.0)
        lbl_real = etiqueta("Casco funcional", pos=RIGHT * 0.5 + DOWN * 1.4)

        casco_mito = casco_vikingo(pos=RIGHT * 3.6 + DOWN * 0.6, escala=0.9).rotate(PI * 0.45)
        lbl_mito = etiqueta("Cuernos: estorbo", pos=RIGHT * 3.6 + UP * 0.6)

        self.play(FadeIn(banda), FadeIn(prota), run_time=1.5)
        self.wait(1.5)

        self.play(FadeIn(casco_real, shift=UP * 0.3), Write(lbl_real), run_time=1.5)
        self.wait(2.0)

        self.play(FadeIn(casco_mito, shift=DOWN * 0.4), Write(lbl_mito), run_time=1.5)
        self.wait(1.5)

        cambiar_cara(prota, "sarcastico")
        self.wait(2.0)

        acento = red_accent(casco_real)
        self.play(Create(acento), run_time=1.2)
        self.wait(2.0)

        cambiar_cara(prota, "decidido")
        self.wait(2.8)