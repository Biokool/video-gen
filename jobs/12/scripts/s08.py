from manim import *
from zenn_rig import *

class S08(Scene):
    def construct(self):
        # 1. Fondo de la escena (Tono claro/crema para el día)
        self.add(fondo(CREMA))
        
        # 2. Título seguro en la zona superior (y=3.0)
        title = titulo_seguro("¿Sentidos Ocultos?", color=INK, y=3.0)
        self.play(Write(title), run_time=1.0)
        
        # 3. Creación de personajes y props principales
        # Stick figure a la izquierda, casa (representando las habitaciones/puertas) a la derecha
        stick = stick_idle(pos=np.array([-3.5, -0.8, 0]), height=2.2, color=INK)
        expr_sorpresa = expresion(stick, "sorpresa")
        home = casa(pos=np.array([2.5, -0.8, 0]), size=2.2)
        
        self.play(
            FadeIn(stick),
            FadeIn(expr_sorpresa),
            Create(home),
            run_time=1.5
        )
        self.wait(1.0)
        
        # 4. Acción: El monigote señala a la casa de los secretos
        pointing_stick = stick_point(stick, home.get_center())
        self.play(
            Transform(stick, pointing_stick),
            FadeOut(expr_sorpresa),
            run_time=1.0
        )
        
        # Nueva expresión de curiosidad/felicidad al descubrir algo
        expr_feliz = expresion(pointing_stick, "feliz")
        self.play(FadeIn(expr_feliz), run_time=0.5)
        
        # 5. Etiquetas de apoyo visual y acento rojo de revelación
        lbl_house = etiqueta("Habilidades Ocultas", pos=np.array([2.5, 1.2, 0]), color=INK)
        lbl_super = etiqueta("¿Superhumano?", pos=np.array([-3.5, 1.2, 0]), color=CORAL)
        accent = red_accent(home, scale=1.3)
        
        self.play(
            FadeIn(lbl_house),
            FadeIn(lbl_super),
            Create(accent),
            run_time=1.5
        )
        
        # 6. Espera final para completar el tiempo de narración (~9 segundos en total)
        self.wait(2.5)