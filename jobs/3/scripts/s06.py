from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        # 1. Setup: Fondo espacial (nocturno)
        self.add(fondo(INK))
        
        # Generar estrellas. Evitar conflicto de nombre con la función 'estrellas'
        # Asumiendo que 'estrellas' es una función que devuelve un VGroup o Mobject
        # Si 'estrellas' es la función, no podemos asignar su valor a una variable llamada 'estrellas'
        # en el mismo scope si luego queremos usar la función, pero aquí solo se usa una vez.
        # El error UnboundLocalError sugiere que Python piensa que 'estrellas' se asigna localmente
        # antes de ser usado, o que hay un conflicto de scope.
        # Solución: Usar un nombre de variable diferente.
        grupo_estrellas = estrellas(20)
        self.play(FadeIn(grupo_estrellas), run_time=1.0)
        
        # 2. Título
        titulo = title_card("1970: La Curva de Rotación", YELLOW)
        self.play(FadeIn(titulo), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(titulo), run_time=1.0)

        # 3. Vera Rubin (Monigote)
        vera = stick_idle(LEFT * 3, color=WHITE)
        self.play(FadeIn(vera), run_time=1.0)
        
        # Expresión: Asombrada/Preocupada por el hallazgo
        cara_sorpresa = expresion(vera, "sorpresa")
        self.play(FadeIn(cara_sorpresa), run_time=0.5)

        # 4. Prop: Galaxia representada por un planeta grande o curva
        galaxia = planeta(ORIGIN + RIGHT * 2, radio=1.5, color=TEAL)
        self.play(FadeIn(galaxia), run_time=1.0)
        
        # 5. Gráfica de Rotación (Prop: curva)
        grafico = curva(ORIGIN + RIGHT * 2 + DOWN * 2.5, ancho=3.0, alto=1.5)
        self.play(FadeIn(grafico), run_time=1.5)
        
        # Explicación visual: La curva es plana
        callout1 = callout("Velocidad Plana", color=YELLOW, font_size=96)
        callout1.next_to(grafico, UP, buff=0.5)
        self.play(FadeIn(callout1), run_time=1.0)
        self.wait(2.0)

        # 6. Vera señala la curva
        # En lugar de usar stick_point que puede tener errores internos con arrays inhomogéneos,
        # movemos la posición del brazo usando la API estándar de Manim si es posible,
        # o simplemente hacemos un fade out/in para simular el movimiento si la API es limitada.
        # Asumiendo que stick_point devuelve un Animation, pero el error vino de dentro de zenn_rig.
        # Para ser seguro, usamos un Transform o simplemente no usamos la función problemática si falla.
        # Sin embargo, el error indica que falla al renderizar el archivo.
        # Si stick_point es la causa, la alternativa es mover el mobject 'vera' parcialmente o usar una animación de rotación.
        # Dado que no podemos modificar zenn_rig.py, evitaremos la llamada a stick_point si es la causa del error.
        # Pero el error era ValueError en line 100 de zenn_rig.py.
        # Probablemente 'target' tenía una forma incorrecta.
        # Grafico es un Mobject, su centro es un np.array de tamaño 3.
        # shoulder es un np.array de tamaño 3.
        # El problema podría ser que 'target' está siendo pasado como algo que no es un array de floats simples.
        # Para corregir el código del Scene sin tocar zenn_rig, podemos evitar usar stick_point
        # y usar una animación más simple como Rotate o Transform para