from manim import *

# Importaciones necesarias de la librería externa si existen, 
# pero como el error es por falta de definición de 'circulo', 
# asumimos que las funciones custom de zenn_rig están disponibles en el entorno.
# Si este código se ejecuta en un entorno sin 'zenn_rig', estas importaciones fallarán.
# Sin embargo, para corregir el error específico del prompt (NameError: circulo), 
# redefiniremos la función faltante y mantendremos la estructura lógica.

def circulo(radio=1, fill_color=None, stroke_color=None, stroke_width=2, fill_opacity=0, **kwargs):
    """Helper para crear un círculo con sintaxis simplificada."""
    return Circle(
        radius=radio,
        fill_color=fill_color,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        fill_opacity=fill_opacity,
        **kwargs
    )

# Nota: Se asume que las funciones 'fondo', 'stick_idle', 'expresion', 
# 'estrellas', 'title_card', 'callout', 'stick_point', 'stick_think' 
# están definidas en el módulo externo o en el ámbito global del script completo.
# Para que este bloque sea válido sintácticamente y corregible, las simulamos si no existen
# para evitar NameErrors adicionales si se ejecuta de forma aislada (aunque en la práctica
# estas vendrían de 'zenn_rig').

def fondo(color): return Rectangle(width=16, height=9, fill_color=color, fill_opacity=1).set_z_index(-1)
def stick_idle(pos, height, color): return Dot(pos, color=color) # Simplificación para evitar errores si no está definido
def expresion(obj, tipo): return obj # Simplificación
def estrellas(n): return VGroup(*[Dot(np.random.uniform([-8,8],[-4.5,4.5]), color=WHITE).scale(0.1) for _ in range(n)])
def title_card(texto, color): return Text(texto, font_size=48, color=color)
def callout(texto, color): return Text(texto, font_size=36, color=color)
def stick_point(obj, pos): pass # Simplificación
def stick_think(obj, texto): pass # Simplificación

from zenn_rig import * # Intentamos importar la librería real si existe en el entorno de renderizado

class S15(Scene):
    def construct(self):
        # Escena nocturna/espacial para las galaxias
        self.add(fondo(INK))
        
        # Crear el monigote principal (astrónomo/pensador)
        fig = stick_idle(LEFT * 3, height=2.2, color=WHITE)
        
        # Expresión de sorpresa/investigación al descubrir algo
        cara = expresion(fig, "sorpresa")
        
        # Crear props visuales: un cúmulo de galaxias (representado abstractamente con estrellas y un planeta central oscuro)
        estrellado = estrellas(50)
        
        # CORRECCIÓN AQUÍ: 'circulo' no estaba definido en el scope global del script original.
        # Se usa la función helper definida arriba o importada si está disponible.
        centro_masa = circulo(radio=1.5, fill_color=BLACK, fill_opacity=1).move_to(RIGHT * 2)
        halo_gravitacional = circulo(radio=2.5, stroke_color=YELLOW, stroke_width=2, fill_opacity=0).move_to(RIGHT * 2)
        
        # Título inicial para contexto
        titulo = title_card("La Masa Oculta", YELLOW)
        
        # Secuencia de animación
        self.play(FadeIn(estrellado), run_time=1.5)
        self.wait(0.5)
        
        # Aparece el monigote pensando
        self.play(FadeIn(fig), FadeIn(cara))
        self.wait(1)
        
        # El monigote señala hacia la masa invisible (derecha)
        stick_point(fig, RIGHT * 2 + UP * 0.5)
        
        # Revelación visual: el halo y la masa central aparecen
        self.play(Create(halo_gravitacional), FadeIn(centro_masa))
        
        # Callout de texto clave
        callout_text = callout("Materia Invisible", RED)
        self.play(Transform(cara, expresion(fig, "preocupado"))) # La gravedad es fuerte
        self.wait(1.5)
        
        # Conclusión: confirmación
        callout_final = callout("Gravedad Visible", GREEN)
        stick_think(fig, "¡Existen!")
        
        self.wait(2)

        # Limpieza final (opcional, Manim lo hace al salir)
        pass