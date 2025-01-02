import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from config import THEMES, FONTS_DIR, FRAMES_DIR, DEFAULT_SETTINGS, APP_INFO, STATIC_DIR
import cv2
from threading import Thread
import random
import yaml
import time
import numpy as np

class ModernFNAFGui:
    def __init__(self, root, camera_manager=None, effects_manager=None, animations=None):
        self.root = root
        self.root.title(APP_INFO["title"])
        
        # Initialize dictionaries
        self.effect_labels = {}
        self.toggles = {}
        self.sliders = {}
        self.labels = {}
        
        # Set managers
        self.camera_manager = camera_manager
        self.effects_manager = effects_manager
        self.animations = animations
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        
        # Initialize GUI
        self.load_tips()
        self.setup_theme()
        self.load_custom_fonts()
        self.create_widgets()
        self.setup_animations()

    def setup_theme(self):
        """Initialize custom theme and styling"""
        self.current_theme = "dark"
        self.apply_theme()
        
        # Configure custom styles
        style = ttk.Style()
        style.configure("FNAF.TButton", 
                       padding=10, 
                       font=("FNAFFont", 12))

    def apply_theme(self):
        """Apply the current theme to all widgets"""
        theme = THEMES[self.current_theme]
        
        # Configure root window
        self.root.configure(bg=theme["bg"])
        
        # Configure CustomTkinter appearance mode
        ctk.set_appearance_mode("dark" if self.current_theme in ["dark", "midnight"] else "light")
        
        # Update all frames
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(
                    fg_color=theme["bg"],
                    border_color=theme["border"]
                )
        
        # Update buttons
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(
                    fg_color=theme["button"],
                    hover_color=theme["hover"],
                    text_color=theme["fg"],
                    border_color=theme["border"]
                )
        
        # Update switches
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkSwitch):
                widget.configure(
                    progress_color=theme["switch"],
                    button_color=theme["accent"],
                    button_hover_color=theme["hover"],
                    text_color=theme["fg"]
                )
        
        # Update sliders
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkSlider):
                widget.configure(
                    progress_color=theme["accent"],
                    button_color=theme["accent"],
                    button_hover_color=theme["hover"],
                    fg_color=theme["slider"]
                )
        
        # Update labels
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=theme["fg"])
        
        # Update specific elements
        if hasattr(self, 'version_label'):
            self.version_label.configure(text_color=theme["title"])
        if hasattr(self, 'author_label'):
            self.author_label.configure(text_color=theme["subtitle"])
        if hasattr(self, 'theme_menu'):
            self.theme_menu.configure(
                fg_color=theme["dropdown"],
                button_color=theme["accent"],
                button_hover_color=theme["hover"],
                dropdown_fg_color=theme["dropdown"],
                dropdown_hover_color=theme["hover"],
                dropdown_text_color=theme["fg"],
                text_color=theme["fg"]
            )

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme()

    def load_custom_fonts(self):
        """Load custom FNAF fonts from fonts directory"""
        # ... font loading logic ...

    def create_widgets(self):
        """Create all GUI widgets"""
        # Create header
        self.create_header()
        
        # Create status bar
        self.create_status_bar()
        
        # Create camera controls
        self.create_camera_controls()
        
        # Create settings panel
        self.create_settings_panel()
        
        # Create preview area
        self.create_preview_area()
        
        # Initial camera refresh
        self.refresh_cameras()

    def create_toggle(self, parent, text, key):
        """Create a toggle switch with label"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=2)
        
        toggle = ctk.CTkSwitch(
            frame,
            text=text,
            command=lambda: self.apply_effect_changes(),
            onvalue=True,
            offvalue=False
        )
        toggle.pack(side="left", padx=10)
        
        # Set initial state from default settings
        if DEFAULT_SETTINGS.get(key, False):
            toggle.select()
        else:
            toggle.deselect()
        
        self.toggles[key] = toggle
        return toggle

    def create_settings_panel(self):
        """Create modern settings panel with sliders and toggles"""
        settings_frame = ctk.CTkFrame(self.main_frame)
        settings_frame.pack(fill="x", padx=20, pady=10)

        # Create two columns for effects
        left_column = ctk.CTkFrame(settings_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=5)
        
        right_column = ctk.CTkFrame(settings_frame)
        right_column.pack(side="left", fill="both", expand=True, padx=5)

        # Initialize storage for controls
        self.sliders = {}
        self.toggles = {}

        # Split effects between columns
        left_effects = [
            ("Static Effect", "static"),
            ("Glitch Effect", "glitch"),
            ("Screen Tear", "tear"),
            ("VHS Effect", "vhs"),
            ("Noise Effect", "noise")
        ]

        right_effects = [
            ("Color Distortion", "color_distortion"),
            ("Chromatic Aberration", "chromatic"),
            ("VHS Tracking", "tracking"),
            ("Digital Artifacts", "artifacts")
        ]

        # Create effect groups in left column
        for title, key in left_effects:
            self.create_effect_group(left_column, title, key)

        # Create effect groups in right column
        for title, key in right_effects:
            self.create_effect_group(right_column, title, key)

    def create_effect_group(self, parent, title, key):
        """Create effect group with toggle and sliders"""
        group = ctk.CTkFrame(parent)
        group.pack(fill="x", pady=5, padx=5)
        
        # Header with toggle
        header = ctk.CTkFrame(group)
        header.pack(fill="x", padx=5, pady=2)
        
        toggle = ctk.CTkSwitch(
            header,
            text=title,
            command=lambda: self.toggle_effect(key)
        )
        toggle.pack(side="left", padx=5)
        self.toggles[key] = toggle
        
        # Controls frame
        controls = ctk.CTkFrame(group)
        controls.pack(fill="x", padx=5, pady=2)
        
        # Intensity slider
        intensity_frame = ctk.CTkFrame(controls)
        intensity_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(intensity_frame, text="Intensity:").pack(side="left", padx=2)
        intensity = ctk.CTkSlider(
            intensity_frame,
            from_=0,
            to=100,
            number_of_steps=100
        )
        intensity.pack(side="left", expand=True, padx=5)
        self.sliders[f"{key}_intensity"] = intensity
        
        # Intensity percentage label
        percent_label = ctk.CTkLabel(intensity_frame, text="0%")
        percent_label.pack(side="left", padx=2)
        
        # Speed slider
        speed_frame = ctk.CTkFrame(controls)
        speed_frame.pack(side="right", padx=5)
        
        ctk.CTkLabel(speed_frame, text="Speed:").pack(side="left")
        speed = ctk.CTkSlider(
            speed_frame,
            from_=0,
            to=200,
            number_of_steps=200,
            width=100
        )
        speed.pack(side="left", padx=5)
        self.sliders[f"{key}_speed"] = speed
        
        # Speed multiplier label
        speed_label = ctk.CTkLabel(speed_frame, text="1.0x")
        speed_label.pack(side="left", padx=2)
        
        # Configure slider commands
        intensity.configure(command=lambda v: self.update_effect_intensity(key, v/100, percent_label))
        speed.configure(command=lambda v: self.update_effect_speed(key, v/100, speed_label))
        
        # Set initial values from config
        intensity.set(DEFAULT_SETTINGS[f"{key}_intensity"] * 100)
        speed.set(DEFAULT_SETTINGS[f"{key}_speed"] * 100)
        if DEFAULT_SETTINGS[f"{key}_enabled"]:
            toggle.select()
        else:
            toggle.deselect()
        
        # Add extra controls for glitch effect
        if key == "glitch":
            # Duration controls
            duration_frame = ctk.CTkFrame(controls)
            duration_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(duration_frame, text="Frame Duration:").pack(side="left", padx=2)
            duration_label = ctk.CTkLabel(duration_frame, text=f"{DEFAULT_SETTINGS['glitch_duration']:.1f}s", width=40)
            duration_label.pack(side="right", padx=2)
            
            duration = ctk.CTkSlider(
                duration_frame,
                from_=0.1,
                to=10.0,
                number_of_steps=99
            )
            duration.set(DEFAULT_SETTINGS["glitch_duration"])
            duration.pack(side="right", expand=True, padx=5)
            self.sliders["glitch_duration"] = duration
            
            # Configure duration slider command
            duration.configure(
                command=lambda v: self.update_glitch_duration(v, duration_label)
            )
            
            # Frequency slider - default to 3s like camera3
            freq_frame = ctk.CTkFrame(controls)
            freq_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(freq_frame, text="Frequency:").pack(side="left", padx=2)
            frequency = ctk.CTkSlider(
                freq_frame,
                from_=2.0,
                to=10.0,
                number_of_steps=100
            )
            frequency.set(3.0)  # Default to 3s like camera3
            frequency.pack(side="left", expand=True, padx=5)
            self.sliders[f"{key}_frequency"] = frequency
            
            # Burst chance slider - higher default
            burst_frame = ctk.CTkFrame(controls)
            burst_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(burst_frame, text="Burst Chance:").pack(side="left", padx=2)
            burst = ctk.CTkSlider(
                burst_frame,
                from_=0,
                to=100,
                number_of_steps=100
            )
            burst.set(40)  # 40% default chance like camera3
            burst.pack(side="left", expand=True, padx=5)
            self.sliders[f"{key}_burst"] = burst
            
            # Set initial values
            duration.set(DEFAULT_SETTINGS["glitch_duration"] * 100)
            frequency.set(DEFAULT_SETTINGS["glitch_frequency"] * 10)
            burst.set(DEFAULT_SETTINGS["glitch_burst_chance"] * 100)

    def create_effect_slider(self, parent, label_text, key, min_val, max_val, default):
        """Create a compact slider with percentage display"""
        slider_frame = ctk.CTkFrame(parent)
        slider_frame.pack(fill="x", pady=1)
        
        # Percentage label
        percentage_label = ctk.CTkLabel(slider_frame, text=f"{default}%", width=30)
        percentage_label.pack(side="right", padx=2)
        
        # Slider
        slider = ctk.CTkSlider(
            slider_frame,
            from_=min_val,
            to=max_val,
            number_of_steps=100,
            command=lambda value: self.update_slider_percentage(key, value, percentage_label)
        )
        slider.pack(side="left", fill="x", expand=True, padx=2)
        slider.set(default)
        
        self.sliders[key] = {"slider": slider, "label": percentage_label}
        return slider  # Return the slider widget

    def create_effects_toggles(self, parent):
        """Create toggle buttons for optional effects"""
        ctk.CTkLabel(parent, text="Optional Effects", 
                     font=("Arial", 12, "bold")).pack(pady=5)
        
        self.effect_toggles = {}
        effects = [
            ("Chromatic Aberration", "chromatic"),
            ("VHS Tracking", "tracking"),
            ("Random Glitches", "random_glitch"),
            ("Color Corruption", "color_corrupt"),
            ("Static Bursts", "static_burst"),
            ("Digital Artifacts", "artifacts")
        ]
        
        for text, key in effects:
            toggle = ctk.CTkSwitch(parent, text=text)
            toggle.pack(pady=2, padx=10, anchor="w")
            self.effect_toggles[key] = toggle

    def create_control_buttons(self, parent):
        """Create control buttons"""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", pady=10)
        
        # Left side buttons
        left_buttons = ctk.CTkFrame(button_frame)
        left_buttons.pack(side="left", padx=5)
        
        ctk.CTkButton(
            left_buttons,
            text="↻ Reload Effects",
            command=self.reload_effects,
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            left_buttons,
            text="Reset to Default",
            command=self.reset_settings,
            width=120
        ).pack(side="left", padx=5)
        
        # Right side buttons
        right_buttons = ctk.CTkFrame(button_frame)
        right_buttons.pack(side="right", padx=5)
        
        ctk.CTkButton(
            right_buttons,
            text="Save Preset",
            command=self.save_preset,
            width=120
        ).pack(side="right", padx=5)

    def update_slider_percentage(self, key, value, label):
        """Update percentage label for slider"""
        label.configure(text=f"{int(value)}%")
        self.apply_effect_changes()

    def apply_effect_changes(self):
        """Apply current effect settings"""
        if hasattr(self, 'effects_manager'):
            settings = self.get_current_settings()
            
            # Update all effect settings
            for key, value in settings.items():
                if "_intensity" in key:
                    effect_name = key.replace("_intensity", "")
                    self.effects_manager.set_effect_intensity(effect_name, value)
                elif "_speed" in key:
                    effect_name = key.replace("_speed", "")
                    self.effects_manager.set_effect_speed(effect_name, value)
                elif "_enabled" in key:
                    effect_name = key.replace("_enabled", "")
                    self.effects_manager.toggle_effect(effect_name, value)

    def get_current_settings(self):
        """Get current effect settings"""
        settings = {}
        
        # Get toggle states
        for key, toggle in self.toggles.items():
            if "_enabled" in key:
                settings[key] = toggle.get()
        
        # Get slider values
        for key, slider in self.sliders.items():
            if "_intensity" in key:
                # Direct access to slider value instead of using ["widget"]
                settings[key] = slider.get() / 100.0
            elif "_speed" in key:
                settings[key] = slider.get() / 100.0
            
        return settings

    def reload_effects(self):
        """Reload all effects and frames"""
        try:
            if hasattr(self, 'effects_manager'):
                self.effects_manager.reload_frames()
                self.effects_manager.reload_extra_images()
            self.update_status("Effects reloaded successfully")
        except Exception as e:
            self.update_status(f"Error reloading effects: {str(e)}")

    def reset_settings(self):
        """Reset all settings to default"""
        for key, default in DEFAULT_SETTINGS.items():
            if key in self.sliders:
                self.sliders[key]["slider"].set(default * 100)
                self.sliders[key]["label"].configure(text=f"{int(default * 100)}%")
        
        # Reset toggles
        for toggle in self.effect_toggles.values():
            toggle.deselect()
        
        self.apply_effect_changes()
        self.update_status("Settings reset to default")

    def save_preset(self):
        """Save current settings as a preset"""
        # Implementation for saving presets
        settings = self.get_current_settings()
        # TODO: Add preset saving functionality
        self.update_status("Preset saved")

    def create_camera_controls(self):
        """Create camera control panel"""
        control_frame = ctk.CTkFrame(self.main_frame)
        control_frame.pack(fill="x", padx=20, pady=5)
        
        # Single row for all controls
        combo_frame = ctk.CTkFrame(control_frame)
        combo_frame.pack(fill="x", pady=2)
        
        # Left side: Camera dropdown and refresh
        self.camera_combo = ctk.CTkOptionMenu(
            combo_frame,
            values=["No cameras detected"],
            width=200,
            command=self.on_camera_select
        )
        self.camera_combo.pack(side="left", padx=5)
        
        self.refresh_btn = ctk.CTkButton(
            combo_frame,
            text="↻ Refresh",
            width=100,
            command=self.refresh_cameras
        )
        self.refresh_btn.pack(side="left", padx=5)
        
        # Center: FPS control
        fps_label = ctk.CTkLabel(combo_frame, text="FPS:")
        fps_label.pack(side="left", padx=(10, 0))
        
        fps_spinbox = ctk.CTkEntry(
            combo_frame,
            width=50,
            placeholder_text="30"
        )
        fps_spinbox.pack(side="left", padx=5)
        fps_spinbox.insert(0, "30")
        fps_spinbox.bind('<Return>', lambda e: self.camera_manager.set_fps(int(fps_spinbox.get())))
        
        # Center-right: Control buttons
        self.start_btn = ctk.CTkButton(
            combo_frame,
            text="▶ Start",
            command=self.start_camera
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ctk.CTkButton(
            combo_frame,
            text="◼ Stop",
            state="disabled",
            command=self.stop_camera
        )
        self.stop_btn.pack(side="left", padx=5)
        
        self.capture_btn = ctk.CTkButton(
            combo_frame,
            text="📸 Capture",
            command=self.capture_frame
        )
        self.capture_btn.pack(side="left", padx=5)
        
        # Right side: Virtual output and reload effects
        self.virtual_toggle = ctk.CTkSwitch(
            combo_frame,
            text="Virtual Output",
            command=self.toggle_virtual_camera
        )
        self.virtual_toggle.pack(side="right", padx=5)
        self.virtual_toggle.select()
        
        self.reload_btn = ctk.CTkButton(
            combo_frame,
            text="↻ Reload Effects",
            command=self.reload_effects
        )
        self.reload_btn.pack(side="right", padx=5)

    def create_tooltip(self, widget, text):
        """Create a cursor-following tooltip for a widget"""
        def update_tooltip_position(event=None):
            if hasattr(widget, 'tooltip'):
                x = widget.winfo_pointerx() + 15
                y = widget.winfo_pointery() + 10
                widget.tooltip.place(x=x, y=y)

        def show_tooltip(event):
            tooltip = ctk.CTkLabel(
                self.root,
                text=text,
                fg_color=THEMES[self.current_theme]["dropdown"],
                text_color=THEMES[self.current_theme]["fg"],
                corner_radius=6,
                padx=10,
                pady=5
            )
            widget.tooltip = tooltip
            update_tooltip_position()
            
            # Bind motion to update tooltip position
            widget.bind('<Motion>', update_tooltip_position)

        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.unbind('<Motion>')
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def update_preview(self, frame):
        """Update preview with frame"""
        if frame is None or not hasattr(self, 'preview_label'):
            return
        
        try:
            # Convert frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get current preview dimensions
            width = self.preview_label.winfo_width()
            height = self.preview_label.winfo_height()
            
            if width > 1 and height > 1:  # Ensure valid dimensions
                # Calculate aspect ratio preserving resize
                aspect_ratio = frame_rgb.shape[1] / frame_rgb.shape[0]
                
                if width / height > aspect_ratio:
                    new_width = int(height * aspect_ratio)
                    new_height = height
                else:
                    new_width = width
                    new_height = int(width / aspect_ratio)
                
                # Resize frame
                frame_resized = cv2.resize(frame_rgb, (new_width, new_height))
                
                # Convert to PIL Image first
                pil_image = Image.fromarray(frame_resized)
                
                # Convert to CTkImage
                ctk_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(new_width, new_height)
                )
                
                # Update preview
                self.preview_label.configure(image=ctk_image)
                self.preview_label.image = ctk_image  # Keep reference
                
        except Exception as e:
            print(f"Preview error: {str(e)}")

    def create_header(self):
        """Create animated header with FNAF styling"""
        theme = THEMES[self.current_theme]
        
        header_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color=theme["header"],
            corner_radius=0
        )
        header_frame.pack(fill="x")  # Removed pady

        # Title and version info
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(side="left", padx=20, pady=5)  # Reduced pady
        
        title_label = ctk.CTkLabel(
            info_frame,
            text=APP_INFO["title"],
            font=("Arial", 24, "bold"),  # Slightly smaller font
            text_color=theme["title"]
        )
        title_label.pack()

        # Theme selector with theme-specific styling
        theme_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        theme_frame.pack(side="left", padx=20, pady=10)
        
        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["🌙 Dark", "☀️ Light", "🌌 Midnight"],
            command=self.change_theme,
            width=150,
            fg_color=theme["dropdown"],
            button_color=theme["accent"],
            button_hover_color=theme["hover"],
            dropdown_fg_color=theme["dropdown"],
            dropdown_hover_color=theme["hover"],
            dropdown_text_color=theme["fg"],
            text_color=theme["fg"]
        )
        self.theme_menu.pack()

        # App info with theme-specific styling
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(side="right", padx=20, pady=10)
        
        self.version_label = ctk.CTkLabel(
            info_frame,
            text=f"Version: {APP_INFO['version']}",
            font=("Arial", 16, "bold"),
            text_color=theme["title"]
        )
        self.version_label.pack()
        
        self.author_label = ctk.CTkLabel(
            info_frame,
            text=f"by {APP_INFO['author']}",
            font=("Arial", 14),
            text_color=theme["subtitle"]
        )
        self.author_label.pack()

    def update_status(self, message):
        """Update status message"""
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)

    def set_camera_manager(self, camera_manager):
        """Set the camera manager instance"""
        self.camera_manager = camera_manager

    def refresh_cameras(self):
        """Refresh available cameras list"""
        try:
            cameras = self.camera_manager.get_available_cameras()
            camera_list = [f"Camera {index}" for index, name in cameras]
            
            if not camera_list:
                camera_list = ["No cameras detected"]
                
            self.camera_combo.configure(values=camera_list)
            self.camera_combo.set(camera_list[0])
            
            self.update_status(
                "Cameras refreshed" if camera_list[0] != "No cameras detected" 
                else "No cameras detected"
            )
        except Exception as e:
            print(f"Camera refresh error: {str(e)}")
            self.update_status("Error refreshing cameras")

    def start_camera(self):
        """Start selected camera"""
        if hasattr(self, 'camera_manager'):
            try:
                # Get selected camera index from combo box
                selection = self.camera_combo.get()
                camera_index = int(selection.split()[1])  # Extract number from "Camera X"
                
                # Set preview callback
                self.camera_manager.set_preview_callback(self.update_preview)
                
                # Start camera
                if self.camera_manager.start_camera(camera_index):
                    # Start processing thread
                    self.process_thread = Thread(
                        target=self.process_camera_feed,
                        daemon=True
                    )
                    self.process_thread.start()
                    
                    self.update_status("Camera started")
                    self.stop_btn.configure(state="normal")
                    self.start_btn.configure(state="disabled")
                    
            except Exception as e:
                self.update_status(f"Error starting camera: {str(e)}")

    def stop_camera(self):
        """Stop the current camera"""
        try:
            if hasattr(self, 'camera_manager'):
                self.camera_manager.stop_camera()
                self.update_status(self.tips["status"]["camera_stop"])
                self.stop_btn.configure(state="disabled")
                self.start_btn.configure(state="normal")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")

    def capture_frame(self):
        """Capture and save the current frame"""
        try:
            filename = self.camera_manager.capture_frame(FRAMES_DIR)
            self.update_status(f"Frame saved as {filename}")
        except Exception as e:
            self.update_status(f"Capture error: {str(e)}")

    def process_camera_feed(self):
        """Process camera feed and update preview"""
        try:
            if hasattr(self, 'camera_manager') and self.camera_manager.running:
                for frame in self.camera_manager.process_video(
                    self.effects_manager, 
                    self.get_current_settings()
                ):
                    if frame is not None:
                        self.update_preview(frame)
                    if not self.camera_manager.running:
                        break
        except Exception as e:
            print(f"Preview error: {str(e)}")
            self.update_status(f"Error: {str(e)}")

    def create_preview_area(self):
        """Create the camera preview area"""
        preview_frame = ctk.CTkFrame(self.main_frame)
        preview_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Create preview label with dark background
        self.preview_label = ctk.CTkLabel(
            preview_frame,
            text="Camera Preview",
            font=("Arial", 14),
            width=640,
            height=480
        )
        self.preview_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Add info text below preview
        info_text = ctk.CTkLabel(
            preview_frame,
            text="Preview will appear when camera is started",
            font=("Arial", 10),
            text_color=THEMES[self.current_theme]["fg"]
        )
        info_text.pack(pady=(0, 10))

    def setup_animations(self):
        """Setup animations for GUI elements"""
        self.animation_frame = 0
        self.animation_running = True
        
        def animate_title():
            """Animate the title with a glitch effect"""
            if hasattr(self, 'status_label') and self.animation_running:
                # Glitch colors for title
                colors = ['#ff0000', '#800000', '#ffffff']
                
                if random.random() < 0.1:  # 10% chance to change color
                    title_color = random.choice(colors)
                    self.status_label.configure(text_color=title_color)
                
                # Reset to theme color after brief delay
                self.root.after(100, lambda: self.status_label.configure(
                    text_color=THEMES[self.current_theme]["accent"]
                ))
                
                # Continue animation
                self.root.after(50, animate_title)
        
        # Start animation loop
        animate_title()

        def cleanup():
            """Stop animations when window closes"""
            self.animation_running = False
            self.root.destroy()
        
        # Bind cleanup to window close
        self.root.protocol("WM_DELETE_WINDOW", cleanup)

    def set_effects_manager(self, effects_manager):
        """Set the effects manager instance"""
        self.effects_manager = effects_manager

    def load_tips(self):
        """Load tooltips from YAML file"""
        try:
            # Create config directory if it doesn't exist
            os.makedirs("config", exist_ok=True)
            
            # Create default tips if file doesn't exist
            if not os.path.exists('config/tips.yml'):
                self.create_default_tips()
            
            # Load tips from file
            with open('config/tips.yml', 'r') as file:
                self.tips = yaml.safe_load(file) or self.create_default_tips()
                
        except Exception as e:
            print(f"Error loading tips: {str(e)}")
            self.tips = self.create_default_tips()

    def create_default_tips(self):
        """Create default tips dictionary and save to file"""
        default_tips = {
            "camera_controls": {
                "start_camera": "Start capturing video from the selected camera",
                "stop_camera": "Stop the current camera feed",
                "capture_frame": "Take a snapshot of the current frame",
                "refresh_cameras": "Refresh the list of available cameras",
                "camera_select": "Select which camera to use"
            },
            "effects": {
                key: {
                    "toggle": f"Enable/disable {key.replace('_', ' ')} effect",
                    "slider": f"Adjust the {key.replace('_', ' ')} intensity"
                } for key in ["static", "glitch", "tear", "vhs", "noise", 
                            "color_distortion", "chromatic", "tracking", "artifacts"]
            },
            "status": {
                "camera_start": "Starting camera feed...",
                "camera_stop": "Camera stopped",
                "capture_success": "Frame captured successfully",
                "no_cameras": "No cameras detected",
                "error": "An error occurred"
            }
        }
        
        try:
            with open('config/tips.yml', 'w') as file:
                yaml.dump(default_tips, file, default_flow_style=False)
        except Exception as e:
            print(f"Error saving default tips: {str(e)}")
        
        return default_tips

    def change_theme(self, theme_name):
        """Change the application theme"""
        try:
            # Convert theme menu selection to theme key
            theme_map = {
                "🌙 Dark": "dark",
                "☀️ Light": "light",
                "🌌 Midnight": "midnight"
            }
            
            self.current_theme = theme_map.get(theme_name, "dark")
            theme = THEMES[self.current_theme]
            
            # Update CustomTkinter appearance mode
            ctk.set_appearance_mode("dark" if self.current_theme in ["dark", "midnight"] else "light")
            
            # Update all widgets recursively
            def update_widget_theme(widget):
                if isinstance(widget, ctk.CTkFrame):
                    widget.configure(fg_color=theme["bg"])
                elif isinstance(widget, ctk.CTkLabel):
                    widget.configure(
                        fg_color="transparent",
                        text_color=theme["fg"]
                    )
                elif isinstance(widget, ctk.CTkButton):
                    widget.configure(
                        fg_color=theme["button"],
                        hover_color=theme["hover"],
                        text_color=theme["fg"]
                    )
                elif isinstance(widget, ctk.CTkSwitch):
                    widget.configure(
                        button_color=theme["switch"],
                        button_hover_color=theme["hover"],
                        progress_color=theme["accent"]
                    )
                elif isinstance(widget, ctk.CTkSlider):
                    widget.configure(
                        button_color=theme["accent"],
                        button_hover_color=theme["hover"],
                        progress_color=theme["slider"]
                    )
                
                # Recursively update child widgets
                for child in widget.winfo_children():
                    update_widget_theme(child)
            
            # Update root and all children
            self.root.configure(bg=theme["bg"])
            update_widget_theme(self.root)
            
            # Update specific widgets
            if hasattr(self, 'status_label'):
                self.status_label.configure(text_color=theme["accent"])
            if hasattr(self, 'title_label'):
                self.title_label.configure(text_color=theme["title"])
            
            # Save theme preference
            self.save_theme_preference()
            
        except Exception as e:
            print(f"Error changing theme: {str(e)}")

    def save_theme_preference(self):
        """Save current theme preference"""
        try:
            settings = DEFAULT_SETTINGS.copy()
            settings['theme'] = self.current_theme
            
            with open('config/settings.yml', 'w') as file:
                yaml.dump(settings, file, default_flow_style=False)
        except Exception as e:
            print(f"Error saving theme preference: {str(e)}")

    def load_theme_preference(self):
        """Load saved theme preference"""
        try:
            if os.path.exists('config/settings.yml'):
                with open('config/settings.yml', 'r') as file:
                    settings = yaml.safe_load(file)
                    if settings and 'theme' in settings:
                        self.current_theme = settings['theme']
                        
                        # Update theme menu
                        theme_map = {
                            "dark": "🌙 Dark",
                            "light": "☀️ Light",
                            "midnight": "🌌 Midnight"
                        }
                        if hasattr(self, 'theme_menu'):
                            self.theme_menu.set(theme_map.get(self.current_theme, "🌙 Dark"))
        except Exception as e:
            print(f"Error loading theme preference: {str(e)}")

    def update_effect_state(self, key):
        """Update effect controls based on toggle state"""
        enabled = self.toggles[f"{key}_enabled"].get()
        intensity_key = f"{key}_intensity"
        
        # Update slider state
        if intensity_key in self.sliders:
            slider = self.sliders[intensity_key]["widget"]
            slider.configure(
                state="normal" if enabled else "disabled",
                button_color=THEMES[self.current_theme]["accent"] if enabled else THEMES[self.current_theme]["slider"]
            )
        
        # Update label state
        if key in self.effect_labels:
            self.effect_labels[key].configure(
                text_color=THEMES[self.current_theme]["fg"] if enabled else THEMES[self.current_theme]["subtitle"]
            )
        
        self.apply_effect_changes()

    def on_camera_select(self, selection):
        """Handle camera selection"""
        try:
            # Extract camera index from selection
            camera_index = int(selection.split()[1])
            self.selected_camera = camera_index
            self.update_status(f"Selected camera {camera_index}")
        except Exception as e:
            print(f"Camera selection error: {str(e)}")

    def toggle_virtual_camera(self):
        """Toggle virtual camera output"""
        if hasattr(self, 'camera_manager'):
            self.camera_manager.virtual_camera_enabled = self.virtual_toggle.get()

    def create_status_bar(self):
        """Create status bar at bottom of window"""
        status_frame = ctk.CTkFrame(self.main_frame)
        status_frame.pack(fill="x", side="bottom", padx=20, pady=5)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            font=("Arial", 12)
        )
        self.status_label.pack(side="left", padx=10)

    def create_menu(self):
        """Create application menu bar"""
        # Add menu bar to root window
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # App menu (attached to window)
        app_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="App", menu=app_menu)
        app_menu.add_command(label="Settings", command=self.show_settings_window)
        app_menu.add_separator()
        app_menu.add_command(label="Exit", command=self.root.quit)

    def show_camera_settings(self):
        """Show camera settings window"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Camera Settings")
        settings_window.geometry("400x300")
        
        # FPS settings
        fps_frame = ctk.CTkFrame(settings_window)
        fps_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(fps_frame, text="FPS:").pack(side="left", padx=5)
        fps_slider = ctk.CTkSlider(
            fps_frame,
            from_=1,
            to=60,
            command=lambda v: self.update_fps(int(v))
        )
        fps_slider.set(self.camera_manager.fps)
        fps_slider.pack(side="left", expand=True, padx=10)
        
        fps_label = ctk.CTkLabel(fps_frame, text=f"{self.camera_manager.fps} FPS")
        fps_label.pack(side="right", padx=5)

    def show_effect_settings(self):
        """Show effect settings window"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Effect Settings")
        settings_window.geometry("500x600")
        
        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(settings_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Effect speed controls
        for effect in ["static", "glitch", "tear", "vhs", "noise", 
                      "color_distortion", "chromatic", "tracking", "artifacts"]:
            self.create_effect_speed_control(scroll_frame, effect)

    def create_effect_speed_control(self, parent, effect):
        """Create speed control for an effect"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(frame, text=f"{effect.title()} Speed:").pack(side="left", padx=5)
        
        speed_slider = ctk.CTkSlider(
            frame,
            from_=0.1,
            to=2.0,
            command=lambda v: self.update_effect_speed(effect, v)
        )
        speed_slider.set(self.effects_manager.get_effect_speed(effect))
        speed_slider.pack(side="left", expand=True, padx=10)
        
        speed_label = ctk.CTkLabel(frame, text=f"{self.effects_manager.get_effect_speed(effect)}x")
        speed_label.pack(side="right", padx=5)

    def show_settings_window(self):
        """Show settings window with tabs"""
        settings = ctk.CTkToplevel(self.root)
        settings.title("Effects Settings")
        settings.geometry("500x600")
        
        # Create tabview
        tabview = ctk.CTkTabview(settings)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Effects tab
        effects_tab = tabview.add("Effects")
        effects_frame = ctk.CTkScrollableFrame(effects_tab)
        effects_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create effect controls
        effects = ["static", "glitch", "vhs", "noise", "tear", 
                  "chromatic", "color_distortion", "tracking", "artifacts"]
                  
        for effect in effects:
            effect_frame = ctk.CTkFrame(effects_frame)
            effect_frame.pack(fill="x", pady=5)
            
            # Effect toggle
            toggle = ctk.CTkSwitch(
                effect_frame,
                text=effect.title(),
                command=lambda e=effect: self.toggle_effect(e)
            )
            toggle.pack(side="left", padx=5)
            
            # Intensity slider
            intensity_frame = ctk.CTkFrame(effect_frame)
            intensity_frame.pack(side="left", expand=True, padx=5)
            
            ctk.CTkLabel(intensity_frame, text="Intensity:").pack(side="left")
            
            # Intensity slider
            intensity = ctk.CTkSlider(
                intensity_frame,
                from_=0,
                to=100,
                command=lambda v, e=effect: self.update_effect_intensity(e, v/100)
            )
            intensity.pack(side="left", expand=True, padx=5)
            
            # Speed slider
            speed_frame = ctk.CTkFrame(effect_frame)
            speed_frame.pack(side="right", padx=5)
            
            ctk.CTkLabel(speed_frame, text="Speed:").pack(side="left")
            
            # Speed slider
            speed = ctk.CTkSlider(
                speed_frame,
                from_=0,
                to=200,
                command=lambda v, e=effect: self.update_effect_speed(e, v/100)
            )
            speed.pack(side="left", padx=5)

    def update_effect_intensity(self, effect, value, label):
        """Update effect intensity and label"""
        if self.effects_manager:
            self.effects_manager.set_effect_intensity(effect, value)
            if label:
                label.configure(text=f"{int(value * 100)}%")

    def update_effect_speed(self, effect, value, label):
        """Update effect speed and label"""
        if self.effects_manager:
            self.effects_manager.set_effect_speed(effect, value)
            if label:
                label.configure(text=f"{value:.1f}x")

    def toggle_effect(self, key):
        """Toggle effect and update settings"""
        if key in self.toggles:
            enabled = self.toggles[key].get()
            if hasattr(self, 'effects_manager'):
                self.effects_manager.toggle_effect(key, enabled)
                self.apply_effect_changes()

    def create_effect_controls(self, parent):
        """Create effect controls panel"""
        effects_frame = ctk.CTkFrame(parent)
        effects_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        effects = [
            ("static", "Static"),
            ("glitch", "Glitch"),
            ("tear", "Screen Tear"),
            ("vhs", "VHS"),
            ("noise", "Noise"),
            ("color_distortion", "Color Distortion"),
            ("chromatic", "Chromatic"),
            ("tracking", "Tracking Lines"),
            ("artifacts", "Digital Artifacts")
        ]
        
        for effect_key, effect_name in effects:
            # Create effect group
            effect_frame = ctk.CTkFrame(effects_frame)
            effect_frame.pack(fill="x", pady=2)
            
            # Controls container
            controls_container = ctk.CTkFrame(effect_frame)
            controls_container.pack(fill="x", expand=True)
            
            # Left side with toggle
            left_frame = ctk.CTkFrame(controls_container)
            left_frame.pack(side="left", fill="x", expand=True)
            
            # Toggle switch
            toggle = ctk.CTkSwitch(
                left_frame, 
                text=effect_name,
                command=lambda e=effect_key: self.toggle_effect_state(e)
            )
            toggle.pack(side="left", padx=5)
            self.toggles[effect_key] = toggle
            
            # Intensity controls - fixed width
            intensity_frame = ctk.CTkFrame(left_frame, width=200)
            intensity_frame.pack(side="left", padx=5)
            intensity_frame.pack_propagate(False)  # Prevent size changes
            
            ctk.CTkLabel(intensity_frame, text="Intensity:", width=60).pack(side="left")
            
            # Intensity percentage label - fixed width
            percent_label = ctk.CTkLabel(intensity_frame, text=f"{int(DEFAULT_SETTINGS[f'{effect_key}_intensity'] * 100)}%", width=40)
            percent_label.pack(side="right", padx=2)
            
            # Intensity slider
            intensity = ctk.CTkSlider(
                intensity_frame,
                from_=0,
                to=100,
                number_of_steps=100,
                width=100
            )
            intensity.pack(side="right", padx=5)
            self.sliders[f"{effect_key}_intensity"] = intensity
            
            # Speed controls - fixed width
            speed_frame = ctk.CTkFrame(left_frame, width=200)
            speed_frame.pack(side="left", padx=5)
            speed_frame.pack_propagate(False)  # Prevent size changes
            
            ctk.CTkLabel(speed_frame, text="Speed:", width=50).pack(side="left")
            
            # Speed multiplier label - fixed width
            speed_label = ctk.CTkLabel(speed_frame, text=f"{DEFAULT_SETTINGS[f'{effect_key}_speed']:.1f}x", width=40)
            speed_label.pack(side="right", padx=2)
            
            # Speed slider
            speed = ctk.CTkSlider(
                speed_frame,
                from_=0,
                to=200,
                number_of_steps=200,
                width=100
            )
            speed.pack(side="right", padx=5)
            self.sliders[f"{effect_key}_speed"] = speed
            
            # Set initial values and state
            intensity.set(DEFAULT_SETTINGS[f"{effect_key}_intensity"] * 100)
            speed.set(DEFAULT_SETTINGS[f"{effect_key}_speed"] * 100)
            
            # Configure slider commands
            intensity.configure(
                command=lambda v, e=effect_key, l=percent_label: 
                    self.update_effect_intensity(e, v/100, l)
            )
            speed.configure(
                command=lambda v, e=effect_key, l=speed_label: 
                    self.update_effect_speed(e, v/100, l)
            )
            
            # Set initial toggle state and disable controls if needed
            if DEFAULT_SETTINGS[f"{effect_key}_enabled"]:
                toggle.select()
            else:
                toggle.deselect()
                intensity.configure(state="disabled")
                speed.configure(state="disabled")

    def toggle_effect_state(self, effect):
        """Toggle effect and control states"""
        enabled = self.toggles[effect].get()
        
        # Update effect state
        if self.effects_manager:
            self.effects_manager.toggle_effect(effect, enabled)
        
        # Update control states
        intensity_slider = self.sliders.get(f"{effect}_intensity")
        speed_slider = self.sliders.get(f"{effect}_speed")
        
        if intensity_slider:
            intensity_slider.configure(state="normal" if enabled else "disabled")
        if speed_slider:
            speed_slider.configure(state="normal" if enabled else "disabled")

    def create_preview(self, parent):
        """Create preview area"""
        preview_frame = ctk.CTkFrame(parent)
        preview_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.preview_label = ctk.CTkLabel(
            preview_frame,
            text="",
            fg_color="black"
        )
        self.preview_label.pack(fill="both", expand=True)

    def update_glitch_duration(self, value, label):
        """Update glitch frame duration"""
        if self.effects_manager:
            self.effects_manager.effect_intensities["glitch_duration"] = value
            label.configure(text=f"{value:.1f}s")