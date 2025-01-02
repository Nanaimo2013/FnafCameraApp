from gui import ModernFNAFGui
from camera import CameraManager
from effects import FNAFEffects
from animations import FNAFAnimations
import tkinter as tk
import os

def main():
    # Create required directories
    os.makedirs("config", exist_ok=True)
    
    root = tk.Tk()
    root.configure(bg="#1a1a1a")
    
    # Initialize managers
    animations = FNAFAnimations()
    camera = CameraManager()
    effects = FNAFEffects(animations)
    
    # Create GUI with all managers
    app = ModernFNAFGui(root, camera, effects, animations)
    
    # Configure window
    root.geometry("1280x720")
    root.minsize(800, 600)
    
    root.mainloop()

if __name__ == "__main__":
    main()