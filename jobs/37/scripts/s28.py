from manim import *
from zenn_rig import *

class S28(Scene):
    def construct(self):
        # 1. Fondo de papel para la estética de divulgación
        self.add(fondo_papel())
        
        # 2. Título seguro en la zona superior
        titulo = banda_titulo("El Mito de los Cuernos", color=ORANGE)
        self.add(titulo)
        
        # 3. Protagonista (observador) a la izquierda, abajo para no tocar la banda
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.5, 
            playera="rosa", 
            altura=2.5, 
            expresion="pensando", 
            pose="de_pie"
        )
        
        # 4. Diseñador (Doepler) a la derecha
        doepler = stick_idle(pos=DOWN*1.2 + RIGHT*0.8, height=2.2, color=INK)
        
        # 5. Elementos de diseño: Caja de bocetos y Casco vikingo histórico
        boceto_caja = caja("Bocetos", pos=DOWN*1.2 + RIGHT*2.4, width=1.5)
        casco = casco_vikingo(pos=UP*0.8 + RIGHT*2.4, escala=1.1)
        
        # Flecha que conecta la acción de diseñar con el resultado final
        flecha = arrow(start=RIGHT*1.2 + DOWN*0.1, end=RIGHT*2.0 + UP*0.5, color=RED)
        
        # Etiqueta explicativa en zona segura
        nota = etiqueta("Edad del Bronce", pos=(2.4, -0.4), color=INK)
        
        # --- SECUENCIA DE ANIMACIÓN ---
        # Presentación del protagonista y el entorno
        self.play(FadeIn(prota))
        self.wait(1.5)
        
        # Aparece Doepler trabajando en sus bocetos
        self.play(
            FadeIn(doepler),
            FadeIn(boceto_caja),
            run_time=1.5
        )
        self.wait(1.0)
        
        # Surge la inspiración dramática (el casco con cuernos)
        self.play(
            Create(flecha),
            FadeIn(casco),
            FadeIn(nota),
            run_time=2.0
        )
        self.wait(1.5)
        
        # Reacción de sorpresa del protagonista ante la invención estética
        cambiar_cara(prota, "sorpresa")
        self.wait(2.5)