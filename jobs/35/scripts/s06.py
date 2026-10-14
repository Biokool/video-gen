from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        self.add(fondo_papel())
        
        # Título seguro en la zona superior (único elemento principal de texto arriba)
        self.play(Write(banda_titulo("Más de 40 genes influyen en la lateralidad", color=ORANGE)))
        
        # Protagonista abajo a la izquierda (con altura controlada para no chocar con la banda)
        prota = protagonista(pos=DOWN*1.5+LEFT*3.8, playera=PLAYERA_VERDE, altura=2.4, expresion="mente_explotada", pose="senalando")
        self.play(FadeIn(prota))
        
        # Grupo secundario representando los múltiples factores/músicos
        grupo = stick_group(n=5, center=RIGHT*2.5+UP*0.2, spacing=1.2, height=2.0, color=INK, seed=7)
        self.play(FadeIn(grupo))
        
        # Se elimina el callout duplicado en la zona superior para evitar sobreposición con banda_titulo.
        # Usamos etiqueta() a un lado del grupo secundario.
        dato = etiqueta("¡Como una orquesta!", pos=RIGHT*2.8+DOWN*1.8, color=TEAL, font_size=40)
        self.play(FadeIn(dato))
        
        # Pequeño movimiento dinámico de la escena
        self.play(
            prota.animate.shift(UP*0.2),
            grupo.animate.shift(LEFT*0.3),
            run_time=1.5
        )
        
        self.wait(5.0)