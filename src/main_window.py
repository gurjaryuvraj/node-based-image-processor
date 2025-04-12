import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QSplitter, QAction, QFileDialog, 
                            QDockWidget, QScrollArea, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

from src.node_graph import NodeGraph
from src.node_canvas import NodeCanvas
from src.properties_panel import PropertiesPanel


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.node_graph = NodeGraph()
        self.init_ui()
    
    def init_ui(self):

        self.setWindowTitle("Node Based Image Processor")
        self.setGeometry(100, 100, 1200, 800)
        
        #main window and divider horizontal divider
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        splitter = QSplitter(Qt.Horizontal)
        
        # main canvas where nodes will be present
        self.canvas = NodeCanvas(self.node_graph)
        canvas_scroll = QScrollArea()
        canvas_scroll.setWidget(self.canvas)
        canvas_scroll.setWidgetResizable(True)
        splitter.addWidget(canvas_scroll)
        
        # panel to change properties if nodes
        self.properties_panel = PropertiesPanel(self.node_graph)
        properties_dock = QDockWidget("Properties")
        properties_dock.setWidget(self.properties_panel)
        properties_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.addDockWidget(Qt.RightDockWidgetArea, properties_dock)
        
        main_layout.addWidget(splitter)
        self.statusBar().showMessage("Ready")
        self.show()

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()