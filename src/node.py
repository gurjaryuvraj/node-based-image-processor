import uuid
import numpy as np

class Node:
    
    def __init__(self, name, id=None):

        self.id = id or str(uuid.uuid4())
        self.name = name
        self.inputs = {}  # dictionary of input connections 
        self.outputs = {}  # dictionary of output 
        self.parameters = {}  # node parameters
        self.position = (0, 0)  # Position on canvas
        self.processed_data = {}  # Cache for processed results {output_name: data}
        self.dirty = True  # Flag to indicate if reprocessing is needed
    
    def process(self):
        raise NotImplementedError(
            f"Node class {self.__class__.__name__} must implement process() method"
        )
    
    def connect_input(self, input_name, source_node, output_name):
        
        if input_name not in self.inputs:
            print(f"Error: Node {self.name} has no input named {input_name}")
            return False
            
        if output_name not in source_node.outputs:
            print(f"Error: Node {source_node.name} has no output named {output_name}")
            return False
            
            
        self.inputs[input_name] = (source_node, output_name)
        self.dirty = True
        return True
        
    
    def disconnect_input(self, input_name):

        if input_name in self.inputs:
            self.inputs[input_name] = None
            self.dirty = True
            return True
        return False
    
    def get_input_data(self, input_name):
        
        if input_name not in self.inputs or self.inputs[input_name] is None:
            return None
            
        source_node, output_name = self.inputs[input_name]
        
        # If the source node is dirty, process it first
        if source_node.dirty:
            success = source_node.process()
            if not success:
                return None
        
        # Return the processed data from the source node
        if output_name in source_node.processed_data:
            return source_node.processed_data[output_name]
        return None
    
    def get_output(self, output_name):
        
        if self.dirty:
            self.process(self)
            
        if output_name in self.processed_data:
            return self.processed_data[output_name]
        return None
    
    def set_parameter(self, param_name, value):
        
        if param_name in self.parameters:
            self.parameters[param_name] = value
            self.dirty = True
            return True
        return False
    
    def get_parameter(self, param_name):
        
        return self.parameters.get(param_name, None)
    
    def set_position(self, x, y):
        
        self.position = (x, y)
    
    def clear_cache(self):
        self.processed_data = {}
        self.dirty = True

