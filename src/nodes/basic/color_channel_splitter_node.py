import cv2
import numpy as np
from src.node import Node

class ColorChannelSplitterNode(Node):    
    def __init__(self, name="Color Channel Splitter", id=None):
        
        super().__init__(name, id)

        self.node_content_height = 250 

        self.inputs = {
            "image": None  
        }
        
        self.outputs = {
            "red": "channel",      
            "green": "channel",    
            "blue": "channel",     
            "alpha": "channel",   
            "grayscale_r": "channel",  
            "grayscale_g": "channel",  
            "grayscale_b": "channel",  
            "grayscale_a": "channel", 
        }
        
        self.parameters = {
            "output_grayscale": True,  
        }
    
    def process(self):
        """
        Split the input image into separate color channels.
        
        Returns:
            bool: True if processing was successful, False otherwise
        """
       
        input_image = self.get_input_data("image")
        
        if input_image is None:
            print("Error: No input image connected")
            return False
        
        try:
            
            if len(input_image.shape) < 3:
                print("Error: Input image must have color channels")
                return False
            
            height, width, channels = input_image.shape
            
            if channels == 3:  # RGB
                b, g, r = cv2.split(input_image)
                
                self.processed_data["red"] = r
                self.processed_data["green"] = g
                self.processed_data["blue"] = b
                self.processed_data["alpha"] = None
                
                if self.parameters["output_grayscale"]:
                    grayscale_r = np.zeros_like(input_image)
                    grayscale_r[:,:,0] = r
                    
                    grayscale_g = np.zeros_like(input_image)
                    grayscale_g[:,:,1] = g
                    
                    grayscale_b = np.zeros_like(input_image)
                    grayscale_b[:,:,2] = b
                    
                    self.processed_data["grayscale_r"] = grayscale_r
                    self.processed_data["grayscale_g"] = grayscale_g
                    self.processed_data["grayscale_b"] = grayscale_b
                    self.processed_data["grayscale_a"] = None
                
            elif channels == 4:  # RGBA
                b, g, r, a = cv2.split(input_image)
                
                self.processed_data["red"] = r
                self.processed_data["green"] = g
                self.processed_data["blue"] = b
                self.processed_data["alpha"] = a
                
                if self.parameters["output_grayscale"]:
                    grayscale_r = np.zeros_like(input_image)
                    grayscale_r[:,:,0] = r
                    grayscale_r[:,:,3] = 255  
                    
                    grayscale_g = np.zeros_like(input_image)
                    grayscale_g[:,:,1] = g
                    grayscale_g[:,:,3] = 255  
                    
                    grayscale_b = np.zeros_like(input_image)
                    grayscale_b[:,:,2] = b
                    grayscale_b[:,:,3] = 255 
                    
                    grayscale_a = np.zeros_like(input_image)
                    grayscale_a[:,:,0] = a  
                    grayscale_a[:,:,1] = a  
                    grayscale_a[:,:,2] = a 
                    grayscale_a[:,:,3] = 255  
                    
                    self.processed_data["grayscale_r"] = grayscale_r
                    self.processed_data["grayscale_g"] = grayscale_g
                    self.processed_data["grayscale_b"] = grayscale_b
                    self.processed_data["grayscale_a"] = grayscale_a
            
            else:
                print(f"Error: Unsupported number of channels: {channels}")
                return False
            
           
            self.dirty = False
            
            return True
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return False
