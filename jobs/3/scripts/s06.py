from manim import *
from zenn_rig import *

class S06(Scene):
    def construct(self):
        # VOZ: Pero en 1970, Vera Rubin observó algo que no encajaba.
        # VISUAL: clock_montage
        # El error "AttributeError: 'tuple' object has no attribute 'shift'"
        # indica que 'clock_montage' devuelve una tupla de Mobjects, no un solo Mobject (como un VGroup).
        # Para aplicar .shift(), necesitamos agrupar los Mobjects de la tupla en un VGroup.
        clock_obj = VGroup(*clock_montage(radius=1.8)).shift(UP*0.5)
        self.play(Create(clock_obj))
        self.wait(1)

        c1970 = callout("1970", color=YELLOW).to_edge(UP)
        self.play(FadeOut(clock_obj), FadeIn(c1970))
        self.wait(1)

        vera = stick_idle(pos=LEFT*4, height=2.2)
        self.play(FadeOut(c1970), Create(vera))
        self.wait(1)

        # VOZ: Midó la velocidad de las estrellas en las galaxias y descubrió que las del borde giraban tan rápido como las del centro.
        # Create a simple galaxy representation
        galaxy_center = Dot(ORIGIN, color=WHITE, radius=0.1)
        galaxy_disk = Circle(radius=1.5, color=TEAL, fill_opacity=0.2)
        star_inner = Dot(0.5*RIGHT, color=YELLOW)
        star_outer = Dot(1.5*RIGHT, color=YELLOW)
        
        galaxy = VGroup(galaxy_center, galaxy_disk, star_inner, star_outer).shift(RIGHT*2)
        
        self.play(Create(galaxy))
        self.play(stick_point(vera, galaxy_disk))
        self.wait(1.5)

        # VOZ: La curva de rotación era plana, no descendente.
        # Represent speeds with arrows of equal length
        arrow_inner = Arrow(star_inner.get_center(), star_inner.get_center() + UP*0.5, color=RED, buff=0)
        arrow_outer = Arrow(star_outer.get_center(), star_outer.get_center() + UP*0.5, color=RED, buff=0)
        
        self.play(Create(arrow_inner), Create(arrow_outer))
        self.wait(1.5)

        flat_curve_text = callout("Velocidad Constante", color=ORANGE, font_size=72).to_edge(DOWN)
        self.play(FadeIn(flat_curve_text))
        self.wait(2.5) # Increased wait for narration
        self.play(FadeOut(flat_curve_text), FadeOut(arrow_inner), FadeOut(arrow_outer))

        # VOZ: Para que esto funcione, debe haber mucha más masa en la galaxia de la que podemos ver.
        # Esa masa adicional forma un halo invisible que abarca toda la galaxia y más allá.
        # Represent the invisible halo
        halo = Circle(radius=3.0, color=INK, fill_opacity=0.1, stroke_opacity=0.5).move_to(galaxy.get_center())
        self.play(Create(halo))

        dark_matter_text = callout("Halo Invisible", color=YELLOW, font_size=72).to_edge(UP)
        self.play(FadeIn(dark_matter_text))
        self.wait(3.5) # Increased wait for narration
        self.play(FadeOut(dark_matter_text))

        # Clean up
        self.play(FadeOut(vera), FadeOut(galaxy), FadeOut(halo))
        self.wait(0.5)