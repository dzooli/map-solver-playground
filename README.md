# Map Solver Playground

A Python application for generating, visualizing, and manipulating 2D map data. This project provides tools for creating
terrain maps, applying filters, and visualizing the results using Pygame.

![Map Solver Playground Screenshot](screenshot.png)

## Features

- Generate terrain maps using various algorithms
- Apply filters to modify map data
- Visualize maps with customizable color gradients
- Interactive UI with keyboard and mouse controls
- Performance metrics for measuring execution time
- Place flags on the map to mark locations
- Map solver for location-based operations
    - Example solver with Flow-field algorithm
- Switch between original and small map views
- Modular map elements architecture
    - Abstract MapElement base class
    - Concrete implementations: Flag, GeoPath
    - Dedicated renderers for each element type
    - Clear separation of concerns:
        - MapElements manage their own data
        - Renderers handle visualization
        - MapView coordinates elements and renderers

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/map-solver-playground.git
cd map-solver-playground

# Install the package using uv (pip is deprecated)
uv pip install -e .
```

## Usage

Run the main application:

```bash
python -m map_solver_playground
```

### Controls

#### Keyboard

- `ESC`: Exit the application
- `N`: Generate a new map
- `S`: Solve a path between placed flags
- `V`: Switch between original and small map views
- `H`: Toggle path visibility
- `T`: Toggle tooltip visibility

#### Mouse

- **Left Click**: Place flags on the map (alternates between red and green flags)
    - First click places a red flag (start location)
    - Second click places a green flag (end location)
    - Subsequent clicks repeat this pattern

## Project Structure

```
map_solver_playground/
├── components/       # UI components
├── maps/             # Map data and manipulation
│   ├── elements/     # Map elements (Flag, GeoPath, etc.)
│   ├── filters/      # Map filters
│   ├── generators/   # Map generation algorithms
│   ├── renderers/    # Renderers for map elements
│   ├── solvers/      # Map solving algorithms
│   ├── types/        # Map data types
│   └── visualization/# Map visualization tools
└── metrics/          # Performance measurement utilities
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
