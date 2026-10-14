from manim import *
from zenn_rig import *

class S24(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título superior seguro con banda (usamos FadeIn ya que banda_titulo es un Mobject)
        bt = banda_titulo("DESARROLLO FETAL Y HORMONAS", color=AZUL_MARINO)
        self.play(
            FadeIn(bt),
            run_time=0.5
        )
        
        # Protagonista ABAJO (y <= -1.2, altura <= 2.6) para no chocar con la banda superior
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.5,
            playera=PLAYERA_AZUL,
            altura=2.4,
            expresion="pensando",
            pose="de_pie"
        )
        self.play(FadeIn(prota), run_time=0.8)
        
        # Props temáticos en el lado derecho
        cerebro_prop = adn(pos=RIGHT * 3.2 + UP * 0.5, escala=1.2, color=AZUL_MARINO)
        matraz_prop = matraz(pos=RIGHT * 3.2 + DOWN * 1.5, escala=1.1, liquido=CORAL)
        
        self.play(
            Create(cerebro_prop),
            FadeIn(matraz_prop),
            run_time=1.2
        )
        
        # Usamos etiqueta() en lugar de callout para evitar llamadas repetidas conflictivas de textos destacados
        c = etiqueta("Exposicion a testosterona", pos=RIGHT * 3.2 + UP * 2.1, color=CORAL, font_size=36)
        self.play(FadeIn(c), run_time=0.8)
        
        # Animación sutil de cambio de expresión del protagonista
        cambiar_cara(prota, "sorpresa")
        self.wait(0.5)
        
        # Tiempo de espera para completar la escena
        self.wait(7.2)
        
        self.play(
            FadeOut(bt),
            FadeOut(prota),
            FadeOut(cerebro_prop),
            FadeOut(matraz_prop),
            FadeOut(c),
            run_time=0.8
        )