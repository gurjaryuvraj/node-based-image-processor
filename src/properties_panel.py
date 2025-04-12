from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLabel, 
                            QSlider, QComboBox, QPushButton, QDoubleSpinBox,
                            QSpinBox, QCheckBox, QColorDialog, QGroupBox,
                            QScrollArea, QSizePolicy, QHBoxLayout, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor

class PropertiesPanel(QScrollArea):

    
    def __init__(self, node_graph, parent=None):
        super().__init__(parent)

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
        
        #separator
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        separator.setStyleSheet("background-color: #555555;")
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