from manim import *
from zenn_rig import *

class S04(Scene):
    def construct(self):
        # Protagonista: naranja, inicialmente de pie y pensando
        prota = protagonista(pos=LEFT * 3.5, playera=PLAYERA_NARANJA, expresion='pensando', pose='de_pie')
        self.play(FadeIn(prota))
        self.wait(0.5) # Pausa inicial para la narración

        # Cerebro transparente: contorno y relleno semitransparente
        brain_outline = Circle(radius=1.8, color=INK, stroke_width=4).shift(RIGHT * 2.5)
        brain_fill = Circle(radius=1.8, color=INK, fill_opacity=0.15).shift(RIGHT * 2.5)
        
        # Piloto diminuto (stick_idle) dentro del cerebro
        pilot = stick_idle(height=0.8, color=INK).move_to(RIGHT * 2.5 + DOWN * 0.3)
        
        # Sillón de mando: un simple rectángulo
        chair = Rectangle(width=0.8, height=0.6, color=INK, fill_opacity=0.8).move_to(pilot.get_bottom() + DOWN * 0.3)
        
        # Agrupar los elementos internos y el cerebro
        internal_elements = VGroup(chair, pilot)
        brain_group = VGroup(brain_fill, brain_outline, internal_elements)

        # Animación de aparición del cerebro y su contenido
        self.play(
            Create(brain_outline),
            FadeIn(brain_fill),
            FadeIn(internal_elements),
            run_time=1.5
        )
        self.wait(0.5)

        # El protagonista cambia a expresión normal y señala el cerebro
        # El rig no expone `change_pose` o `change_expresion` como métodos directos
        # para animar con `.animate`. Para cambiar la pose y expresión,
        # se debe crear un nuevo objeto `protagonista` con los parámetros deseados
        # y luego usar `Transform` para animar el cambio.
        new_prota = protagonista(
            pos=prota.get_center(), # Mantiene la posición actual del protagonista
            playera=PLAYERA_NARANJA,
            expresion='normal', # Nueva expresión
            pose='senalando'    # Nueva pose
        )
        
        self.play(Transform(prota, new_prota), run_time=1)
        # Es buena práctica actualizar la referencia 'prota' al nuevo objeto
        prota = new_prota
        self.wait(0.5)

        # Callout con el texto clave
        callout_text = callout("PILOTO EN LA CABINA").next_to(brain_outline, UP, buff=0.5)
        self.play(FadeIn(callout_text))

        self.wait(2) # Espera final para la narración

        # Desvanecer todos los elementos al final de la escena
        self.play(FadeOut(VGroup(prota, brain_group, callout_text)))