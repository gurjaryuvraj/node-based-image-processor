import sys
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPainterPath

class NodeCanvas(QWidget):

    #give signal when node selected
    node_selected = pyqtSignal(str)
    
    def __init__(self, node_graph, parent=None):
        super().__init__(parent)

        #store the node graph
        self.node_graph = node_graph
        
        #set widget properties
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        
        #initialize state variables
        self.selected_node_id = None
        self.dragging_node = False
        self.drag_start_pos = None
        self.node_start_pos = None
        self.creating_connection = False
        self.connection_start_node = None
        self.connection_start_output = None
        self.connection_end_pos = None
        
        #node appearance 
        self.node_width = 180
        self.node_header_height = 30
        self.node_content_height = 100
        self.node_corner_radius = 5
        self.node_title_font_size = 10
        self.connector_radius = 8
        self.connector_spacing = 20
        
        #colors
        self.background_color = QColor(29, 29, 29)
        self.grid_color = QColor(80, 80, 80)
        self.node_color = QColor(100, 100, 100)
        self.node_selected_color = QColor(120, 120, 180)
        self.node_header_color = QColor(80, 80, 80)
        self.node_title_color = QColor(220, 220, 220)
        self.connector_color = QColor(180, 180, 180)
        self.connector_hover_color = QColor(220, 220, 220)
        self.connection_color = QColor(200, 200, 200)
        
        #initialize hover state
        self.hover_node_id = None
        self.hover_connector = None  


    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.fillRect(self.rect(), self.background_color)
        
        self._draw_connections(painter)
        
        #temporary connection if creating one
        if self.creating_connection and self.connection_start_node and self.connection_end_pos:
            self._draw_temp_connection(painter)
        
        for node_id, node in self.node_graph.nodes.items():
            self._draw_node(painter, node)
    
    
    def _draw_connections(self, painter):
        painter.setPen(QPen(self.connection_color, 2))
        
        for node_id, node in self.node_graph.nodes.items():
            for input_name, connection in node.inputs.items():
                if connection:
                    source_node, output_name = connection
                    
                    #connector positions
                    start_pos = self._get_output_connector_pos(source_node, output_name)
                    end_pos = self._get_input_connector_pos(node, input_name)
                    
                    #draw bezier curve
                    path = QPainterPath()
                    path.moveTo(start_pos)
                    
                    ctrl1_x = start_pos.x() + 100
                    ctrl1_y = start_pos.y()
                    ctrl2_x = end_pos.x() - 100
                    ctrl2_y = end_pos.y()
                    
                    path.cubicTo(
                        QPointF(ctrl1_x, ctrl1_y),
                        QPointF(ctrl2_x, ctrl2_y),
                        end_pos
                    )
                    
                    painter.drawPath(path)
    
    def _draw_temp_connection(self, painter):
        #set pen for temporary connection
        painter.setPen(QPen(self.connection_color, 2, Qt.DashLine))
        
        #get start position
        start_pos = self._get_output_connector_pos(
            self.node_graph.nodes[self.connection_start_node],
            self.connection_start_output
        )
        
        #draw bezier curve
        path = QPainterPath()
        path.moveTo(start_pos)
        
        ctrl1_x = start_pos.x() + 100
        ctrl1_y = start_pos.y()
        ctrl2_x = self.connection_end_pos.x() - 100
        ctrl2_y = self.connection_end_pos.y()
        
        path.cubicTo(
            QPointF(ctrl1_x, ctrl1_y),
            QPointF(ctrl2_x, ctrl2_y),
            self.connection_end_pos
        )
        
        painter.drawPath(path)
    
    def _draw_node(self, painter, node):
        x, y = node.position
        
        is_selected = (node.id == self.selected_node_id)
        
        #set node color based on selection state
        if is_selected:
            node_color = self.node_selected_color
        else:
            node_color = self.node_color
        
        #draw node background
        node_rect = QRectF(
            x, y, 
            self.node_width, 
            self.node_header_height + 20 + (max(len(node.outputs), len(node.inputs))) * 25
        )
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(node_color))
        painter.drawRoundedRect(
            node_rect, 
            self.node_corner_radius, 
            self.node_corner_radius
        )
        
        #draw node header
        header_rect = QRectF(
            x, y, 
            self.node_width, 
            self.node_header_height
        )
        
        painter.setBrush(QBrush(self.node_header_color))
        painter.drawRoundedRect(
            header_rect, 
            self.node_corner_radius, 
            self.node_corner_radius
        )
        
        #draw node title
        painter.setPen(QPen(self.node_title_color))
        painter.setFont(painter.font())
        painter.drawText(
            header_rect.adjusted(10, 0, -10, 0),
            Qt.AlignVCenter | Qt.AlignLeft,
            node.name
        )
        
        #draw input connectors
        y_offset = self.node_header_height + 20
        for input_name in node.inputs.keys():
            #determine if connector is hovered
            is_hovered = (
                self.hover_connector and 
                self.hover_connector[0] == node.id and
                self.hover_connector[1] == input_name and
                self.hover_connector[2] == True
            )
            
            #set connector color
            if is_hovered:
                connector_color = self.connector_hover_color
            else:
                connector_color = self.connector_color
            
            #draw connector
            connector_pos = QPointF(x, y + y_offset)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(connector_color))
            painter.drawEllipse(
                int(connector_pos.x() - self.connector_radius / 2),
                int(connector_pos.y() - self.connector_radius / 2),
                int(self.connector_radius),
                int(self.connector_radius)
            )
            
            #draw connector label
            painter.setPen(QPen(self.node_title_color))
            painter.drawText(
                QRectF(
                    x + 10, 
                    y + y_offset - 10, 
                    self.node_width - 20, 
                    20
                ),
                Qt.AlignVCenter | Qt.AlignLeft,
                input_name
            )
            
            y_offset += self.connector_spacing
        
        #draw output connectors
        y_offset = self.node_header_height + 20
        for output_name in node.outputs.keys():
            #determine if connector is hovered
            is_hovered = (
                self.hover_connector and 
                self.hover_connector[0] == node.id and
                self.hover_connector[1] == output_name and
                self.hover_connector[2] == False
            )
            
            #set connector color
            if is_hovered:
                connector_color = self.connector_hover_color
            else:
                connector_color = self.connector_color
            
            #draw connector
            connector_pos = QPointF(x + self.node_width, y + y_offset)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(connector_color))
            painter.drawEllipse(
                int(connector_pos.x() - self.connector_radius / 2),
                int(connector_pos.y() - self.connector_radius / 2),
                int(self.connector_radius),
                int(self.connector_radius)
            )
            
            #draw connector label
            painter.setPen(QPen(self.node_title_color))
            painter.drawText(
                QRectF(
                    x + 10, 
                    y + y_offset - 10, 
                    self.node_width - 20, 
                    20
                ),
                Qt.AlignVCenter | Qt.AlignRight,
                output_name
            )
            
            y_offset += self.connector_spacing
    
    def _get_input_connector_pos(self, node, input_name):
        x, y = node.position
        
        #find the index of the input
        input_names = list(node.inputs.keys())
        if input_name in input_names:
            index = input_names.index(input_name)
            y_offset = self.node_header_height + 20 + index * self.connector_spacing
            return QPointF(x, y + y_offset)
        
        return QPointF(x, y)
    
    def _get_output_connector_pos(self, node, output_name):
        x, y = node.position
        
        #find the index of the output
        output_names = list(node.outputs.keys())
        if output_name in output_names:
            index = output_names.index(output_name)
            y_offset = self.node_header_height + 20 + index * self.connector_spacing
            return QPointF(x + self.node_width, y + y_offset)
        
        return QPointF(x + self.node_width, y)
    
    def _get_node_at_pos(self, pos):
        for node_id, node in self.node_graph.nodes.items():
            x, y = node.position
            node_rect = QRectF(
                x, y, 
                self.node_width, 
                self.node_header_height + self.node_content_height
            )
            
            if node_rect.contains(pos):
                return node_id
        
        return None
    
    def _get_connector_at_pos(self, pos):
        for node_id, node in self.node_graph.nodes.items():
            for input_name in node.inputs.keys():
                connector_pos = self._get_input_connector_pos(node, input_name)
                
                #check if position is within connector radius
                if (pos - connector_pos).manhattanLength() <= self.connector_radius:
                    return (node_id, input_name, True)  
            
            #check output connectors
            for output_name in node.outputs.keys():
                connector_pos = self._get_output_connector_pos(node, output_name)
                
                #check if position is within connector radius
                if (pos - connector_pos).manhattanLength() <= self.connector_radius:
                    return (node_id, output_name, False)  # False for output
        
        return None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            
            #check if clicked on a connector
            connector = self._get_connector_at_pos(pos)
            if connector:
                node_id, connector_name, is_input = connector
                
                if is_input:
                    #clicked on an input connector
                    #disconnect the input
                    node = self.node_graph.nodes[node_id]
                    node.disconnect_input(connector_name)
                    self.update()
                else:
                    #clicked on an output connector
                    #start creating a connection
                    self.creating_connection = True
                    self.connection_start_node = node_id
                    self.connection_start_output = connector_name
                    self.connection_end_pos = pos
                    self.update()
            else:
                node_id = self._get_node_at_pos(pos)
                if node_id:
                    self.select_node(node_id)
                    
                    #start dragging the node
                    self.dragging_node = True
                    self.drag_start_pos = pos
                    self.node_start_pos = self.node_graph.nodes[node_id].position
                else:
                    #clicked on empty space, deselect
                    self.select_node(None)
    
    def mouseMoveEvent(self, event):
        pos = event.pos()
        
        #update hover state
        self.hover_connector = self._get_connector_at_pos(pos)
        self.hover_node_id = self._get_node_at_pos(pos)
        
        if self.dragging_node and self.selected_node_id:
            #calculate new position
            delta_x = pos.x() - self.drag_start_pos.x()
            delta_y = pos.y() - self.drag_start_pos.y()
            
            new_x = self.node_start_pos[0] + delta_x
            new_y = self.node_start_pos[1] + delta_y
            
            #udate node position
            self.node_graph.nodes[self.selected_node_id].set_position(new_x, new_y)
            
            #update canvas
            self.update()
        
        #handle creating connection
        if self.creating_connection:
            self.connection_end_pos = pos
            self.update()
        
        #update cursor
        if self.hover_connector or self.creating_connection:
            self.setCursor(Qt.CrossCursor)
        elif self.dragging_node:
            self.setCursor(Qt.ClosedHandCursor)
        elif self.hover_node_id:
            self.setCursor(Qt.OpenHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            #end dragging node
            self.dragging_node = False
            
            # ed creating connection
            if self.creating_connection:
                #check if released on an input connector
                connector = self._get_connector_at_pos(event.pos())
                if connector:
                    node_id, connector_name, is_input = connector
                    
                    if is_input:
                        #connect the nodes
                        target_node = self.node_graph.nodes[node_id]
                        source_node = self.node_graph.nodes[self.connection_start_node]
                        
                        target_node.connect_input(
                            connector_name, 
                            source_node, 
                            self.connection_start_output
                        )
                
                #reset connection state
                self.creating_connection = False
                self.connection_start_node = None
                self.connection_start_output = None
                self.connection_end_pos = None
                
                self.update()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete and self.selected_node_id:
            self.node_graph.remove_node(self.selected_node_id)
            self.selected_node_id = None
            self.update()
    
    def select_node(self, node_id):
        if self.selected_node_id != node_id:
            self.selected_node_id = node_id
            self.node_selected.emit(node_id)
            self.update()


