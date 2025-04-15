import cv2
import numpy as np
from src.node import Node

class BlendNode(Node):
    
    def __init__(self, name="Blend", id=None):
        super().__init__(name, id)
        
        self.inputs = {
            "image1": None,  
            "image2": None   
        }
        
        self.outputs = {
            "image": "image"  
        }
        
        self.parameters = {
            "blend_mode": "normal",  #blend mode (normal, multiply, screen, overlay, difference)
            "opacity": 1.0           
        }
    
    def process(self):
        
        image1 = self.get_input_data("image1")
        image2 = self.get_input_data("image2")
        
        if image1 is None or image2 is None:
            print("Error: Both input images must be connected")
            return False
        
        try:
            if len(image1.shape) != len(image2.shape):
                if len(image1.shape) == 2:
                    image1 = cv2.cvtColor(image1, cv2.COLOR_GRAY2RGB)
                elif len(image2.shape) == 2:
                    image2 = cv2.cvtColor(image2, cv2.COLOR_GRAY2RGB)
            
            #ensure both images have the same dimensions
            if image1.shape[:2] != image2.shape[:2]:
                image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
            
            blend_mode = self.parameters["blend_mode"]
            opacity = max(0.0, min(1.0, self.parameters["opacity"]))
            
            #apply blend mode
            if blend_mode == "normal":
                result = cv2.addWeighted(image1, 1.0 - opacity, image2, opacity, 0)
                
            elif blend_mode == "multiply":
                img1_float = image1.astype(np.float32) / 255.0
                img2_float = image2.astype(np.float32) / 255.0
                
                blended = img1_float * img2_float
                
                if opacity < 1.0:
                    blended = img1_float * (1.0 - opacity) + blended * opacity
                
                result = (blended * 255.0).astype(np.uint8)
                
            elif blend_mode == "screen":
                img1_float = image1.astype(np.float32) / 255.0
                img2_float = image2.astype(np.float32) / 255.0
                
                blended = 1.0 - (1.0 - img1_float) * (1.0 - img2_float)
                
                if opacity < 1.0:
                    blended = img1_float * (1.0 - opacity) + blended * opacity
                
                result = (blended * 255.0).astype(np.uint8)
                
            elif blend_mode == "overlay":
                #overlay blend mode
                img1_float = image1.astype(np.float32) / 255.0
                img2_float = image2.astype(np.float32) / 255.0
                
                mask = img1_float < 0.5
                blended = np.zeros_like(img1_float)
                blended[mask] = 2.0 * img1_float[mask] * img2_float[mask]
                blended[~mask] = 1.0 - 2.0 * (1.0 - img1_float[~mask]) * (1.0 - img2_float[~mask])
                
                if opacity < 1.0:
                    blended = img1_float * (1.0 - opacity) + blended * opacity
                
                result = (blended * 255.0).astype(np.uint8)
                
            elif blend_mode == "difference":
                img1_float = image1.astype(np.float32) / 255.0
                img2_float = image2.astype(np.float32) / 255.0
                
                blended = np.abs(img1_float - img2_float)
                
                if opacity < 1.0:
                    blended = img1_float * (1.0 - opacity) + blended * opacity
                
                result = (blended * 255.0).astype(np.uint8)
                
            else:
                print(f"Error: Unsupported blend mode: {blend_mode}")
                return False
            
            self.processed_data["image"] = result
            
            self.dirty = False
            
            return True
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return False
