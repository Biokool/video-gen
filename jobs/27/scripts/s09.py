from manim import *
from zenn_rig import *

class S09(Scene):
    def construct(self):
        # Fondo crema cálido característico del canal
        self.add(fondo_papel())
        
        # Título superior seguro que plantea la gran duda
        banda = banda_titulo("¿Un método torpe por más de un milenio?", color=AZUL_MARINO)
        self.add(banda)
        
        # Protagonista a la izquierda, en zona segura baja
        prota = protagonista(
            pos=DOWN * 1.25 + LEFT * 2.8, 
            playera="azul", 
            altura=2.2, 
            expresion="confundido"
        )
        
        # Elementos visuales a la derecha (reloj y calendario que representan el tiempo)
        reloj = reloj_pared(radius=0.8, pos=RIGHT * 2.8 + UP * 0.8)
        cal = calendario(pos=RIGHT * 2.8 + DOWN * 1.0, width=1.6)
        
        # Entrada de los elementos
        self.play(
            FadeIn(prota),
            Create(reloj),
            Create(cal),
            run_time=1.5
        )
        self.wait(1.0)
        
        # El protagonista cambia su expresión a asombro/mente explotada
        prota_sorprendido = protagonista(
            pos=DOWN * 1.25 + LEFT * 2.8, 
            playera="azul", 
            altura=2.2, 
            expresion="mente_explotada"
        )
        
        # Acento rojo sobre el calendario para enfatizar la enorme duración
        alerta = red_accent(cal, scale=1.3)
        
        self.play(
            Transform(prota, prota_sorprendido),
            Create(alerta),
            run_time=1.5
        )
        
        # Espera final para completar el tiempo de narración
        self.wait(3.0)