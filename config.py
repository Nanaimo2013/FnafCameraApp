import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
FRAMES_DIR = os.path.join(STATIC_DIR, "frames")
EXTRA_DIR = os.path.join(STATIC_DIR, "extra")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")

# Create directories if they don't exist
for dir_path in [STATIC_DIR, FRAMES_DIR, EXTRA_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# Default settings
DEFAULT_SETTINGS = {
    # Effect toggles and intensities
    "static_enabled": True,
    "static_intensity": 0.1,
    
    "glitch_enabled": True,
    "glitch_intensity": 0.1,
    
    "tear_enabled": True,
    "tear_intensity": 0.3,
    
    "vhs_enabled": False,
    "vhs_intensity": 0.1,
    
    "noise_enabled": False,
    "noise_intensity": 0.4,
    
    "color_distortion_enabled": False,
    "color_distortion_intensity": 0.5,
    
    "chromatic_enabled": False,
    "chromatic_intensity": 0.3,
    
    "tracking_enabled": False,
    "tracking_intensity": 0.3,
    
    "artifacts_enabled": False,
    "artifacts_intensity": 0.3,
    
    # Additional settings
    "theme": "dark",
    
    # Add virtual camera settings
    "virtual_camera_enabled": True,
    "virtual_camera_backend": "obs"
}

# Add to DEFAULT_SETTINGS
DEFAULT_SETTINGS.update({
    # Camera settings
    "fps": 10,
    "effect_speed": 1.0,
    
    # Effect speeds (multipliers)
    "static_speed": 1.0,
    "glitch_speed": 1.0,
    "tear_speed": 1.0,
    "vhs_speed": 1.0,
    "noise_speed": 1.0,
    "color_distortion_speed": 1.0,
    "chromatic_speed": 1.0,
    "tracking_speed": 1.0,
    "artifacts_speed": 1.0,
    
    # Glitch timing settings
    "glitch_duration": 2.0,      # Each frame lasts 5 seconds
    "glitch_frequency": 3.0,     # Time between glitch sequences
    "glitch_burst_chance": 2.5,  # Chance for multi-frame bursts
    "glitch_frames_in_burst": [1, 2, 3],  # Possible number of frames in sequence
    "glitch_blend_alpha": 1.0,   # Blend ratio
})

# Add version info
APP_INFO = {
    "version": "v2.0.2",
    "author": "Nanaimo_2013",
    "title": "Nan's FNAF Camera"
}

# Updated themes with more distinct designs
THEMES = {
    "dark": {
        "bg": "#1a1a1a",
        "fg": "#ffffff",
        "accent": "#ff4444",
        "button": "#2d2d2d",
        "slider": "#404040",
        "header": "#0f0f0f",
        "border": "#3d3d3d",
        "hover": "#ff6666",
        "switch": "#ff4444",
        "dropdown": "#2d2d2d",
        "title": "#ff4444",
        "subtitle": "#cccccc"
    },
    "light": {
        "bg": "#f0f2f5",
        "fg": "#2d2d2d",
        "accent": "#e63946",
        "button": "#ffffff",
        "slider": "#e2e2e2",
        "header": "#ffffff",
        "border": "#d1d1d1",
        "hover": "#ff6b6b",
        "switch": "#e63946",
        "dropdown": "#ffffff",
        "title": "#e63946",
        "subtitle": "#666666"
    },
    "midnight": {
        "bg": "#0a0a1f",
        "fg": "#e0e0ff",
        "accent": "#9d00ff",
        "button": "#1a1a3e",
        "slider": "#2a2a4d",
        "header": "#05051a",
        "border": "#2a2a5d",
        "hover": "#b238ff",
        "switch": "#9d00ff",
        "dropdown": "#1a1a3e",
        "title": "#9d00ff",
        "subtitle": "#8080ff"
    }
}
