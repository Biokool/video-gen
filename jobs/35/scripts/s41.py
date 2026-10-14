from manim import *
from zenn_rig import *

class S41(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título superior seguro para la escena (ÚNICA llamada a banda/título/callout principal)
        self.add(banda_titulo("Tu conciencia se adapta", color=ORANGE))
        
        # Protagonista abajo a la izquierda para evitar solapes
        prota = protagonista(
            pos=DOWN * 1.5 + LEFT * 3.5, 
            playera=PLAYERA_NARANJA, 
            altura=2.6, 
            expresion='pensando', 
            pose='de_pie'
        )
        
        # Prop adicional con color para acompañar la escena (una lupa para observar)
        prop_lupa = lupa(pos=RIGHT * 3.0 + DOWN * 0.5, escala=1.2)
        
        # Usamos etiqueta() en lugar de callout para evitar duplicidad de elementos principales de texto
        aviso = etiqueta("O viceversa...", pos=RIGHT * 3.2 + UP * 1.2, color=INK, font_size=40)
        
        # Animaciones de entrada
        self.play(
            FadeIn(prota, shift=UP),
            FadeIn(prop_lupa, shift=RIGHT),
            run_time=1.0
        )
        
        # Cambio de expresión a sorpresa y aparición de la etiqueta
        cambiar_cara(prota, 'sorpresa')
        self.play(
            FadeIn(aviso, shift=LEFT),
            run_time=1.0
        )
        
        # Breve pausa para la asimilación del concepto
        self.wait(3.0)
        
        # Salida limpia
        self.play(
            FadeOut(prota),
            FadeOut(prop_lupa),
            FadeOut(aviso),
            run_time=1.0
        )