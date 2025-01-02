import cv2
import numpy as np
import random
import time
import os
from config import FRAMES_DIR, EXTRA_DIR, DEFAULT_SETTINGS
from animations import FNAFAnimations

class FNAFEffects:
    def __init__(self, animations=None):
        self.preloaded_images = self.load_frames()
        self.extra_images = self.load_extra_images()
        self.last_glitch_time = 0
        self.last_extra_time = 0
        self.glitch_active = False
        self.glitch_frame_count = 0
        self.frame_number = 0
        
        # Make sure we initialize these dictionaries
        self.effect_speeds = {
            "static": 1.0,
            "glitch": 1.0,
            "tear": 1.0,
            "vhs": 1.0,
            "noise": 1.0,
            "color_distortion": 1.0,
            "chromatic": 1.0,
            "tracking": 1.0,
            "artifacts": 1.0
        }
        
        # Initialize effect states from DEFAULT_SETTINGS
        self.effect_enabled = {
            "static": DEFAULT_SETTINGS["static_enabled"],
            "glitch": DEFAULT_SETTINGS["glitch_enabled"],
            "tear": DEFAULT_SETTINGS["tear_enabled"],
            "vhs": DEFAULT_SETTINGS["vhs_enabled"],
            "noise": DEFAULT_SETTINGS["noise_enabled"],
            "color_distortion": DEFAULT_SETTINGS["color_distortion_enabled"],
            "chromatic": DEFAULT_SETTINGS["chromatic_enabled"],
            "tracking": DEFAULT_SETTINGS["tracking_enabled"],
            "artifacts": DEFAULT_SETTINGS["artifacts_enabled"]
        }
        
        # Initialize effect intensities
        self.effect_intensities = {
            "static": DEFAULT_SETTINGS["static_intensity"],
            "glitch": DEFAULT_SETTINGS["glitch_intensity"],
            "tear": DEFAULT_SETTINGS["tear_intensity"],
            "vhs": DEFAULT_SETTINGS["vhs_intensity"],
            "noise": DEFAULT_SETTINGS["noise_intensity"],
            "color_distortion": DEFAULT_SETTINGS["color_distortion_intensity"],
            "chromatic": DEFAULT_SETTINGS["chromatic_intensity"],
            "tracking": DEFAULT_SETTINGS["tracking_intensity"],
            "artifacts": DEFAULT_SETTINGS["artifacts_intensity"],
            "glitch_duration": DEFAULT_SETTINGS["glitch_duration"],
            "glitch_frequency": DEFAULT_SETTINGS["glitch_frequency"],
            "glitch_burst_chance": DEFAULT_SETTINGS["glitch_burst_chance"]
        }
        self.animations = animations if animations else FNAFAnimations()
        
        # Separate glitch timing from other effects
        self.glitch_timer = {
            "last_time": time.time(),
            "frame_start": 0,
            "active": False,
            "frame_count": 0,
            "current_frame": None
        }
        
    def load_frames(self):
        """Load glitch frames from static/frames directory"""
        frames = []
        for file in os.listdir(FRAMES_DIR):
            if file.endswith(('.png', '.jpg')):
                path = os.path.join(FRAMES_DIR, file)
                img = cv2.imread(path)
                if img is not None:
                    frames.append(cv2.resize(img, (640, 480)))
        return frames

    def load_extra_images(self):
        """Load extra images from static/extra directory"""
        extras = []
        for file in os.listdir(EXTRA_DIR):
            if file.endswith('.png'):
                path = os.path.join(EXTRA_DIR, file)
                img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if img is not None:
                    extras.append(cv2.resize(img, (640, 480)))
        return extras

    def apply_effects(self, frame, settings=None):
        """Apply all enabled effects to frame"""
        if frame is None:
            return None
        
        try:
            # Apply glitch first to maintain timing
            if self.effect_enabled["glitch"]:
                frame = self.apply_glitch(frame)
            
            # Apply other effects
            if self.effect_enabled["static"]:
                frame = self.apply_static(frame, self.effect_intensities["static"])
            
            if self.effect_enabled["tear"]:
                frame = self.apply_tear(frame, self.effect_intensities["tear"])
                
            if self.effect_enabled["vhs"]:
                frame = self.apply_vhs_effect(frame, self.effect_intensities["vhs"])
                
            if self.effect_enabled["noise"]:
                frame = self.apply_noise(frame, self.effect_intensities["noise"])
                
            if self.effect_enabled["color_distortion"]:
                frame = self.apply_color_distortion(frame, self.effect_intensities["color_distortion"])
                
            if self.effect_enabled["chromatic"]:
                frame = self.apply_chromatic_aberration(frame, self.effect_intensities["chromatic"])
                
            if self.effect_enabled["tracking"]:
                frame = self.apply_vhs_tracking(frame, self.effect_intensities["tracking"])
                
            if self.effect_enabled["artifacts"]:
                frame = self.apply_digital_artifacts(frame, self.effect_intensities["artifacts"])
                
            return frame
            
        except Exception as e:
            print(f"Effect error: {str(e)}")
            return frame

    def apply_vhs_effect(self, frame, intensity):
        """Apply VHS-style distortion effect with reduced intensity"""
        # Create noise pattern
        noise = np.random.randint(0, 255, frame.shape, dtype='uint8')
        noise = cv2.GaussianBlur(noise, (3, 3), 0)
        
        # Add scanlines with reduced intensity
        height, width = frame.shape[:2]
        scanlines = np.zeros((height, width, 3), dtype='uint8')
        for i in range(0, height, 2):
            scanlines[i, :] = [25, 25, 25]  # Reduced scanline intensity
        
        # Apply color bleeding with reduced shift
        channels = cv2.split(frame)
        shifted_channels = []
        for i, channel in enumerate(channels):
            shift = int(2 * intensity * (i - 1))  # Reduced shift amount
            shifted = np.roll(channel, shift, axis=1)
            shifted_channels.append(shifted)
        
        frame = cv2.merge(shifted_channels)
        
        # Combine effects with reduced intensity
        frame = cv2.addWeighted(frame, 1 - intensity * 0.3, noise, intensity * 0.1, 0)
        frame = cv2.addWeighted(frame, 1, scanlines, intensity * 0.2, 0)
        
        return frame

    def apply_chromatic_aberration(self, frame, intensity):
        """Apply chromatic aberration effect with intensity"""
        shift = int(5 * intensity)  # Scale the shift by intensity
        rows, cols = frame.shape[:2]
        
        # Split channels
        b, g, r = cv2.split(frame)
        
        # Create translation matrices
        M_left = np.float32([[1, 0, -shift], [0, 1, 0]])
        M_right = np.float32([[1, 0, shift], [0, 1, 0]])
        
        # Apply shift to red and blue channels
        r = cv2.warpAffine(r, M_right, (cols, rows))
        b = cv2.warpAffine(b, M_left, (cols, rows))
        
        return cv2.merge([b, g, r])

    def apply_vhs_tracking(self, frame, intensity):
        """Apply VHS tracking lines effect with intensity"""
        if random.random() > intensity:  # Only apply sometimes based on intensity
            return frame
        
        height, width = frame.shape[:2]
        y_pos = random.randint(0, height - 20)
        tracking_height = random.randint(10, int(20 * intensity))
        
        tracking_area = frame[y_pos:y_pos + tracking_height, :]
        noise = np.random.randint(0, 255, tracking_area.shape, dtype='uint8')
        
        frame[y_pos:y_pos + tracking_height, :] = cv2.addWeighted(
            tracking_area, 1 - intensity, noise, intensity, 0
        )
        
        return frame

    def apply_color_corruption(self, frame):
        """Apply color corruption effect"""
        # Randomly modify color channels
        channels = list(cv2.split(frame))
        
        # Choose a random channel to corrupt
        corrupt_channel = random.randint(0, 2)
        
        # Apply random corruption
        corruption = np.random.randint(-50, 50)
        channels[corrupt_channel] = cv2.add(channels[corrupt_channel], corruption)
        
        return cv2.merge(channels)

    def apply_digital_artifacts(self, frame, intensity):
        """Apply digital artifact glitches with intensity"""
        height, width = frame.shape[:2]
        
        num_artifacts = int(random.randint(3, 8) * intensity)
        for _ in range(num_artifacts):
            x = random.randint(0, width - 50)
            y = random.randint(0, height - 50)
            w = random.randint(20, int(50 * intensity))
            h = random.randint(10, int(30 * intensity))
            
            block = frame[y:y+h, x:x+w].copy()
            
            if random.random() < 0.5:
                block.sort(axis=1)
            else:
                block = np.roll(block, int(random.randint(-10, 10) * intensity), axis=1)
            
            frame[y:y+h, x:x+w] = block
        
        return frame

    def apply_color_distortion(self, frame, intensity):
        """Apply color distortion effect"""
        # Split into channels
        b, g, r = cv2.split(frame)
        
        # Apply different intensity modifications to each channel
        b = cv2.addWeighted(b, 1 + intensity * 0.2, np.zeros_like(b), 0, random.randint(-20, 20))
        g = cv2.addWeighted(g, 1 - intensity * 0.1, np.zeros_like(g), 0, random.randint(-20, 20))
        r = cv2.addWeighted(r, 1 + intensity * 0.15, np.zeros_like(r), 0, random.randint(-20, 20))
        
        # Merge channels with slight offset
        shift = int(intensity * 4)
        rows, cols = frame.shape[:2]
        
        # Create translation matrices
        M_left = np.float32([[1, 0, -shift], [0, 1, 0]])
        M_right = np.float32([[1, 0, shift], [0, 1, 0]])
        
        # Apply channel shifts
        r = cv2.warpAffine(r, M_right, (cols, rows))
        b = cv2.warpAffine(b, M_left, (cols, rows))
        
        return cv2.merge([b, g, r])

    def apply_static(self, frame, intensity):
        """Apply static noise effect similar to camera3"""
        if frame is None:
            return None
        
        # Use camera3's static implementation
        static_overlay = np.random.randint(50, 150, (frame.shape[0], frame.shape[1]), dtype='uint8')
        static_resized = cv2.cvtColor(static_overlay, cv2.COLOR_GRAY2BGR)
        
        # Reduced alpha for more subtle effect
        alpha = intensity * 0.3
        return cv2.addWeighted(frame, 1 - alpha, static_resized, alpha, 0)

    def apply_glitch(self, frame):
        """Apply glitch effect with independent timing"""
        current_time = time.time()
        
        # Check if we should start a new glitch sequence
        if not self.glitch_timer["active"]:
            if current_time - self.glitch_timer["last_time"] > self.effect_intensities["glitch_frequency"]:
                if random.random() < self.effect_intensities["glitch"]:
                    self.glitch_timer["active"] = True
                    self.glitch_timer["last_time"] = current_time
                    self.glitch_timer["frame_start"] = current_time
                    self.glitch_timer["current_frame"] = random.choice(self.preloaded_images)
                    self.glitch_timer["frame_count"] = random.choice(DEFAULT_SETTINGS["glitch_frames_in_burst"])
        
        # If glitch is active, check if we should switch to next frame
        elif current_time - self.glitch_timer["frame_start"] >= self.effect_intensities["glitch_duration"]:
            if self.glitch_timer["frame_count"] > 1:
                # Switch to next frame
                self.glitch_timer["current_frame"] = random.choice(self.preloaded_images)
                self.glitch_timer["frame_start"] = current_time
                self.glitch_timer["frame_count"] -= 1
            else:
                # End glitch sequence
                self.glitch_timer["active"] = False
                self.glitch_timer["frame_count"] = 0
                return frame
        
        # Apply current glitch frame if active
        if self.glitch_timer["active"] and self.glitch_timer["current_frame"] is not None:
            blend_alpha = DEFAULT_SETTINGS["glitch_blend_alpha"]
            return cv2.addWeighted(frame, 1 - blend_alpha, self.glitch_timer["current_frame"], blend_alpha, 0)
        
        return frame

    def should_glitch(self, probability):
        """Determine if glitch should occur"""
        current_time = time.time()
        if current_time - self.last_glitch_time > 0.1:  # Minimum time between glitches
            if random.random() < probability / 100:
                self.last_glitch_time = current_time
                return True
        return False

    def apply_screen_tear(self, frame):
        """Apply screen tear effect"""
        height, width = frame.shape[:2]
        tear_point = random.randint(0, height)
        tear_height = random.randint(10, 50)
        
        # Create tear effect
        if tear_point + tear_height < height:
            frame[tear_point:tear_point + tear_height] = np.roll(
                frame[tear_point:tear_point + tear_height],
                random.randint(-50, 50),
                axis=1
            )
        return frame

    def apply_noise(self, frame, intensity):
        """Apply noise effect"""
        noise = np.random.normal(0, intensity * 30, frame.shape).astype('uint8')
        return cv2.add(frame, noise)

    def reload_frames(self):
        """Reload glitch frames"""
        self.preloaded_images = self.load_frames()
        
    def reload_extra_images(self):
        """Reload extra effect images"""
        self.extra_images = self.load_extra_images()

    def set_effect_speed(self, effect, speed):
        """Set speed multiplier for an effect"""
        if effect in self.effect_speeds:
            self.effect_speeds[effect] = speed

    def get_effect_speed(self, effect):
        """Get speed multiplier for an effect"""
        return self.effect_speeds.get(effect, 1.0)

    def toggle_effect(self, effect, enabled):
        """Toggle effect on/off"""
        if effect in self.effect_speeds:
            self.effect_enabled[effect] = enabled

    def set_effect_intensity(self, effect, value):
        """Set effect intensity with camera3-style timing"""
        if effect in self.effect_intensities:
            self.effect_intensities[effect] = value
            
            # Update glitch timing based on intensity
            if effect == "glitch":
                # More aggressive timing values matching camera3.py
                self.effect_intensities["glitch_duration"] = 0.5  # Fixed 0.5s duration
                self.effect_intensities["glitch_frequency"] = max(2.0, (1.0 - value) * 4.0)  # 2-4s between glitches
                self.effect_intensities["glitch_burst_chance"] = min(0.8, value * 0.8)  # Up to 80% chance of bursts
