import sys
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPainterPath

class NodeCanvas(QWidget):
    
    def __init__(self, node_graph, parent=None):
        super().__init__(parent)

        
        #widget properties
        self.setMinimumSize(800, 600)
        
        
        #colors
        self.background_color = QColor(60, 60, 60)
        self.grid_color = QColor(80, 80, 80)

