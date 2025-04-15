import cv2
import numpy as np
import matplotlib.pyplot as plt
from src.node import Node

class ThresholdNode(Node):    
    def __init__(self, name="Threshold", id=None):
        
        super().__init__(name, id)
        
        self.inputs = {
            "image": None  
        }
        
        self.outputs = {
            "image": "image",     
            "histogram": "image"   
        }
        
        self.parameters = {
            "threshold_value": 127,    #threshold value (0-255) 
            "max_value": 255,           #maximum value for binary threshold
            "threshold_type": "binary", #thresholding method (binary, adaptive, otsu)
            "adaptive_method": "mean",  #adaptive method (mean, gaussian)
            "block_size": 11,           #block size for adaptive threshold (must be odd)
            "c_value": 2                #constant subtracted from mean/gaussian
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
            
            threshold_value = self.parameters["threshold_value"]
            max_value = self.parameters["max_value"]
            threshold_type = self.parameters["threshold_type"]
            
            if threshold_type == "binary":
                _, result = cv2.threshold(gray_image, threshold_value, max_value, cv2.THRESH_BINARY)
                
            elif threshold_type == "adaptive":
                adaptive_method = self.parameters["adaptive_method"]
                block_size = self.parameters["block_size"]
                c_value = self.parameters["c_value"]
                
                if block_size % 2 == 0:
                    block_size += 1
                
                if adaptive_method == "mean":
                    result = cv2.adaptiveThreshold(
                        gray_image, 
                        max_value, 
                        cv2.ADAPTIVE_THRESH_MEAN_C, 
                        cv2.THRESH_BINARY, 
                        block_size, 
                        c_value
                    )
                else: 
                    result = cv2.adaptiveThreshold(
                        gray_image, 
                        max_value, 
                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                        cv2.THRESH_BINARY, 
                        block_size, 
                        c_value
                    )
                    
            elif threshold_type == "otsu":
                _, result = cv2.threshold(gray_image, 0, max_value, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            else:
                print(f"Error: Unsupported threshold type: {threshold_type}")
                return False
            
            hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
            
            fig = plt.figure(figsize=(8, 4))
            plt.plot(hist)
            plt.xlim([0, 256])
            plt.axvline(x=threshold_value, color='r', linestyle='--')
            plt.title('Image Histogram with Threshold')
            plt.xlabel('Pixel Value')
            plt.ylabel('Frequency')
            plt.grid(True)
            
            fig.canvas.draw()
            hist_image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
            hist_image = hist_image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            plt.close(fig)
            
            if len(input_image.shape) == 3:
                result_rgb = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
                self.processed_data["image"] = result_rgb
            else:
                self.processed_data["image"] = result
            
            self.processed_data["histogram"] = hist_image
            
            self.dirty = False
            
            return True
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return False
