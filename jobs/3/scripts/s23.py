from zenn_rig import *

class S23(Scene):
    def construct(self):
        self.background_color = "#0a0a0a"
        
        estrellas = VGroup(*[
            Dot(radius=0.02, color=WHITE).move_to([random.uniform(-6, 6), random.uniform(-4, 4), 0])
            for _ in range(30)
        ])
        self.add(estrellas)
        self.play(FadeIn(estrellas), run_time=2.0)

        # Usar el rig para el monigote
        monigote = self.rig.get_monic("stickman")
        monigote.scale(1.5).move_to(ORIGIN)
        self.play(FadeIn(monigote), run_time=1.0)

        # Red de seguridad
        red = Grid(
            x_lines=5, y_lines=5,
            height=3, width=3,
            color=BLUE, stroke_width=1,
            buff=0
        ).move_to([0, 0.5, 0])
        
        self.play(Create(red), run_time=2.0)

        # Callout
        callout_obj = Text("Invisible", color=YELLOW, font_size=48)
        callout_obj.to_edge(UP, buff=0.5)
        self.play(FadeIn(callout_obj), run_time=1.0)

        self.wait(1.0)

        self.play(FadeOut(callout_obj), run_time=0.5)
        self.wait(0.5)