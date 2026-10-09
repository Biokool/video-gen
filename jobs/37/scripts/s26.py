from manim import *
from zenn_rig import *

class S26(Scene):
    def construct(self):
        # 1. Fondo e interfaz
        self.add(fondo_papel())
        title = titulo_seguro("Mito vs. Realidad", color=INK)
        
        # 2. Elementos iniciales: Protagonista y el famoso casco con cuernos
        prota = protagonista(
            pos=DOWN*1.2 + LEFT*3.0, 
            playera="azul", 
            altura=2.5, 
            expresion="pensando", 
            pose="de_pie"
        )
        
        helmet = casco_vikingo(pos=RIGHT*2.5 + UP*0.2, escala=1.5)
        
        # Entrada en escena
        self.play(
            FadeIn(title),
            FadeIn(prota),
            Create(helmet),
            run_time=1.5
        )
        self.wait(1.0)
        
        # 3. Señalando el casco (el mito popularizado)
        prota_pointing = protagonista(
            pos=DOWN*1.2 + LEFT*3.0, 
            playera="azul", 
            altura=2.5, 
            expresion="sarcastico", 
            pose="senalando"
        )
        self.play(
            Transform(prota, prota_pointing),
            run_time=1.0
        )
        self.wait(1.5)
        
        # 4. Resaltado del error (acento rojo sobre el casco de "disfraz")
        accent = red_accent(helmet, scale=1.4)
        self.play(
            FadeIn(accent),
            run_time=1.0
        )
        self.wait(1.5)
        
        # 5. Revelación de la arqueología (lupa, etiqueta de desmentido y asombro)
        lupa_obj = lupa(pos=RIGHT*0.5 + DOWN*1.0, escala=0.9)
        etiq = etiqueta("Nunca existió", pos=RIGHT*3.0 + DOWN*1.2, color=RED)
        
        prota_shocked = protagonista(
            pos=DOWN*1.2 + LEFT*3.0, 
            playera="azul", 
            altura=2.5, 
            expresion="mente_explotada", 
            pose="brazos_cruzados"
        )
        
        self.play(
            Transform(prota, prota_shocked),
            Create(lupa_obj),
            FadeIn(etiq),
            run_time=1.5
        )
        self.wait(4.0)