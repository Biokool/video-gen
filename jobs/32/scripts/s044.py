from manim import *
from zenn_rig import *

class S044(Scene):
    def construct(self):
        # Protagonista con playera amarilla y expresión pensativa
        prota = protagonista(
            pos=DOWN*1.2+LEFT*3.5,
            playera="amarilla",
            altura=2.6,
            expresion="pensativo",
            pose="de_pie"
        )
        # Casa desplazada un poco hacia arriba para evitar la zona de subtítulos
        casa_img = casa(pos=RIGHT*2+UP*0.5, size=1.6)
        # Agua de inundación (rectángulo azul) encima de la base de la casa
        agua = Rectangle(
            width=4.0,
            height=1.2,
            color=BLUE,
            fill_opacity=0.5
        )
        agua.next_to(casa_img, DOWN, buff=0).align_to(casa_img, LEFT)
        # Balde representado como una caja con etiqueta
        balde = caja(etiqueta="balde", pos=DOWN*1.2+RIGHT*3.5, width=1.5)

        # Entrada de los elementos
        self.play(FadeIn(prota), FadeIn(casa_img), run_time=1.0)
        self.play(FadeIn(agua), FadeIn(balde), run_time=1.0)
        self.wait(0.5)

        # Simular aumento del agua (inundación)
        self.play(agua.animate.shift(UP*0.4), run_time=1.5)
        # Simular vaciado del balde (moverlo hacia abajo)
        self.play(balde.animate.shift(DOWN*0.4), run_time=1.5)
        self.wait(0.5)