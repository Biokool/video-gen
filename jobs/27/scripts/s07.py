from manim import *
from zenn_rig import *

class S07(Scene):
    def construct(self):
        # 1. Inicializar fondo estilo papel
        self.add(fondo_papel())
        
        # 2. Título seguro en la parte superior
        titulo = titulo_seguro("Precisión de Solo 1 Grado", color=AZUL_MARINO)
        self.add(titulo)
        
        # 3. Protagonista (abajo a la izquierda, playera azul, sorprendido)
        prota = protagonista(
            pos=LEFT * 3.8 + DOWN * 1.3, 
            playera="azul", 
            altura=2.4, 
            expresion="sorpresa",
            pose="de_pie"
        )
        
        # 4. Regla de medir (construida con líneas simples)
        regla = VGroup()
        barra_principal = Line(LEFT * 2, RIGHT * 2, color=INK, stroke_width=6)
        regla.add(barra_principal)
        
        # Marcas de graduación de la regla
        for x in np.arange(-2.0, 2.1, 0.5):
            tick = Line(UP * 0.15, DOWN * 0.15, color=INK, stroke_width=4).shift(RIGHT * x)
            regla.add(tick)
            
        regla.move_to(RIGHT * 2.5 + DOWN * 0.8)
        
        # Marca de error mínima en rojo
        marca_roja = Line(UP * 0.3, DOWN * 0.3, color=RED, stroke_width=8).shift(RIGHT * 2.0 + DOWN * 0.8)
        lbl_error = etiqueta("Error: 1°", pos=(2.0, -0.1), color=RED, font_size=36)
        
        # 5. Ojo grande de observación
        ojo = ojo_grande(pos=RIGHT * 1.0 + UP * 1.0, escala=1.2)
        
        # --- Secuencia de Animación ---
        
        # Entrada del protagonista
        self.play(
            FadeIn(prota),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Aparece la regla de medir y el ojo que observa
        self.play(
            Create(regla),
            FadeIn(ojo),
            run_time=1.5
        )
        self.wait(1.0)
        
        # El ojo se acerca a la regla y se revela la marca de error mínimo
        self.play(
            ojo.animate.shift(RIGHT * 0.5 + DOWN * 0.3),
            Create(marca_roja),
            Write(lbl_error),
            run_time=1.5
        )
        
        # Énfasis visual en la precisión (acento rojo)
        acento = red_accent(marca_roja, scale=1.4)
        self.play(
            FadeIn(acento),
            run_time=0.8
        )
        
        # El protagonista reacciona con asombro masivo (mente explotada)
        cambiar_cara(prota, "mente_explotada")
        self.play(
            prota.animate.shift(RIGHT * 0.2),
            run_time=0.7
        )
        
        # Espera final para completar la narración
        self.wait(2.0)