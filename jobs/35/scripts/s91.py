from manim import *
from zenn_rig import *

class S91(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título seguro superior (usando FadeIn en lugar de Write sobre banda_titulo)
        titulo = banda_titulo("¿Lotería biológica o azar?", color=ORANGE)
        self.play(FadeIn(titulo))
        
        # Protagonista abajo a la izquierda (respetando layout con banda y zona de subtítulos)
        prota = protagonista(pos=DOWN*1.2+LEFT*3.5, playera=PLAYERA_AZUL, altura=2.4, expresion="pensando", pose="de_pie")
        self.play(FadeIn(prota))
        
        # Prop temático a la derecha (ADN y una etiqueta secundaria compacta)
        dna = adn(pos=RIGHT*3.5+UP*0.2, escala=1.1, color=TEAL)
        et = etiqueta("¿Genética o suerte?", pos=RIGHT*3.5+DOWN*1.2, color=CORAL, font_size=40)
        
        self.play(Create(dna), FadeIn(et))
        
        # Animación de cambio de cara y movimientos del protagonista por separado
        cambiar_cara(prota, "sorpresa")
        self.play(prota.animate.shift(UP*0.2), run_time=0.5)
        self.play(prota.animate.shift(DOWN*0.2), run_time=0.5)
        
        self.wait(2)