from zenn_rig import *

class S13(Scene):
    def construct(self):
        rig = Rig(self)
        
        # Fondo espacial oscuro
        fondo_rect = Rectangle(
            width=14.22, 
            height=8, 
            color=BLACK, 
            fill_opacity=1
        )
        self.add(fondo_rect)
        self.wait(0.5)
        
        # Estrellas de fondo
        stars = VGroup()
        for _ in range(15):
            dot = Dot(
                point=random.uniform(-7, 7) * RIGHT + random.uniform(-4, 4) * UP,
                radius=0.02,
                color=WHITE,
                opacity=0.8
            )
            stars.add(dot)
        self.play(FadeIn(stars, run_time=1.0))
        
        # Monigote con expresión de sorpresa usando rig
        fig = rig.get_character("stick_idle")
        fig.move_to(LEFT * 5)
        self.play(FadeIn(fig, run_time=0.8))
        
        # Galaxia lejana usando rig
        galaxia = rig.get_prop("galaxy")
        galaxia.move_to(RIGHT * 5 + UP * 1)
        self.play(FadeIn(galaxia, run_time=1.0))
        
        # Objeto masivo usando rig
        objeto_masivo = rig.get_prop("sun")
        objeto_masivo.move_to(ORIGIN)
        self.play(FadeIn(objeto_masivo, run_time=1.0))
        
        # Trayectoria recta de la luz
        trayectoria_recta = Line(
            RIGHT * 5 + UP * 1,
            LEFT * 5 + UP * 1,
            color=WHITE,
            stroke_width=2
        )
        self.play(Create(trayectoria_recta, run_time=1.2))
        
        # Flecha que muestra la curvatura
        flecha_curvatura = Arrow(
            RIGHT * 5 + UP * 1,
            LEFT * 5 + UP * 1,
            color=ORANGE,
            buff=0.2
        )
        self.play(FadeIn(flecha_curvatura, run_time=1.5))
        
        # Callout con el concepto
        callout_text = Text("Gravedad curva el espacio", color=TEAL, font_size=36)
        callout_box = SurroundingRectangle(callout_text, color=TEAL, buff=0.2)
        callout_obj = VGroup(callout_box, callout_text)
        callout_obj.to_edge(UP)
        self.play(FadeIn(callout_obj, run_time=1.0))
        
        self.wait(1.5)
        
        # Transformación: la luz se dobla
        # Crear una curva arc que simule la desviación
        trayectoria_curva = Arc(
            start_angle=0,
            angle=PI / 4,
            radius=3,
            color=WHITE,
            stroke_width=2
        )
        # Mover la curva para que empiece aproximadamente donde empieza la recta
        trayectoria_curva.move_to(RIGHT * 2 + UP * 1)
        
        self.play(
            Transform(trayectoria_recta, trayectoria_curva, run_time=1.5),
            FadeOut(flecha_curvatura, run_time=1.5)
        )
        
        self.wait(1.0)
        
        # Limpiar pantalla
        self.play(
            *[FadeOut(m, run_time=1.0) for m in self.mobjects]
        )