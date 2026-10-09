from manim import *
from zenn_rig import *

class S47(Scene):
    def construct(self):
        # Fondo y título
        self.add(fondo(CREMA))
        banda = banda_titulo("SUSCRÍBETE", color=TEAL)
        self.play(FadeIn(banda, shift=DOWN*0.3), run_time=0.8)

        # Protagonista: siguiendo reglas de layout (y <= -1.2, altura <= 2.6)
        prota = protagonista(
            pos=DOWN*1.4 + LEFT*3.5, 
            playera="teal", 
            altura=2.5, 
            expresion="feliz", 
            pose="senalando"
        )
        self.play(FadeIn(prota, shift=UP*0.4), run_time=0.8)

        # Etiquetas: Corrigiendo el error de la tupla en 'pos'
        # pos debe ser un array/vector (suma), no una tupla (coma)
        like = etiqueta("👍 LIKE", RIGHT*3.0 + UP*0.5, color=RED, font_size=44)
        sub  = etiqueta("🔔 SUSCRÍBETE", RIGHT*3.0 + DOWN*0.5, color=ORANGE, font_size=44)
        
        self.play(FadeIn(like, shift=LEFT*0.2), run_time=0.5)
        self.play(FadeIn(sub, shift=LEFT*0.2), run_time=0.5)

        # Elementos extra: Peces
        pez1 = pez(pos=UP*1.5 + RIGHT*1.5, color=CORAL, escala=0.9)
        pez2 = pez(pos=UP*1.0 + RIGHT*3.5, color=TEAL, escala=0.7)
        self.play(
            FadeIn(pez1, shift=LEFT*0.5), 
            FadeIn(pez2, shift=LEFT*0.5), 
            run_time=0.7
        )

        # Animación de los peces
        self.play(
            pez1.animate.shift(RIGHT*1.2).scale(0.95),
            pez2.animate.shift(RIGHT*0.8).scale(1.05),
            run_time=1.6
        )
        self.play(
            pez1.animate.shift(LEFT*1.2).scale(0.95),
            pez2.animate.shift(LEFT*0.8).scale(1.05),
            run_time=1.6
        )

        # Cambio de expresión
        cambiar_cara(prota, "euforico")
        self.wait(0.8)

        # Salida
        self.play(
            FadeOut(pez1), 
            FadeOut(pez2),
            FadeOut(prota), 
            FadeOut(like), 
            FadeOut(sub),
            FadeOut(banda),
            run_time=0.8
        )
        self.wait(0.4)