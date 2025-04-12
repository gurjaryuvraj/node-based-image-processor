import uuid
import numpy as np

class Node:
    
    def __init__(self, name, id=None):

        self.id = id or str(uuid.uuid4())
        self.name = name
        self.inputs = {}  # dictionary of input connections 
        self.outputs = {}  # dictionary of output 
        self.parameters = {}  # node parameters
