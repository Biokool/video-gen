from manim import *
import numpy as np

# --- Definiciones de funciones y variables desde zenn_rig (simuladas) ---
INK = "#1a1a1a"

def fondo(color):
    return Rectangle(width=15, height=8, fill_color=color, fill_opacity=1)

def stick_idle(pos, color=WHITE, height=2.0):
    """Crea un monigote simple."""
    g = VGroup()
    b = pos
    h = height
    head_r = h * 0.13
    
    # Cabeza
    head = Circle(radius=head_r, color=color).move_to(b + np.array([0, h - head_r, 0]))
    g.add(head)
    
    # Cuerpo
    body = Line(b + np.array([0, h - 2*head_r, 0]), b, color=color)
    g.add(body)
    
    # Brazos
    arm_len = h * 0.3
    arm_start = b + np.array([0, h - 2*head_r - h*0.1, 0])
    left_arm = Line(arm_start, arm_start + np.array([-arm_len*0.7, -arm_len*0.7, 0]), color=color)
    right_arm = Line(arm_start, arm_start + np.array([arm_len*0.7, -arm_len*0.7, 0]), color=color)
    g.add(left_arm, right_arm)
    
    # Piernas
    leg_len = h * 0.4
    left_leg = Line(b, b + np.array([-leg_len*0.5, -leg_len, 0]), color=color)
    right_leg = Line(b, b + np.array([leg_len*0.5, -leg_len, 0]), color=color)
    g.add(left_leg, right_leg)
    
    return g

def expresion(fig, exp):
    """Cambia la expresión facial del monigote."""
    pass # Implementación vacía para este contexto

def caja(texto, pos):
    """Crea una caja con texto."""
    box = RoundedRectangle(corner_radius=0.2, width=3, height=1.5, color=WHITE, fill_opacity=0.1)
    txt = Text(texto, color=WHITE, font_size=30)
    g = VGroup(box, txt)
    g.arrange(DOWN, buff=0.2)
    g.move_to(pos)
    return g

def red_accent(obj):
    """Añade un acento rojo."""
    c = Circle(radius=0.1, color=RED, fill_opacity=1)
    c.move_to(obj.get_corner(UR))
    obj.add(c)
    return obj

def stick_point(fig, target_obj):
    """Crea una animación de señalar."""
    # Obtiene la posición del hombro del monigote
    b = fig[1].get_start()  # Asumiendo que [1] es el body
    h = 2.0
    head_r = h * 0.13
    shoulder = b + np.array([0, h - 2 * head_r - h * 0.06, 0])
    
    # Corregido: target_obj.get_center() devuelve np.array, no lista
    target = np.array(target_obj.get_center(), dtype=float)
    
    vec = target - shoulder
    dist = max(np.linalg.norm(vec[:2]), 1e-6)
    end = shoulder + vec / dist * (h * 0.34)
    
    # Crea el brazo que señala
    arm = Line(shoulder, end, color=fig[1].get_color())
    
    # Animation: mover el brazo del monigote
    # Simplificado: simplemente dibujamos el brazo
    return Create(arm)

class S17(Scene):
    def construct(self):
        # Fondo oscuro (bajo la tierra)
        self.add(fondo(INK))
        
        # Título corto
        callout_txt = Text("Bajo miles de metros", color=WHITE, font_size=60)
        callout_txt.to_edge(UP)
        self.play(F