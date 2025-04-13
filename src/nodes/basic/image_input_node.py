import os
import cv2
import numpy as np
from src.node import Node

class ImageInputNode(Node):

    def __init__(self, name="Image Input", id=None):
        
        super().__init__(name, id)
        
        #outputs
        self.outputs = {
            "image": "image",  # Main image output
        }
        
        #parameters
        self.parameters = {
            "file_path": "", 
            "preserve_alpha": True,  # Whether to preserve alpha channel if present
        }
        
        # Initialize processed data
        self.processed_data = {
            "image": None,
            "metadata": None
        }
    

    def process(self):

        file_path = self.parameters["file_path"]
        
        if not file_path or not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return False
        
        try:
            # Load the image
            if self.parameters["preserve_alpha"]:
                # Load with alpha channel if available
                image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            else:
                # Load without alpha channel
                image = cv2.imread(file_path, cv2.IMREAD_COLOR)
            
            if image is None:
                print(f"Error: Failed to load image: {file_path}")
                return False
            
            # Convert BGR to RGB (OpenCV loads as BGR)
            if len(image.shape) == 3 and image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            elif len(image.shape) == 3 and image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
            
            # Extract metadata
            height, width = image.shape[:2]
            channels = 1 if len(image.shape) == 2 else image.shape[2]
            file_size = os.path.getsize(file_path)
            file_extension = os.path.splitext(file_path)[1].lower()
            
            metadata = {
                "width": str(width) + " px",
                "height": str(height) + " px",
                "file_size": str(round(file_size/1024**2, 2)) + " MB" ,
                "file_format": file_extension[1:],
            }

            
            # Store the results
            self.processed_data["image"] = image
            self.processed_data["metadata"] = metadata
            
            # Mark as not dirty
            self.dirty = False
            
            return True
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return False
    
    def set_file_path(self, file_path):
        if os.path.exists(file_path):
            self.parameters["file_path"] = file_path
            self.dirty = True
            return True
        else:
            print(f"Warning: File does not exist: {file_path}")
            return False

    
