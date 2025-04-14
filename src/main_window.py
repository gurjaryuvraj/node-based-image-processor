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

        #menu bar
        self.create_menu_bar()
        
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

        #connect signals
        self.canvas.node_selected.connect(self.properties_panel.set_selected_node)

        self.show()

    def create_menu_bar(self):
        #file menu
        file_menu = self.menuBar().addMenu("File")
        
        #new action
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        #open action
        open_action = QAction("Open Image", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)
        
        #save action
        save_action = QAction("Save Result", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_result)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        #exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        #edit menu
        edit_menu = self.menuBar().addMenu("Edit")
        
        #delete node action
        delete_action = QAction("Delete Node", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.delete_selected_node)
        edit_menu.addAction(delete_action)
        
        #node menu
        node_menu = self.menuBar().addMenu("Node")
        
        #basic nodes submenu
        basic_menu = node_menu.addMenu("Basic Nodes")
        
        #add Image Input Node action
        add_input_action = QAction("Image Input", self)
        add_input_action.triggered.connect(lambda: self.add_node("image_input"))
        basic_menu.addAction(add_input_action)
        
        #add Output Node action
        add_output_action = QAction("Output", self)
        add_output_action.triggered.connect(lambda: self.add_node("output"))
        basic_menu.addAction(add_output_action)
        
        #intermediate nodes submenu
        intermediate_menu = node_menu.addMenu("Intermediate Nodes")
        
        #advanced nodes submenu
        advanced_menu = node_menu.addMenu("Advanced Nodes")
        
        #help menu
        help_menu = self.menuBar().addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def new_project(self):
        if len(self.node_graph.nodes) > 0:
            reply = QMessageBox.question(
                self, "New Project", 
                "Are you sure you want to create a new project? All unsaved changes will be lost.",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                return
            
        self.node_graph.clear()
        self.canvas.update()
        self.properties_panel.set_selected_node(None)
        self.statusBar().showMessage("New project created")
    
    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            node = self.node_graph.create_node("image_input")
            node.set_parameter("file_path", file_path)
            node.set_position(100, 100)
            self.canvas.update()
            self.canvas.select_node(node.id)
            self.statusBar().showMessage(f"Opened image: {file_path}")


    def save_result(self):
        output_nodes = [node for node in self.node_graph.nodes.values() 
                        if node.__class__.__name__ == "OutputNode"]
        
        if not output_nodes:
            QMessageBox.warning(
                self, "No Output Node", 
                "Please add an Output Node to save results."
            )
            return
        
        output_node = output_nodes[0]
        
        file_path_save, _ = QFileDialog.getSaveFileName(
            self, "Save Result", "", "PNG Files (*.png);;JPEG Files (*.jpg);;BMP Files (*.bmp)"
        )
        
        if file_path_save:
            output_node.set_parameter("file_path_save", file_path_save)
            
            ext = file_path_save.split(".")[-1].lower()
            if ext in ["jpg", "jpeg"]:
                output_node.set_parameter("format", "jpg")
            elif ext == "png":
                output_node.set_parameter("format", "png")
            elif ext == "bmp":
                output_node.set_parameter("format", "bmp")
            
            output_node.process()
            success = output_node.save_image()
            
            if success:
                msg = QMessageBox()
                msg.setText(f"Saved result to: {file_path_save_save}")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
            else:
                QMessageBox.warning(
                    self, "Save Failed", 
                    "Failed to save the result. Please check the connections and try again."
                )
    
    def add_node(self, node_type):
        #create the node
        node = self.node_graph.create_node(node_type)
        
        if node:
            canvas_center = self.canvas.rect().center()
            node.set_position(canvas_center.x(), canvas_center.y())
            self.canvas.update()
            self.canvas.select_node(node.id)
            self.statusBar().showMessage(f"Added {node.name} node")
    
    def delete_selected_node(self):
        selected_node_id = self.canvas.selected_node_id
        
        if selected_node_id:
            self.node_graph.remove_node(selected_node_id)
            self.canvas.update()
            self.canvas.select_node(None)
            self.statusBar().showMessage("Node deleted")
    
    def show_about(self):
        QMessageBox.about(
            self, "About Node-Based Image Processor",
            "Node-Based Image Processor\n\n"
            "Created by Yuvraj."
        )

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()