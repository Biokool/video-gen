from manim import *
from zenn_rig import *

class S08(Scene):
    def construct(self):
        # VOZ: La materia ordinaria, o bariónica, no es suficiente para explicar cómo se formaron estas estructuras tan pronto después del Big Bang.
        
        # VISUAL: callout
        # Create the callout mobject. The `callout` function from zenn_rig.py
        # is assumed to return a Mobject that can be animated.
        callout_mobject = callout("Materia Ordinaria\nNO SUFICIENTE", color=RED)
        
        # Play the animation to make the callout appear
        self.play(FadeIn(callout_mobject))
        
        # Wait for the narration. Total scene duration targeted at ~8 seconds.
        # (1s FadeIn + 6s wait + 1s FadeOut = 8s)
        self.wait(6)
        
        # Play the animation to make the callout disappear
        self.play(FadeOut(callout_mobject))