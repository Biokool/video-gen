from manim import *
from zenn_rig import *

class S13(Scene):
    def construct(self):
        # 1. Fondo de papel para estilo divulgación
        self.add(fondo_papel())
        
        # 2. Título seguro de la escena (evita zona de subtítulos y bordes)
        titulo = titulo_seguro("La Herejía de Mover la Tierra", color=AZUL_MARINO)
        self.add(titulo)
        
        # 3. Protagonista en zona segura (izquierda y abajo)
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera="verde", 
            altura=2.4, 
            expresion="pensando"
        )
        
        # 4. Elementos del centro del universo (Tierra y etiqueta)
        tierra = planeta(pos=RIGHT*1.5 + DOWN*0.8, radio=0.75, color=TEAL)
        lbl_centro = etiqueta("Centro", pos=(1.5, -1.9), color=INK)
        
        self.play(
            FadeIn(prota),
            FadeIn(tierra),
            FadeIn(lbl_centro),
            run_time=1.0
        )
        self.wait(0.5)
        
        # 5. Animación: Desplazar la Tierra del centro
        self.play(
            tierra.animate.move_to(RIGHT*3.2 + UP*0.4),
            lbl_centro.animate.set_opacity(0.4),
            run_time=1.5
        )
        
        # Cambiar la cara del protagonista a reprobación/miedo ante la herejía
        cambiar_cara(prota, "miedo")
        self.play(prota.animate.scale(1.05), run_time=0.3)
        
        # 6. Aparece la sombra con forma de cruz (amenaza de la inquisición/herejía)
        cruz_v = Rectangle(width=0.35, height=2.2, color=INK, fill_opacity=0.25, stroke_width=0)
        cruz_h = Rectangle(width=1.5, height=0.35, color=INK, fill_opacity=0.25, stroke_width=0).shift(UP*0.4)
        sombra_cruz = VGroup(cruz_v, cruz_h).move_to(RIGHT*1.0 + UP*0.5)
        
        # Etiqueta de advertencia y acento rojo sobre la Tierra desplazada
        lbl_herejia = etiqueta("¡Herejía!", pos=(3.2, 1.5), color=RED)
        alerta = red_accent(tierra, scale=1.3)
        
        self.play(
            FadeIn(sombra_cruz, shift=UP*0.2),
            FadeIn(lbl_herejia),
            FadeIn(alerta),
            run_time=1.2
        )
        self.wait(1.0)