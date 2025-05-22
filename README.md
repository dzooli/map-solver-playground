# Map Solver Playground

A Python application for generating, visualizing, and manipulating 2D map data. This project provides tools for creating
terrain maps, applying filters, and visualizing the results using Pygame.

![Map Solver Playground Screenshot](screenshot.png)

## Features

- Generate terrain maps using various algorithms
- Apply filters to modify map data
- Visualize maps with customizable color gradients
- Modular UI elements architecture
    - All UI elements have a common parent: Widget
    - UI elements implemented:
        - TextPanel
            - StatusBar
            - ToolTipPanel
            - InfoPanel
        - MapView
- Interactive UI with keyboard and mouse controls
- Performance metrics for measuring execution time
- Place flags on the map to mark locations
- Map solver for location-based operations
    - Example solver with Flow-field algorithm
- Switch between original and small map views
- Modular map elements architecture
    - Abstract MapElement base class
    - Concrete implementations: Flag, GeoPath, Terrain
    - Dedicated renderers for each element type
    - Clear separation of concerns:
        - MapElements manage their own data
        - Renderers handle visualization
        - MapView coordinates elements and renderers

## Installation

```bash
# Clone the repository
git clone https://github.com/dzooli/map-solver-playground.git
cd map-solver-playground

# Install the package using pip
pip install -e .

# Or using uv (recommended)
uv sync
```

## Dependencies

This project requires Python 3.12 or higher and depends on the following packages:

- pygame >= 2.5.0
- numpy >= 1.24.0
- scipy == 1.15.3
- networkx == 3.4.2
- networkx-astar-path >= 1.0.1
- pydantic >= 2.0.0

Development dependencies:

- black[d] >= 25.1.0
- pytest-cov >= 6.1.1
- pytest-mock >= 3.14.0
- pytest-xdist >= 3.6.1

## Usage

Run the main application:

```bash
# Using the module
python -m map_solver_playground

# Or using the installed entry point
map-solver

# Run performance tests
map-solver-perftest
```

### Controls

#### Keyboard

- `Q`: Exit the application
- `N`: Generate a new map
- `S`: Solve a path between placed flags
- `V`: Switch between original and small map views
- `H`: Toggle path visibility
- `T`: Toggle tooltip visibility

#### Mouse

- **Left Click**: Place flags on the map (alternates between red and green flags)
    - First click places a red flag (start location)
    - Second click places a green flag (goal location)
    - Subsequent clicks repeat this pattern

## Project Structure

```
map_solver_playground/
├── asset_loader        # Asset loaders
├── assets              # Common assets
├── components/         # UI components
├── map/                # Map data and manipulation
│   ├── elements/       # Map elements (Flag, GeoPath, etc.)
│   ├── filters/        # Map filters
│   ├── generator/      # Map generation algorithms
│   ├── render/         # Rendering related functions and classes
│   │   ├── element     # Map element rendering
│   ├── solver/         # Map solving algorithms
│   ├── types/          # Map data types
└── profile/            # Performance measurement utilities
```

## Testing

### Unit and others

Unit testing is performed by PyTest. Just start it in the project root directory with `pytest`.

### Performance

A small script added to measure the MapView's performance:

```bash
map-solver-perftest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
