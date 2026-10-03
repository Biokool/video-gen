from manim import *
from zenn_rig import *

class S13(Scene):
    def construct(self):
        # Fondo espacial/nocturno para dar contexto cósmico
        self.add(fondo(INK))
        
        # Elementos de fondo: estrellas y luna
        stars = estrellas(50)
        moon = luna(UP * 3 + RIGHT * 4, 0.8, INK)
        self.play(FadeIn(stars), FadeIn(moon))

        # Crear el monigote principal (astrónomo observador)
        fig = stick_idle(RIGHT * 3, height=2.5, color=WHITE)
        cara = expresion(fig, "preocupado") # Dudando/sorprendido ante lo invisible
        
        # Añadir props: un telescopio o indicador de luz
        telescope = curva(LEFT * 2 + DOWN * 1, 1, 0.5) # Representación abstracta del telescopio
        telescope.set_color(YELLOW)
        
        self.play(FadeIn(fig), FadeIn(cara))
        self.wait(0.5)

        # Narración: "La gravedad curva el espacio"
        # Visualizamos la trayectoria de la luz doblándose
        straight_arrow = arrow(LEFT * 5 + UP * 2, LEFT * 1 + UP * 2, color=YELLOW)
        
        # Objeto masivo (agujero negro o galaxia) en el centro
        # Corrección: Usar Circle para representar el objeto masivo ya que 'esfera' no está definido en el rig estándar/Manim básico
        mass_obj = Circle(radius=1, color=RED)
        mass_accent = red_accent(mass_obj)

        self.play(FadeIn(straight_arrow))
        self.wait(0.5)

        # Efecto de curvatura: la flecha cambia de dirección al pasar cerca del objeto masivo
        # Como no tenemos CurvedPath explícito en el rig, usaremos una transformación visual simple
        # Dibujamos una flecha curva manualmente con líneas si fuera necesario, 
        # pero usaremos callout para reforzar la idea de "gravedad" y "espacio".
        
        self.play(Transform(straight_arrow, arrow(LEFT * 5 + UP * 2, LEFT * 1 + DOWN * 2, color=YELLOW))) # Curvatura simulada
        
        # Callout clave: "GRAVEDAD CURVA EL ESPACIO"
        callout_text = callout("ESPACIO CURVO", TEAL)
        self.play(FadeIn(callout_text))
        
        # El monigote reacciona
        stick_think(fig, "?")
        self.wait(2)
        
        # Salida
        self.play(FadeOut(callout_text), FadeOut(straight_arrow), FadeOut(mass_obj), FadeOut(mass_accent), FadeOut(telescope))
        self.wait(1)