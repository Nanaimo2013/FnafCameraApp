import cv2
import pyvirtualcam
from pyvirtualcam import PixelFormat
from threading import Thread
import time
import os

class CameraManager:
    def __init__(self):
        self.cap = None
        self.virtual_camera = None
        self.running = False
        self.preview_callback = None
        self.fps = 30
        self.virtual_camera_enabled = True
        
    def get_available_cameras(self):
        """Detect available cameras using DirectShow"""
        cameras = []
        for index in range(10):
            try:
                cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
                if cap.isOpened():
                    ret, _ = cap.read()
                    if ret:
                        cameras.append((index, f"Camera {index}"))
                    cap.release()
            except:
                continue
        return cameras
    
    def set_preview_callback(self, callback):
        """Set callback function for preview updates"""
        self.preview_callback = callback
        
    def start_camera(self, camera_index):
        """Start capturing from selected camera"""
        try:
            self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                return False
                
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            # Initialize virtual camera if enabled
            if self.virtual_camera_enabled:
                width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.virtual_camera = pyvirtualcam.Camera(
                    width=width,
                    height=height,
                    fps=self.fps,
                    fmt=PixelFormat.BGR
                )
            
            self.running = True
            return True
            
        except Exception as e:
            print(f"Error starting camera: {str(e)}")
            return False
            
    def stop_camera(self):
        """Stop camera capture"""
        self.running = False
        if self.cap:
            self.cap.release()
        if self.virtual_camera:
            self.virtual_camera.close()
            
    def set_fps(self, fps):
        """Set camera FPS"""
        self.fps = fps
        if self.cap:
            self.cap.set(cv2.CAP_PROP_FPS, fps)
            
    def capture_frame(self, save_dir):
        """Capture single frame and save to file"""
        if not self.cap:
            return None
            
        ret, frame = self.cap.read()
        if ret:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"capture_{timestamp}.png"
            filepath = os.path.join(save_dir, filename)
            cv2.imwrite(filepath, frame)
            return filename
        return None
        
    def process_video(self, effects_manager=None, settings=None):
        """Process video feed with effects"""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Apply effects if available
            if effects_manager:
                frame = effects_manager.apply_effects(frame, settings)
                
            # Update preview
            if self.preview_callback:
                self.preview_callback(frame)
                
            # Send to virtual camera if enabled
            if self.virtual_camera_enabled and self.virtual_camera:
                self.virtual_camera.send(frame)
                
            yield frame
    