import cv2
import numpy as np
from src.node import Node

class BlurNode(Node):    
    def __init__(self, name="Blur", id=None):
        super().__init__(name, id)
        
        self.inputs = {
            "image": None  
        }
        
        self.outputs = {
            "image": "image",  
            "kernel": "image"  
        }
        
        self.parameters = {
            "radius": 5,      #blur radius (1-20px)       
            "directional": False,    
            "direction_angle": 0,    
            "direction_strength": 1.0  
        }
    
    def process(self):
        
        input_image = self.get_input_data("image")
        
        if input_image is None:
            print("Error: No input image connected")
            return False
        
        try:
            radius = max(1, min(20, self.parameters["radius"]))
            directional = self.parameters["directional"]
            
            kernel_size = 2 * radius + 1
            
            if not directional:
                result = cv2.GaussianBlur(input_image, (kernel_size, kernel_size), 0)
                
                kernel = cv2.getGaussianKernel(kernel_size, 0)
                kernel = kernel * kernel.T  # Outer product to get 2D kernel
                
                kernel_vis = (kernel / kernel.max() * 255).astype(np.uint8)
                
                if len(input_image.shape) == 3:
                    kernel_vis = cv2.cvtColor(kernel_vis, cv2.COLOR_GRAY2RGB)
            
            else:
                angle = self.parameters["direction_angle"]
                strength = self.parameters["direction_strength"]
                
                angle_rad = np.deg2rad(angle)
                
                kernel = np.zeros((kernel_size, kernel_size))
                
                center = kernel_size // 2
                
                for i in range(-center, center + 1):
                    x = int(round(i * np.cos(angle_rad)))
                    y = int(round(i * np.sin(angle_rad)))
                    
                    if abs(x) <= center and abs(y) <= center:
                        kernel[center + y, center + x] = 1
                
                kernel = kernel / kernel.sum()
                
                if strength < 1.0:
                    gaussian_kernel = cv2.getGaussianKernel(kernel_size, 0)
                    gaussian_kernel = gaussian_kernel * gaussian_kernel.T
                    kernel = kernel * strength + gaussian_kernel * (1 - strength)
                
                result = cv2.filter2D(input_image, -1, kernel)
                
                kernel_vis = (kernel / kernel.max() * 255).astype(np.uint8)
                
                if len(input_image.shape) == 3:
                    kernel_vis = cv2.cvtColor(kernel_vis, cv2.COLOR_GRAY2RGB)
            
            self.processed_data["image"] = result
            self.processed_data["kernel"] = kernel_vis
            
            self.dirty = False
            
            return True
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return False
