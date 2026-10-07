from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        # 1. Inicializar el fondo de papel estilo divulgación
        self.add(fondo_papel())
        
        # 2. Título de la escena auto-ajustado arriba
        titulo = titulo_seguro("Cálculos Complejos", color=AZUL_MARINO)
        
        # 3. Crear el protagonista (playera azul, expresión confundida, abajo a la izquierda)
        prota = protagonista(
            pos=DOWN * 1.0 + LEFT * 3.0,
            playera="azul",
            altura=2.4,
            expresion="confundido",
            pose="de_pie"
        )
        
        # 4. Elementos de la derecha: Órbita intrincada (curva) y Marte (planeta)
        orbita = curva(
            pos=RIGHT * 2.0 + UP * 0.2,
            ancho=4.5,
            alto=2.5,
            color=INK,
            acento=RED
        )
        
        marte = planeta(
            pos=RIGHT * 4.0 + UP * 1.0,
            radio=0.5,
            color=CORAL
        )
        
        # 5. Calendario para representar el paso del tiempo (tres meses)
        cal = calendario(
            pos=RIGHT * 1.5 + DOWN * 1.2,
            width=1.4
        )
        
        # --- SECUENCIA DE ANIMACIÓN ---
        
        # Aparece el título y el protagonista
        self.play(FadeIn(titulo), run_time=1.0)
        self.play(FadeIn(prota), run_time=1.0)
        self.wait(1.0)
        
        # Se dibuja la órbita compleja y aparece Marte en su trayectoria
        self.play(Create(orbita), run_time=1.5)
        self.play(FadeIn(marte), run_time=1.0)
        
        # El protagonista cambia su expresión a mente explotada ante la complejidad
        cambiar_cara(prota, "mente_explotada")
        
        # Aparece el calendario simbolizando los meses de cálculo
        self.play(FadeIn(cal), run_time=1.0)
        
        # Espera final para completar el tiempo de narración (~9 segundos en total)
        self.wait(2.5)