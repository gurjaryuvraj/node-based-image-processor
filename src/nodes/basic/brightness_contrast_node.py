import cv2
import numpy as np
from src.node import Node

class BrightnessContrastNode(Node):
    
    def __init__(self, name="Brightness/Contrast", id=None):
        super().__init__(name, id)

        self.inputs = {
            "image": None  
        }
        
        self.outputs = {
            "image": "image"  
        }
        
        self.parameters = {
            "brightness": 0,    
            "contrast": 1.0,    
        }
    
    def process(self):
        input_image = self.get_input_data("image")
        
        if input_image is None:
            print("Error: No input image connected")
            return False
        
        try:
            result = input_image.copy()
            
            brightness = self.parameters["brightness"]  
            contrast = self.parameters["contrast"]      
            
            if brightness != 0:
                if result.dtype != np.float32:
                    result = result.astype(np.float32)
                
                brightness_factor = brightness / 100.0 * 255.0
                
                result = cv2.add(result, brightness_factor)
            
            if contrast != 1.0:
                if result.dtype != np.float32:
                    result = result.astype(np.float32)
                
                result = (result - 128.0) * contrast + 128.0
            
            if input_image.dtype == np.uint8:
                result = np.clip(result, 0, 255).astype(np.uint8)
            else:
                result = np.clip(result, 0, 1.0).astype(input_image.dtype)
            
            self.processed_data["image"] = result
            
            self.dirty = False
            
            return True
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return False
    
    def reset_brightness(self):
        self.parameters["brightness"] = 0
        self.dirty = True
    
    def reset_contrast(self):
        self.parameters["contrast"] = 1.0
        self.dirty = True
