from manim import *
from zenn_rig import *

class S38(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        banda = banda_titulo("VIKINGO = BRUTALIDAD", color=RED)
        self.play(FadeIn(banda), run_time=1)
        self.wait(1)

        prota = version_prota(4, pos=DOWN*1.5 + LEFT*3.5)
        casco = casco_vikingo(pos=ORIGIN, escala=1.0)
        self.play(FadeIn(prota), run_time=1)
        self.wait(0.5)

        # Cambiar cara usando Transform para animar de forma segura
        prota_decidido = version_prota(4, pos=DOWN*1.5 + LEFT*3.5)
        cambiar_cara(prota_decidido, 'decidido')
        self.play(Transform(prota, prota_decidido), run_time=0.5)
        
        self.play(FadeIn(casco, shift=RIGHT*0.5), run_time=1)
        self.wait(0.5)

        texto_vikingo = Text("VIKINGO", font_size=48, color=RED).move_to(RIGHT*2.5 + UP*1.5)
        self.play(Write(texto_vikingo), run_time=1)
        self.wait(1)
        
        texto_brutalidad = Text("BRUTALIDAD", font_size=48, color=RED).move_to(RIGHT*2.5 + UP*1.5)
        self.play(Transform(texto_vikingo, texto_brutalidad), run_time=1)
        self.wait(1)
        
        self.play(
            FadeOut(banda),
            FadeOut(prota),
            FadeOut(casco),
            FadeOut(texto_vikingo),
            run_time=1
        )
        self.wait(0.5)