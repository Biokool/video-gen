from manim import *
from zenn_rig import *

class S05(Scene):
    def construct(self):
        # 1. Inicializar fondo estilo papel
        self.add(fondo_papel())
        
        # 2. Título seguro en la parte superior
        title = titulo_seguro("El Modelo Ptolomeico", color=INK)
        
        # 3. Protagonista señalando desde la izquierda (zona segura, abajo)
        prota = protagonista(
            pos=DOWN * 1.2 + LEFT * 3.2, 
            playera="azul", 
            altura=2.5, 
            expresion="sorpresa", 
            pose="senalando"
        )
        
        # Mostrar título y protagonista
        self.play(
            FadeIn(title),
            FadeIn(prota),
            run_time=1.2
        )
        
        # 4. Crear el sistema de órbitas complejas (Tierra en el centro)
        # Tierra (centro del modelo geocéntrico)
        tierra = planeta(pos=RIGHT * 2 + UP * 0.2, radio=0.5, color=TEAL)
        
        # Órbita principal (deferente)
        c1 = Circle(radius=1.4, color=INK, stroke_width=2).move_to(RIGHT * 2 + UP * 0.2)
        
        # Epiciclo 1 (círculo sobre la órbita)
        c2 = Circle(radius=0.7, color=CORAL, stroke_width=2).move_to(RIGHT * 3.4 + UP * 0.2)
        
        # Epiciclo 2 (más complejidad)
        c3 = Circle(radius=0.3, color=MOSTAZA, stroke_width=1.5).move_to(RIGHT * 3.4 + UP * 0.9)
        
        # Planeta orbitando en el extremo
        planeta_movil = planeta(pos=RIGHT * 3.4 + UP * 1.2, radio=0.15, color=ORANGE)
        
        # Agrupamos el sistema de epiciclos para animar su rotación conjunta
        sistema_epiciclos = VGroup(c2, c3, planeta_movil)
        
        # Animar la aparición del sistema astronómico
        self.play(
            Create(tierra),
            Create(c1),
            run_time=1.0
        )
        
        self.play(
            Create(sistema_epiciclos),
            run_time=1.0
        )
        
        # 5. Añadir etiqueta explicativa en zona segura inferior derecha
        lbl = etiqueta("Complejidad Geocéntrica", pos=RIGHT * 2 + DOWN * 1.8, color=INK)
        self.play(Write(lbl), run_time=0.8)
        
        # 6. Simular el movimiento orbital complejo y cambiar la expresión del protagonista
        # Cambiamos la cara del protagonista a "mente_explotada" ante tanta complejidad
        cambiar_cara(prota, "mente_explotada")
        
        self.play(
            Rotate(
                sistema_epiciclos, 
                angle=180 * DEGREES, 
                about_point=RIGHT * 2 + UP * 0.2, 
                run_time=3.0, 
                rate_func=smooth
            )
        )
        
        # Espera final para completar el tiempo de narración
        self.wait(2.0)