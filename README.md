# Node-Based Image Manipulation Interface

A Python application for image manipulation using a node-based interface. This project allows users to load images, process them through a series of connected nodes, and save the resulting output.

## Features

- **Node-based workflow**: Create complex image processing pipelines by connecting nodes
- **Real-time preview**: See the results of your operations immediately
- **Extensive node library**: 8 different node types for various image processing operations
- **Intuitive UI**: Easy-to-use interface for creating and connecting nodes
- **Error handling**: Proper detection of invalid connections and circular dependencies

## Node Types

### Basic Nodes
- **Image Input Node**: Load images from the file system
- **Output Node**: Save processed images to disk
- **Brightness/Contrast Node**: Adjust image brightness and contrast
- **Color Channel Splitter**: Split RGB/RGBA images into separate channels

### Intermediate Nodes
- **Blur Node**: Apply Gaussian blur with configurable radius
- **Threshold Node**: Convert to binary image based on threshold value
- **Edge Detection Node**: Implement Sobel and Canny edge detection
- **Blend Node**: Combine two images using different blend modes


## Installation

### Prerequisites
- Python 3.8 or higher
- PyQt5
- OpenCV
- NumPy
- NetworkX

### Setup
1. Clone the repository:
```
git clone https://github.com/yourusername/node-based-image-processor.git
cd node-based-image-processor
```

2. Install the required dependencies:
```
pip install numpy opencv-python-headless pillow PyQt5 networkx
```

3. Run the application:
```
python main.py
```

## Usage

### Creating Nodes
1. Use the "Node" menu to add nodes to the canvas
2. Each node type has specific inputs, outputs, and parameters

### Connecting Nodes
1. Click and drag from an output connector (right side) to an input connector (left side)
2. Connections define the flow of data between nodes

### Adjusting Parameters
1. Select a node to view its properties in the right panel
2. Adjust parameters to modify the node's behavior
3. Results update in real-time

### Processing Images
1. Start with an Image Input Node to load an image
2. Connect processing nodes to modify the image
3. Use an Output Node to save the result

## Architecture

The application follows an object-oriented design with these key components:

- **Node**: Base class for all node types
- **NodeGraph**: Manages the collection of nodes and their connections
- **NodeCanvas**: Visual representation of nodes and connections
- **PropertiesPanel**: UI for adjusting node parameters
- **MainWindow**: Main application window with menus and layout

The execution system processes nodes in the correct order based on their dependencies, avoiding redundant calculations by caching results.

## Development

### Project Structure
```
node_image_processor/
├── main.py                  # Application entry point
└── src/
   ├── node.py              # Base Node class
   ├── node_graph.py        # NodeGraph class
   ├── node_canvas.py       # Canvas for displaying nodes
   ├── properties_panel.py  # Panel for editing node properties
   ├── main_window.py       # Main application window
   └── nodes/               # Node implementations
       ├── basic/           # Basic nodes
       ├── intermediate/    # Intermediate nodes
       └── advanced/        # Advanced nodes

```

### Adding New Nodes
To add a new node type:
1. Create a new class that inherits from `Node`
2. Implement the `process()` method
3. Define inputs, outputs, and parameters
4. Add the node to the `NodeGraph.create_node()` method

