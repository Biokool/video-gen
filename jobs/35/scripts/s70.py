from manim import *
from zenn_rig import *

class S70(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        # Título superior seguro: banda_titulo devuelve un Mobject, se usa con FadeIn o Create, NUNCA directamente en self.play() con argumentos inválidos o sin animación.
        titulo = banda_titulo("¿Lotería biológica y suerte?", color=AZUL_MARINO)
        self.play(FadeIn(titulo))
        
        # Protagonista abajo a la izquierda con playera azul y expresión de duda
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.5,
            playera=PLAYERA_AZUL,
            altura=2.5,
            expresion="pensando",
            pose="de_pie"
        )
        self.play(FadeIn(prota))
        
        # Props visuales temáticos (ADN y moneda dorada)
        dna_obj = adn(pos=UP * 0.3 + RIGHT * 2.0, escala=0.9, color=TEAL)
        coin = moneda_dorada(texto="$", pos=UP * 1.5 + RIGHT * 4.5, radio=0.7)
        
        self.play(
            Create(dna_obj),
            FadeIn(coin, shift=UP*0.5),
            run_time=1.0
        )
        
        # Usamos etiqueta() para texto secundario
        c = etiqueta("Genes, madre y azar", pos=RIGHT * 3.4 + DOWN * 0.8, color=ORANGE, font_size=40)
        self.play(FadeIn(c))
        
        # Animación sutil de cambio de cara y espera
        cambiar_cara(prota, "sorpresa")
        self.wait(3.5)
        
        # Salida limpia
        self.play(
            FadeOut(titulo),
            FadeOut(prota),
            FadeOut(dna_obj),
            FadeOut(coin),
            FadeOut(c),
            run_time=0.8
        )