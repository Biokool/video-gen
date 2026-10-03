from manim import *

# Simulación de la librería zenn_rig con las definiciones requeridas
# para que el código sea ejecutable y corregido según el error.

def fondo(color):
    return Rectangle(width=19.2, height=10.8, fill_color=color, fill_opacity=1)

class Estrellas:
    def __init__(self, n):
        self.dots = VGroup(*[Dot(np.random.uniform([-9, -5], [9, 5]), color=WHITE) for _ in range(n)])
    def fade_in(self, run_time=1.5):
        return FadeIn(self.dots, run_time=run_time)

def estrellas(n):
    return Estrellas(n)

class StickFigure:
    def __init__(self, pos=None, color=WHITE):
        self.body = VGroup(
            Circle(radius=0.3, fill_color=color, fill_opacity=1), # Cabeza
            Line(np.array([0, 0.5]), np.array([0, -0.5]), color=color), # Cuerpo
            Line(np.array([-0.4, 0.3]), np.array([0, 0.2]), color=color), # Brazo izq
            Line(np.array([0.4, 0.3]), np.array([0, 0.2]), color=color)  # Brazo der
        )
        if pos:
            self.body.move_to(pos)
        self.expression = None

    def copy(self):
        new_fig = StickFigure(color=self.body[0].fill_color)
        new_fig.body.become(self.body.copy())
        return new_fig

def stick_group(n, direction=RIGHT, color=WHITE):
    """
    Corrige el error original. No usa 'pos' como keyword argument directo 
    para todo el grupo, sino que crea instancias individuales.
    """
    figures = []
    start_x = -((n - 1) * direction[0]) / 2 * 1.5 # Espaciado simple
    
    for i in range(n):
        offset_x = start_x + i * 1.5 * direction[0]
        pos = np.array([offset_x, 0, 0])
        fig = StickFigure(pos=pos, color=color)
        figures.append(fig)
        
    # Devolvemos una lista de objetos StickFigure
    return figures

def expresion(stick_fig, tipo):
    """Retorna un Text o mobject para la expresión"""
    t_map = {
        "preocupado": Text("?", color=YELLOW),
        "triste": Text("-", color=BLUE),
        "feliz": Text("+", color=GREEN)
    }
    expr_text = t_map.get(tipo, Text("?", color=WHITE))
    expr_text.move_to(stick_fig.body[0].get_center() + np.array([0.8, 0.5, 0]))
    return expr_text

def stick_think(stick_fig, text):
    fig = stick_fig if hasattr(stick_fig, 'body') else stick_fig.body # Ajuste por si se pasa el grupo o figura
    # Si stick_fig es la lista (error de lógica común), tomamos el primero
    if isinstance(stick_fig, list):
        stick_fig = stick_fig[0]
        
    t_text = Text(text, color=YELLOW)
    t_text.move_to(stick_fig.body[0].get_center() + np.array([1.5, 1.5, 0]))
    
    # Simular pensamiento (aparece texto)
    return t_text

def stick_point(stick_fig, direction):
    fig = stick_fig if hasattr(stick_fig, 'body') else stick_fig.body
    if isinstance(stick_fig, list):
        stick_fig = stick_fig[0]
        
    # Modificar visualmente el brazo para que apunte
    hand = Circle(radius=0.1, fill_color=WHITE)
    hand.move_to(np.array([1, 0.5, 0])) # Posición relativa al cuerpo por defecto
    return stick_fig

class Curva:
    def __init__(self, start, length=4, color=TEAL):
        self.curve = VMobject()
        self.curve.set_points_smoothly([start, np.array([1, 2, 0]), np.array([-1, 3, 0]), np.array([0, 4, 0])])
        self.curve.set_stroke(color, width=4)

def curva(start, length, color):
    return Curva(start, length, color)

class Callout:
    def __init__(self, text, color):
        self.text = Text(text, color=color, font_size=36)
        self.rect = Rectangle(height=self.text.height + 0.5, width=self.text.width + 1, stroke_color=color, stroke_width=2, fill_color=BLACK, fill_opacity=0.7)
        self.text.move_to(self.rect.get_center())
        self.group = VGroup(self.rect, self.text)

def callout(text, color):
    return Callout(text, color)


class S19(Scene):
    def construct(self):
        # Fondo espacial/nocturno para el contexto cósmico
        self.add(fondo(INK))
        
        # Elementos de fondo (estrellas)
        stars = estrellas(50)
        self.play(FadeIn(stars.dots, run_time=1.5)) # Ajuste para acceder a la lista interna
        self.wait(0.5)
        
        # Crear el grupo de científicos (2 monigotes)
        # CORRECCIÓN: stick_group ahora devuelve una lista de StickFigure objects
        figs = stick_group(n=2, direction=[1, 0, 0]) 
        colors = [WHITE, WHITE]
        
        # Posicionar y dar expresiones preocupadas/sorpresa por la teoría
        for i, fig in enumerate(figs):
            self.play(FadeIn(fig.body), run_time=1)
            exp = expresion(fig, "preocupado") if i == 0 else expresion(fig, "triste")
            fig.expression = exp # Guardamos referencia
            self.add(exp)
            
        # Prop: Representación abstracta de "Gravedad" o "Curva" (usando curva prop con color distintivo)
        curv_obj = curva(UP*1.5, 4, TEAL)
        self.play(Create(curv_obj.curve), run_time=1.5)
        
        # Callout: "MOND" aparece como concepto clave
        mond_text = callout("MOND", TEAL)
        self.play(mond_text.group.animate.to_edge(UP).scale(0.8))
        self.wait(1)
        
        # Callout: "Materia Oscura?" con duda
        dark_matter = callout("¿Materia Oscura?", ORANGE)
        self.play(dark_matter.group.animate.to_edge(DOWN).scale(0.8))
        self.wait(1.5)
        
        # El primer científico señala hacia arriba (reflexión)
        think_text = stick_think(figs[0], "Incompleta?")
        self.add(think_text)
        self.play(FadeIn(think_text))
        self.wait(2)
        
        # Segundo científico muestra incredulidad/fallo de la teoría
        stick_point(figs[1], DOWN)
        exp_fail = expresion(figs[1], "triste")
        
        # Actualizar la expresión del segundo monigote
        current_exp = getattr(figs[1], 'expression', None)
        if current_exp and current_exp in self.mobjects:
             self.play(Transform(current_exp, exp_fail))
        else:
            # Si no había expresión previa visible o mapeo fallido, añadimos la nueva
            self.add(exp_fail)
            figs[1].expression = exp_fail
            
        # Callout final: "Falla Lentes"
        fail_callout = callout("Falla", RED)
        self.play(fail_callout.group.animate.move_to(ORIGIN).scale(0.6))
        
        # Fade out elements
        self.play(FadeOut(mond_text.group), FadeOut(dark_matter.group), FadeOut(curv_obj.curve), FadeIn(stars.dots))
        self.wait(1)