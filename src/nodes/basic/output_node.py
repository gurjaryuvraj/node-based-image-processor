import os
import cv2
import numpy as np
from src.node import Node

class OutputNode(Node):

    def __init__(self, name="Output", id=None):
        
        super().__init__(name, id)
        
        #inputs
        self.inputs = {
            "image": None  # Input image connection
        }
        
        #outputs
        self.outputs = {
            
        }
        
        #parameters
        self.parameters = {
            "file_path_save": "",  # Path to save the image
            "format": "png",
            "quality": 95,    # Quality for jpg format (0-100)
            "preview": None    # Preview of the final image
        }

    def process(self):
        """
        Process the input image and prepare for saving.
        
        Returns:
            bool: True if processing was successful, False otherwise
        """
        # Get input image
        input_image = self.get_input_data("image")
        
        if input_image is None:
            print("Error: No input image connected")
            return False
        
        # Store the preview
        self.parameters["preview"] = input_image
        
        # Mark as not dirty
        self.dirty = False
        
        return True
    
    def save_image(self):
        """
        Save the processed image to disk.
        
        Returns:
            bool: True if saving was successful, False otherwise
        """
        # Process if dirty
        if self.dirty:
            success = self.process()
            if not success:
                return False
        
        file_path = self.parameters["file_path_save"]
        if not file_path:
            print("Error: No file path specified")
            return False
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                print(f"Error creating directory: {str(e)}")
                return False
        
        # Get the image to save
        image = self.parameters.get("preview")
        if image is None:
            print("Error: No processed image available")
            return False
        
        try:
            # Convert to BGR for OpenCV
            if len(image.shape) == 3 and image.shape[2] == 3:
                save_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            elif len(image.shape) == 3 and image.shape[2] == 4:
                save_image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
            else:
                save_image = image
            
            # Save with appropriate format and quality
            format_lower = self.parameters["format"].lower()
            
            if format_lower == "jpg" or format_lower == "jpeg":
                quality = self.parameters["quality"]
                cv2.imwrite(file_path, save_image, [cv2.IMWRITE_JPEG_QUALITY, quality])
            elif format_lower == "png":
                cv2.imwrite(file_path, save_image, [cv2.IMWRITE_PNG_COMPRESSION, 9])
            elif format_lower == "bmp":
                cv2.imwrite(file_path, save_image)
            else:
                print(f"Error: Unsupported format: {format_lower}")
                return False
            
            print(f"Image saved successfully to: {file_path}")
            return True
            
        except Exception as e:
            print(f"Error saving image: {str(e)}")
            return False
    
    def set_file_path(self, file_path):
        """
        Set the file path for saving the image.
        
        Args:
            file_path (str): Path to save the image
        """
        self.parameters["file_path"] = file_path



