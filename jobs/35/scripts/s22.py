from manim import *
from zenn_rig import *

class S22(Scene):
    def construct(self):
        self.add(fondo(CREMA))
        
        prota = version_prota(6, pos=DOWN*1.5+LEFT*3.5)
        cambiar_cara(prota, 'sorpresa')
        
        titulo = banda_titulo("ASIMETRÍA CEREBRAL", color=TEAL)
        
        m_cerebro = matraz(pos=RIGHT*3.0+UP*0.5, escala=1.4, liquido=TEAL)
        lbl = etiqueta("¡Lateralidad!", pos=RIGHT*3.0+DOWN*1.2)
        
        arr = arrow(LEFT*1.2+UP*0.5, RIGHT*1.2+UP*0.5, color=INK, width=8)
        
        self.play(
            FadeIn(prota),
            Write(titulo),
            Create(m_cerebro),
            Create(arr),
            FadeIn(lbl),
            run_time=1.5
        )
        
        cambiar_cara(prota, 'alegria_pura')
        self.wait(1.5)
        
        self.wait(1.0)