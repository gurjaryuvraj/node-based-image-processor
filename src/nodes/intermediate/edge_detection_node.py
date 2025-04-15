import cv2
import numpy as np
from src.node import Node

class EdgeDetectionNode(Node):    
    def __init__(self, name="Edge Detection", id=None):
        super().__init__(name, id)
        
        self.inputs = {
            "image": None  
        }
        
        self.outputs = {
            "image": "image", 
            "edges": "image"   
        }
        
        self.parameters = {
            "algorithm": "sobel",    #edge detection algorithm (sobel, canny) 
            "threshold1": 100,       #first threshold for Canny
            "threshold2": 200,        #second threshold for Canny
            "sobel_ksize": 3,        #kernel size for Sobel (1, 3, 5, 7)
            "sobel_scale": 1,         
            "sobel_delta": 0,         
            "overlay": False,         
            "overlay_color": [0, 255, 0],  
            "overlay_opacity": 0.7    
        }
    
    def process(self):
       
        input_image = self.get_input_data("image")
        
        if input_image is None:
            print("Error: No input image connected")
            return False
        
        try:
            if len(input_image.shape) > 2:
                gray_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)
            else:
                gray_image = input_image.copy()
            
            algorithm = self.parameters["algorithm"]
            
            if algorithm == "sobel":
                ksize = self.parameters["sobel_ksize"]
                scale = self.parameters["sobel_scale"]
                delta = self.parameters["sobel_delta"]
                
                if ksize not in [1, 3, 5, 7]:
                    ksize = 3
                
                grad_x = cv2.Sobel(gray_image, cv2.CV_16S, 1, 0, ksize=ksize, scale=scale, delta=delta)
                grad_y = cv2.Sobel(gray_image, cv2.CV_16S, 0, 1, ksize=ksize, scale=scale, delta=delta)
                
                abs_grad_x = cv2.convertScaleAbs(grad_x)
                abs_grad_y = cv2.convertScaleAbs(grad_y)
                
                edges = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
                
            elif algorithm == "canny":
                threshold1 = self.parameters["threshold1"]
                threshold2 = self.parameters["threshold2"]
                
                edges = cv2.Canny(gray_image, threshold1, threshold2)
                
            else:
                print(f"Error: Unsupported edge detection algorithm: {algorithm}")
                return False
            
            self.processed_data["edges"] = edges
            
            if self.parameters["overlay"]:
                if len(input_image.shape) == 3:
                    overlay_color = self.parameters["overlay_color"]
                    overlay_opacity = self.parameters["overlay_opacity"]
                    
                    edge_mask = np.zeros_like(input_image)
                    edge_mask[edges > 0] = overlay_color
                    
                    result = cv2.addWeighted(
                        input_image, 
                        1.0, 
                        edge_mask, 
                        overlay_opacity, 
                        0
                    )
                else:
                    result = cv2.addWeighted(gray_image, 0.7, edges, 0.3, 0)
            else:
                if len(input_image.shape) == 3:
                    result = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
                else:
                    result = edges
            
            self.processed_data["image"] = result
            
            self.dirty = False
            
            return True
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return False
