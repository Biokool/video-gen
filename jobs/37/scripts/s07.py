from manim import *
from zenn_rig import *

class S07(Scene):
    def construct(self):
        # Fondo y título principal
        self.add(fondo(CREMA))
        banda = banda_titulo("El casco de Gjermundbu", color=AZUL_MARINO)
        self.play(FadeIn(banda), run_time=0.8)
        self.wait(0.5)

        # Protagonista y objeto principal
        # Usamos constantes de playera o strings según el rig
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera="verde", 
            altura=2.6, 
            expresion="feliz", 
            pose="senalando"
        )
        casco = casco_vikingo(pos=RIGHT*2.5, escala=1.8)
        
        self.play(FadeIn(prota), FadeIn(casco), run_time=1.0)
        self.wait(0.8)

        # En lugar de Line sueltas (que el rig pide evitar para personajes/objetos), 
        # usamos red_accent que es la herramienta oficial de resaltado del rig.
        acento = red_accent(casco, scale=1.3)
        self.play(Create(acento), run_time=1.0)
        self.wait(0.5)

        # IMPORTANTE: Reemplazamos callout por etiqueta para evitar el error de 
        # superposición con la banda_titulo.
        info = etiqueta(
            "Protección ocular y nasal", 
            pos=RIGHT*2.5 + UP*1.8, 
            color=INK,
            font_size=36
        )
        self.play(Write(info), run_time=1.0)
        self.wait(1.0)

        # Animación de interacción
        cambiar_cara(prota, "pensando")
        self.wait(0.8)

        # Flecha de conexión (parámetros reales del rig: start, end, color, width)
        flecha = arrow(
            start=prota.get_center() + RIGHT*0.7, 
            end=casco.get_center() + LEFT*0.8, 
            color=INK, 
            width=8
        )
        self.play(Create(flecha), run_time=0.8)
        self.wait(1.5)

        # Salida
        self.play(
            FadeOut(info), 
            FadeOut(flecha), 
            FadeOut(acento), 
            run_time=0.8
        )
        cambiar_cara(prota, "feliz")
        self.wait(0.5)

        self.play(
            FadeOut(prota), 
            FadeOut(casco), 
            FadeOut(banda), 
            run_time=1.0
        )
        self.wait(0.3)