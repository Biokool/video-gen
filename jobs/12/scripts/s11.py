from manim import *
from zenn_rig import *

class S11(Scene):
    def construct(self):
        # 1. Configuración de fondo y título seguro
        self.add(fondo(AZUL_MARINO))
        titulo = titulo_seguro("¿CÓMO FUNCIONA LA PROPIOCEPCIÓN?", color=WHITE)
        self.add(titulo)
        
        # 2. Crear monigote a la izquierda
        fig = stick_idle(pos=LEFT*3.5 + DOWN*0.5, color=WHITE)
        self.add(fig)
        self.wait(1.0)
        
        # 3. Caminar con los ojos cerrados (simulación de propiocepción)
        self.play(stick_walk(fig, LEFT*1.5 + DOWN*0.5, run_time=2.5))
        
        # 4. Añadir expresión de ojos cerrados ("dormido")
        expr_cerrada = expresion(fig, "dormido")
        self.play(FadeIn(expr_cerrada))
        
        # 5. Mostrar el GPS mental (caja) y la flecha de conexión
        gps_prop = caja("GPS", pos=RIGHT*2.5 + UP*1, width=1.8)
        flecha_gps = arrow(start=LEFT*1.5 + UP*0.8, end=RIGHT*1.5 + UP*1, color=YELLOW)
        lbl_gps = etiqueta("GPS Interno", pos=(2.5, -0.2), color=WHITE)
        
        self.play(
            FadeIn(gps_prop),
            Create(flecha_gps),
            Write(lbl_gps),
            run_time=1.5
        )
        self.wait(4.0)
        
        # 6. Transición al "desastre" (fallo de propiocepción)
        self.play(
            FadeOut(gps_prop),
            FadeOut(flecha_gps),
            FadeOut(lbl_gps),
            FadeOut(expr_cerrada),
            run_time=1.0
        )
        
        # Nueva expresión de pánico/sorpresa
        expr_panico = expresion(fig, "miedo")
        self.play(FadeIn(expr_panico))
        
        # Resaltado rojo de alerta y cartel de desastre
        alerta = red_accent(fig, scale=1.3)
        cartel_desastre = callout("¡UN DESASTRE!", color=RED, font_size=80).move_to(RIGHT*2.5 + UP*0.5)
        lbl_torpe = etiqueta("Movimiento torpe", pos=(2.5, -1.0), color=CORAL)
        
        self.play(
            FadeIn(alerta),
            Write(cartel_desastre),
            Write(lbl_torpe),
            run_time=1.5
        )
        self.wait(4.5)