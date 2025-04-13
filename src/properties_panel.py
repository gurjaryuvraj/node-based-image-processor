from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLabel, 
                            QSlider, QComboBox, QPushButton, QDoubleSpinBox,
                            QSpinBox, QCheckBox, QColorDialog, QGroupBox,
                            QScrollArea, QSizePolicy, QHBoxLayout, QLineEdit, QMessageBox, QFileDialog, QPixmap, QImage)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor

class PropertiesPanel(QScrollArea):

    
    def __init__(self, node_graph, parent=None):
        super().__init__(parent)

        #bg color
        self.background_color = QColor(40, 40, 40)

        #store the node graph
        self.node_graph = node_graph

        #widget properties
        self.setWidgetResizable(True)
        self.setMinimumWidth(250)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        #content widget
        self.content_widget = QWidget()
        self.setWidget(self.content_widget)
        
        #layout
        self.layout = QVBoxLayout(self.content_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        #title
        self.title_label = QLabel("No Node Selected")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.layout.addWidget(self.title_label)

        #add node type label
        self.type_label = QLabel("")
        self.layout.addWidget(self.type_label)
        
        #separator
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        separator.setStyleSheet("background-color: #303030;")
        self.layout.addWidget(separator)
        
        # Add parameters group
        self.params_group = QGroupBox("Parameters")
        self.params_layout = QFormLayout(self.params_group)
        self.layout.addWidget(self.params_group)
        
        # Add inputs group
        self.inputs_group = QGroupBox("Inputs")
        self.inputs_layout = QFormLayout(self.inputs_group)
        self.layout.addWidget(self.inputs_group)
        
        # Add outputs group
        self.outputs_group = QGroupBox("Outputs")
        self.outputs_layout = QFormLayout(self.outputs_group)
        self.layout.addWidget(self.outputs_group)
        
        # Add spacer
        self.layout.addStretch()
        
        # Initialize state variables
        self.selected_node = None
        self.parameter_widgets = {}

    @pyqtSlot(str)
    def set_selected_node(self, node_id):

        #clear previous widgets
        self.clear_widgets()
        
        #update selected node
        self.selected_node = self.node_graph.nodes.get(node_id) if node_id else None
        
        if self.selected_node:
            #update title and type
            self.title_label.setText(self.selected_node.name)
            self.type_label.setText(f"Type: {self.selected_node.__class__.__name__}")
            
            #add parameter widgets
            self.add_parameter_widgets()
            
            #add input widgets
            self.add_input_widgets()
            
            #add output widgets
            self.add_output_widgets()
            
            # Show all groups
            self.params_group.show()
            self.inputs_group.show()
            self.outputs_group.show()
        else:
            # No node selected
            self.title_label.setText("No Node Selected")
            self.type_label.setText("")
            
            # Hide all groups
            self.params_group.hide()
            self.inputs_group.hide()
            self.outputs_group.hide()
    
    def clear_widgets(self):
        # Clear parameter widgets
        while self.params_layout.count():
            item = self.params_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Clear input widgets
        while self.inputs_layout.count():
            item = self.inputs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Clear output widgets
        while self.outputs_layout.count():
            item = self.outputs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Clear parameter widgets dictionary
        self.parameter_widgets = {}
    
    def add_parameter_widgets(self):
        """Add widgets for the selected node's parameters."""
        if not self.selected_node:
            return
        
        # Add widgets for each parameter
        for param_name, param_value in self.selected_node.parameters.items():
            # Create appropriate widget based on parameter type
            if param_value is not None and isinstance(param_value, np.ndarray):
                    # Create a container widget for the preview
                    preview_container = QWidget()
                    preview_layout = QVBoxLayout(preview_container)
                    preview_layout.setContentsMargins(0, 0, 0, 0)
                    
                    # Add label
                    preview_label = QLabel("Preview")
                    preview_label.setStyleSheet("font-weight: bold;")
                    preview_layout.addWidget(preview_label)
                    
                    # Convert numpy array to QPixmap
                    image_widget = QLabel()
                    qimage = self.numpy_to_qimage(param_value)
                    pixmap = QPixmap.fromImage(qimage)
                    
                    # Scale the pixmap if it's too large
                    max_size = 300
                    if pixmap.width() > max_size or pixmap.height() > max_size:
                        pixmap = pixmap.scaled(max_size, max_size, Qt.KeepAspectRatio)
                    
                    image_widget.setPixmap(pixmap)
                    preview_layout.addWidget(image_widget)
                    
                    self.params_layout.addRow(preview_container)
                    continue


            if isinstance(param_value, bool):
                widget = QCheckBox()
                widget.setChecked(param_value)
                widget.stateChanged.connect(
                    lambda state, name=param_name: self.on_parameter_changed(name, bool(state))
                )
            
            
            
            elif isinstance(param_value, str):
                # Special handling for specific parameters
                if param_name == "file_path":
                    widget = QWidget()
                    layout = QHBoxLayout(widget)
                    layout.setContentsMargins(0, 0, 0, 0)
                    
                    text_field = QLineEdit(param_value)
                    text_field.setReadOnly(True)
                    layout.addWidget(text_field)
                    
                    browse_button = QPushButton("Browse")
                    layout.addWidget(browse_button)
                    
                    if isinstance(self.selected_node, type) and self.selected_node.__name__ == "ImageInputNode":
                        browse_button.clicked.connect(self.browse_input_file)
                    else:
                        browse_button.clicked.connect(self.browse_input_file)
                elif param_name == "file_path_save":
                    widget = QWidget()
                    layout = QHBoxLayout(widget)
                    layout.setContentsMargins(0, 0, 0, 0)
                    

                    save_button = QPushButton("Save Result")
                    layout.addWidget(save_button)                 

                    if isinstance(self.selected_node, type) and self.selected_node.__name__ == "ImageOutputNode":
                        save_button.clicked.connect(self.save_result)
                    else:
                        save_button.clicked.connect(self.save_result)
                    
                                
                
                else:
                    widget = QLineEdit(param_value)
                    widget.textChanged.connect(
                        lambda text, name=param_name: self.on_parameter_changed(name, text)
                    )
            
            elif isinstance(param_value, int):
                widget = QSpinBox()
                widget.setRange(-1000, 1000)
                widget.setValue(param_value)
                widget.valueChanged.connect(
                    lambda value, name=param_name: self.on_parameter_changed(name, value)
                )
            
            
            
            else:
                # Generic handling for other parameter types
                widget = QLabel(str(param_value))
            
            # Add widget to layout
            self.params_layout.addRow(self.format_label(param_name), widget)
            
            # Store widget for later access
            self.parameter_widgets[param_name] = widget

        if self.selected_node.processed_data :
            if self.selected_node.processed_data["metadata"]:
                for metadata_name, metadata_value in self.selected_node.processed_data["metadata"].items():
                    
                    widget = QLabel(str(metadata_value))
                    self.params_layout.addRow(self.format_label(metadata_name), widget)
            else:
                if self.selected_node.parameters["file_path"]:
                    file_path = self.selected_node.parameters["file_path"]
                    import cv2
                    import os
                    image = cv2.imread(file_path)
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

                    self.selected_node.processed_data["image"] = image
                    self.selected_node.processed_data["metadata"] = metadata
                    for metadata_name, metadata_value in self.selected_node.processed_data["metadata"].items():
                        widget = QLabel(metadata_value)
                        self.params_layout.addRow(self.format_label(metadata_name), widget)


        



        

            
            
    
    def add_input_widgets(self):
        """Add widgets for the selected node's inputs."""
        if not self.selected_node:
            return
        
        # Add widgets for each input
        for input_name, connection in self.selected_node.inputs.items():
            if connection:
                source_node, output_name = connection
                label = QLabel(f"{source_node.name} → {output_name}")
                
                # Add disconnect button
                disconnect_button = QPushButton("Disconnect")
                disconnect_button.clicked.connect(
                    lambda _, name=input_name: self.disconnect_input(name)
                )
                
                # Create widget with label and button
                widget = QWidget()
                layout = QHBoxLayout(widget)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(label)
                layout.addWidget(disconnect_button)
            else:
                widget = QLabel("Not connected")
            
            # Add widget to layout
            self.inputs_layout.addRow(self.format_label(input_name), widget)
    
    def add_output_widgets(self):
        """Add widgets for the selected node's outputs."""
        if not self.selected_node:
            return
        
        # Add widgets for each output
        for output_name, output_type in self.selected_node.outputs.items():
            # Create label with output type
            widget = QLabel(output_type)
            
            # Add widget to layout
            self.outputs_layout.addRow(self.format_label(output_name), widget)

        
                
    def numpy_to_qimage(self, array):
        """Convert numpy array to QImage"""
        if array is None:
            return QImage()
        
        # Normalize to 0-255 if needed
        if array.dtype == np.float32 or array.dtype == np.float64:
            array = (array * 255).astype(np.uint8)
        
        # Handle different channel counts
        if len(array.shape) == 2:  # Grayscale
            height, width = array.shape
            bytes_per_line = width
            return QImage(array.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        elif array.shape[2] == 3:  # RGB
            height, width, _ = array.shape
            bytes_per_line = 3 * width
            return QImage(array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        elif array.shape[2] == 4:  # RGBA
            height, width, _ = array.shape
            bytes_per_line = 4 * width
            return QImage(array.data, width, height, bytes_per_line, QImage.Format_RGBA8888)
        else:
            return QImage()
    
    def format_label(self, name):
        """Format a parameter, input, or output name for display."""
        # Convert snake_case to Title Case with spaces
        return " ".join(word.capitalize() for word in name.split("_"))
    
    def on_parameter_changed(self, param_name, value):
        """
        Handle parameter value changes.
        
        Args:
            param_name: Name of the parameter
            value: New value for the parameter
        """
        if self.selected_node:
            # Update the parameter
            self.selected_node.set_parameter(param_name, value)
            
            # Mark the node as dirty
            self.selected_node.dirty = True
    
    def update_widget_value(self, param_name, value):
        """
        Update a widget's value without triggering signals.
        
        Args:
            param_name: Name of the parameter
            value: New value for the widget
        """
        if param_name in self.parameter_widgets:
            widget = self.parameter_widgets[param_name]
            
            # Update widget based on type
            if isinstance(widget, QSlider):
                widget.setValue(value)
            elif isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                widget.setValue(value)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(value)
            elif isinstance(widget, QComboBox):
                widget.setCurrentText(value)
            elif isinstance(widget, QLineEdit):
                widget.setText(value)
    
    def disconnect_input(self, input_name):
        """
        Disconnect an input connection.
        
        Args:
            input_name: Name of the input to disconnect
        """
        if self.selected_node:
            # Disconnect the input
            self.selected_node.disconnect_input(input_name)
            
            # Update the properties panel
            self.set_selected_node(self.selected_node.id)
    
    def browse_input_file(self):
        """Open a file dialog to browse for an input image file."""
        
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path and self.selected_node:
            # Set the file path
            self.selected_node.set_parameter("file_path", file_path)
            
            # Update the widget
            self.update_widget_value("file_path", file_path)
    
    def browse_output_file(self):
        """Open a file dialog to browse for an output image file."""
        
        
        file_path_save, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg);;BMP Files (*.bmp)"
        )
        
        if file_path_save and self.selected_node:
            # Set the file path
            self.selected_node.set_parameter("file_path_save", file_path_save)
            
            # Update the widget
            self.update_widget_value("file_path_save", file_path_save)
    
    def save_result(self):
        """Save the result of an Output Node."""
        # Find an Output Node
        output_nodes = [node for node in self.node_graph.nodes.values() 
                        if node.__class__.__name__ == "OutputNode"]
        
        if not output_nodes:
            QMessageBox.warning(
                self, "No Output Node", 
                "Please add an Output Node to save results."
            )
            return
        
        # Use the first Output Node
        output_node = output_nodes[0]
        
        # Open file dialog
        file_path_save, _ = QFileDialog.getSaveFileName(
            self, "Save Result", "", "PNG Files (*.png);;JPEG Files (*.jpg);;BMP Files (*.bmp)"
        )
        
        if file_path_save:
            # Set the file path
            output_node.set_parameter("file_path_save", file_path_save)
            
            # Determine format from file extension
            ext = file_path_save.split(".")[-1].lower()
            if ext in ["jpg", "jpeg"]:
                output_node.set_parameter("format", "jpg")
            elif ext == "png":
                output_node.set_parameter("format", "png")
            elif ext == "bmp":
                output_node.set_parameter("format", "bmp")
            
            if not output_node.process():
                QMessageBox.warning(
                    self, "Processing Failed", 
                    "Failed to process the node. Please check the connections."
                )
                return
            
            # Save the image
            success = output_node.save_image()
            
            if success:
                self.statusBar().showMessage(f"Saved result to: {file_path_save}")
            else:
                QMessageBox.warning(
                    self, "Save Failed", 
                    "Failed to save the result. Please check the connections and try again."
                )
        else:
            QMessageBox.warning(
                self, "Save Failed", 
                "path not defined"
            )
    
    
