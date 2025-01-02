import random
import time
import cv2
import numpy as np
from config import THEMES, APP_INFO

class FNAFAnimations:
    def __init__(self):
        self.animation_frame = 0
        self.animation_running = True
        self.last_static_update = 0
        self.static_overlay = None
        self.static_update_interval = 1.0 / 30  # 30 FPS for static
        
    def generate_static_overlay(self, frame_shape):
        """Generate static noise overlay similar to camera3"""
        current_time = time.time()
        
        if current_time - self.last_static_update > self.static_update_interval:
            # Use camera3's static implementation
            self.static_overlay = np.random.randint(50, 150, frame_shape[:2], dtype='uint8')
            self.last_static_update = current_time
            
        return self.static_overlay
        
    def animate_title(self, widget, theme):
        """Animate title with FNAF-style glitch effect"""
        if not self.animation_running:
            return
            
        if random.random() < 0.1:  # 10% chance to glitch
            effects = [
                lambda: widget.configure(text_color=random.choice(['#ff0000', '#00ff00', '#0000ff'])),  # RGB
                lambda: widget.configure(text_color='#ffffff'),  # White flash
                lambda: widget.configure(text_color='#000000'),  # Black out
                lambda: widget.place(x=widget.winfo_x() + random.randint(-2, 2)),  # Shake
                lambda: widget.configure(text=widget.cget('text').upper()),  # Uppercase
                lambda: widget.configure(text="".join([c if random.random() > 0.3 else random.choice("@#$%&") for c in widget.cget('text')])),  # Corrupt
                lambda: widget.configure(text=widget.cget('text').lower())   # Lowercase
            ]
            
            effect = random.choice(effects)
            effect()
            
            # Reset after brief delay
            widget.after(50, lambda: widget.configure(
                text_color=THEMES[theme]["title"],
                text=APP_INFO["title"]
            ))
        
        # Continue animation more frequently
        widget.after(30, lambda: self.animate_title(widget, theme))
        
    def stop_animations(self):
        """Stop all animations"""
        self.animation_running = False 