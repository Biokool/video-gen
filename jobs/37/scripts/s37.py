from manim import *
from zenn_rig import *

class S37(Scene):
    def construct(self):
        # Fondo de papel estilo Zenn
        self.add(fondo_papel())
        
        # Título superior seguro, auto-ajustado
        banda = banda_titulo("¿QUÉ CASCO IMPACTA MÁS?", color=MOSTAZA)
        self.add(banda)
        
        # Protagonista a la izquierda, abajo (zona segura y <= -1.2, altura <= 2.6)
        prota = protagonista(
            pos=LEFT * 3.8 + DOWN * 1.2, 
            playera="amarilla", 
            altura=2.4, 
            expresion="pensando", 
            pose="de_pie"
        )
        
        self.play(FadeIn(prota))
        self.wait(1.0)
        
        # Casco 1: Gjermundbu (Histórico, simple y funcional)
        casco_real = casco_vikingo(pos=LEFT * 0.2 + UP * 0.5, escala=0.9)
        casco_real.set_color(GRAY)
        label_real = etiqueta("Gjermundbu\n(Funcional)", pos=LEFT * 0.2 + DOWN * 1.2, color=AZUL_MARINO)
        
        self.play(
            FadeIn(casco_real),
            Write(label_real),
            run_time=1.5
        )
        self.wait(1.5)
        
        # Casco 2: Fantasía (Con cuernos, aspecto de demonio de batalla)
        casco_mito = casco_vikingo(pos=RIGHT * 3.8 + UP * 0.5, escala=1.3)
        casco_mito.set_color(ORANGE)
        label_mito = etiqueta("Mito con Cuernos\n(Demonio)", pos=RIGHT * 3.8 + DOWN * 1.2, color=RED)
        
        self.play(
            FadeIn(casco_mito),
            Write(label_mito),
            run_time=1.5
        )
        
        # Destacar el casco de fantasía para denotar su impacto visual exagerado
        acento = red_accent(casco_mito, scale=1.35)
        self.play(
            Create(acento),
            run_time=1.0
        )
        
        # Reacción del protagonista ante la comparación
        cambiar_cara(prota, "confundido")
        self.wait(2.0)
        
        cambiar_cara(prota, "mente_explotada")
        self.wait(2.0)