import networkx as nx
from src.nodes.basic.input_node import InputNode
from src.nodes.basic.output_node import OutputNode

class NodeGraph:
    
    def __init__(self):
        self.nodes = {} 
        self.execution_order = []
    
    def add_node(self, node):
        
        if node.id in self.nodes:
            print(f"Error: Node with ID {node.id} already exists")
            return False
        
        self.nodes[node.id] = node
        self.update_execution_order()
        return True
    
    def remove_node(self, node_id):
        
        if node_id not in self.nodes:
            print(f"Error: Node with ID {node_id} does not exist")
            return False
        
        
        del self.nodes[node_id]
        self.update_execution_order()
        return True
    
    def connect_nodes(self, source_node_id, output_name, target_node_id, input_name):
        
        if source_node_id not in self.nodes:
            print(f"Error: Source node with ID {source_node_id} does not exist")
            return False
        
        if target_node_id not in self.nodes:
            print(f"Error: Target node with ID {target_node_id} does not exist")
            return False
        
        source_node = self.nodes[source_node_id]
        target_node = self.nodes[target_node_id]
        
        
        success = target_node.connect_input(input_name, source_node, output_name)
        
        if success:
            self.update_execution_order()
        
        return success
    
    def disconnect_nodes(self, target_node_id, input_name):
       
        if target_node_id not in self.nodes:
            print(f"Error: Target node with ID {target_node_id} does not exist")
            return False
        
        target_node = self.nodes[target_node_id]
        success = target_node.disconnect_input(input_name)
        
        if success:
            self.update_execution_order()
        
        return success
    
    def update_execution_order(self):
        try:
            graph = nx.DiGraph()
            
            for node_id in self.nodes:
                graph.add_node(node_id)
            
            for node_id, node in self.nodes.items():
                for input_name, connection in node.inputs.items():
                    if connection:
                        source_node, _ = connection
                        graph.add_edge(source_node.id, node_id)
            
            self.execution_order = list(nx.topological_sort(graph))
            return True
            
        except nx.NetworkXUnfeasible:
            print("Error: Graph contains a cycle")
            self.execution_order = []
            return False
    
    
    def execute(self, output_node_id=None):
        
        if not self.execution_order:
            self.update_execution_order()
            
            if not self.execution_order:
                print("Error: Failed to determine execution order")
                return False
        
        if output_node_id:
            if output_node_id not in self.nodes:
                print(f"Error: Output node with ID {output_node_id} does not exist")
                return False
            
            return self.nodes[output_node_id].process()
        else:
            success = True
            for node_id in self.execution_order:
                if not self.nodes[node_id].process():
                    success = False
            
            return success
    
    def clear(self):

        self.nodes = {}
        self.execution_order = []
    
    def create_node(self, node_type):
        
        try:
            if node_type == "image_input":
                node = InputNode()
            elif node_type == "output":
                node = OutputNode()
            else:
                print(f"Error: Unknown node type: {node_type}")
                return None
            
            self.add_node(node)
            
            return node
            
        except Exception as e:
            print(f"Error creating node: {str(e)}")
            return None
