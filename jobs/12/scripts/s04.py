from manim import *
from zenn_rig import *

class S04(Scene):
    def construct(self):
        # Configurar fondo cálido característico del estilo
        self.add(fondo(CREMA))
        
        # Título superior seguro auto-ajustado
        titulo = banda_titulo("LA ILUSIÓN DE LOS CINCO SENTIDOS", color=AZUL_MARINO)
        self.add(titulo)
        
        # Presentar a Aristóteles (monigote a la izquierda)
        aristoteles = stick_idle(pos=LEFT * 3.8 + DOWN * 0.5, height=2.2, color=INK)
        cara_normal = expresion(aristoteles, "normal")
        self.play(FadeIn(aristoteles), FadeIn(cara_normal))
        self.wait(1.0)
        
        # Aristóteles postula los 5 sentidos (bocadillo de pensamiento)
        pensamiento = stick_think(aristoteles, "¡Solo 5 sentidos!")
        self.play(FadeIn(pensamiento))
        self.wait(1.0)
        
        # Mostrar ejemplos de los sentidos clásicos en la derecha
        ojo = ojo_grande(pos=RIGHT * 1.5 + UP * 0.6, escala=0.8)
        comida = pastel(pos=RIGHT * 4.5 + UP * 0.6, width=1.2)
        lbl_vista = etiqueta("Vista", pos=RIGHT * 1.5 + UP * 1.5, color=INK)
        lbl_gusto = etiqueta("Gusto", pos=RIGHT * 4.5 + UP * 1.5, color=INK)
        
        self.play(
            FadeIn(ojo), 
            FadeIn(comida),
            Write(lbl_vista),
            Write(lbl_gusto)
        )
        self.wait(3.0)
        
        # Transición: Desvanecer los sentidos para dar paso al concepto del tiempo transcurrido
        self.play(
            FadeOut(pensamiento),
            FadeOut(ojo),
            FadeOut(comida),
            FadeOut(lbl_vista),
            FadeOut(lbl_gusto)
        )
        
        # Aristóteles se sorprende al ver cuánto duró su idea
        cara_sorpresa = expresion(aristoteles, "sorpresa")
        self.play(Transform(cara_normal, cara_sorpresa))
        
        # Elementos que representan el paso de más de dos mil años
        reloj = reloj_pared(radius=0.8, pos=RIGHT * 3.0 + UP * 0.8)
        cal = calendario(pos=RIGHT * 3.0 + DOWN * 0.7, width=1.5)
        lbl_tiempo = etiqueta("¡2.000 AÑOS!", pos=RIGHT * 3.0 + DOWN * 1.8, color=RED)
        
        self.play(
            FadeIn(reloj),
            FadeIn(cal),
            Write(lbl_tiempo)
        )
        self.wait(4.0)