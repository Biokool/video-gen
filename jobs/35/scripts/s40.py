from manim import *
from zenn_rig import *

class S40(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        prota = protagonista(pos=DOWN*1.5+LEFT*3.5, playera=PLAYERA_NARANJA, altura=2.4, expresion='triste', pose='senalando')
        
        grupo_criticos = stick_group(3, center=RIGHT*2.5+UP*0.5, spacing=1.3, height=2.0, color=INK, seed=42)
        for fig in grupo_criticos:
            expresion(fig, 'preocupado')
        
        txt_titulo = banda_titulo("¿Zurdo obligado a ser diestro?", color=ORANGE)
        
        flecha = arrow(start=grupo_criticos.get_left() + LEFT*0.2, end=prota.get_top() + RIGHT*0.5, color=RED, width=8)
        
        self.play(
            FadeIn(prota),
            FadeIn(grupo_criticos),
            FadeIn(txt_titulo),
            run_time=1.0
        )
        
        self.play(
            Create(flecha),
            run_time=1.0
        )
        
        cambiar_cara(prota, 'pensando')
        self.wait(2.0)
        
        self.play(
            FadeOut(prota),
            FadeOut(grupo_criticos),
            FadeOut(txt_titulo),
            FadeOut(flecha),
            run_time=1.0
        )