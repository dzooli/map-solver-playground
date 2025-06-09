"""
This script creates a simple map viewer application with keyboard controls.
"""

import logging
from typing import Dict, Any, Optional

# Import backend-independent utilities
from map_solver_playground.asset_loader.backend_independent_image_loader import load_image_with_transparency
from map_solver_playground.map.render.color_utils import get_color
from map_solver_playground.components import StatusBar, InfoPanel, ToolTipPanel, MapView
from map_solver_playground.constants import DEFAULT_MAP_SIZE, DEFAULT_BLOCKS
from map_solver_playground.map.generator import MapGeneratorFactory, MapGenerator
from map_solver_playground.map.render.color_maps import ColorGradient, TerrainColorGradient
from map_solver_playground.map.render.element.renderer_factory import RendererFactory, RendererBackend
from map_solver_playground.map.solver import MapSolverFactory, MapSolver
from map_solver_playground.map.types import Terrain
from map_solver_playground.profile import measure_time

logger: logging.Logger = logging.getLogger("mapsolver")
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture the timing logs
logger.propagate = False  # Prevent propagation to the root logger to avoid duplicate logs

# Remove any existing handlers to avoid duplicate logging
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

# Default solver to use for pathfinding
DEFAULT_SOLVER = "FlowFieldSolver"
MAP_SIZE = 600


class MapSolverApp:

    def __init__(
        self,
        width: int = 900,
        height: int = 900,
        map_size: int = MAP_SIZE,
        block_size: int = 30,
        colormap: TerrainColorGradient = None,
        generator: str = "RecursiveDiamondSquareGenerator",
        renderer_backend: RendererBackend = RendererBackend.PYGAME,
    ):
        self.tooltips = [
            "LMB to place a flag",
            "Press 'N' to generate a new map",
            "Press 'V' to view the small map",
            "Press 'S' solve the map",
            "Press 'H' to toggle path visibility",
            'Press "T" to toggle the tooltips',
            "Press 'Q' to exit",
        ]

        self._generator_name = generator
        self.map_generator = MapGeneratorFactory.create(self._generator_name, width=map_size, height=map_size)

        # Set the renderer backend
        RendererFactory.set_backend(renderer_backend)

        # Initialize the renderer
        renderer = RendererFactory.get_current_renderer()
        renderer.init()

        self.width, self.height = width, height

        # Create the window and screen/renderer
        self.window, self.screen = renderer.create_window(self.width, self.height, "Map Generator Demo")

        # Create the font
        self.font = renderer.create_font(size=24)

        # Use the global logger instead of storing a separate reference
        self._logger = logger

        # Status bar for displaying messages
        self.status_bar = StatusBar(self.screen, self.width, self.height, self.font)
        # Info panel for displaying map information
        self.info_panel = InfoPanel(self.screen, self.width, self.height, self.font)
        # Tooltip panel for displaying instructions
        self.tooltip_panel = ToolTipPanel(self.screen, self.width, self.height, self.font)
        self.tooltip_panel.set_text(self.tooltips)

        # Initialize the terrain
        self.colormap: TerrainColorGradient = ColorGradient.TOPO_COLORS if colormap is None else colormap
        terrain = Terrain(visible=True, map_size=map_size, block_size=block_size, colormap=self.colormap)

        # Create the map view component
        # Position it at the center of the screen
        map_view_x = self.width // 2 - map_size // 2
        # logger.debug(f"Tooltip panel height: {self.tooltip_panel.size[1]}")
        map_view_y = self.height // 2 - map_size // 2 - self.tooltip_panel.size[1] // 2
        self.map_view = MapView(
            self.screen, self.width, self.height, terrain, map_size, block_size, self.colormap, map_view_x, map_view_y
        )

        # Add map elements to the map view
        from map_solver_playground.map.types import Flag, GeoPath

        self.map_view.add_element("red_flag", Flag(None, None, "red", True))
        self.map_view.add_element("green_flag", Flag(None, None, "green", True))
        self.map_view.add_element("geo_path", GeoPath(None, (0, 0, 255), 2, True))

        # Widgets all in one
        self.widgets = [self.map_view, self.status_bar, self.info_panel, self.tooltip_panel]

        self.resources: Dict[str, Any] = {}
        self.load_resources()

        # Main loop control
        self.running = True

        # Mouse click tracking
        self.click_count = 0
        self.red_flag_pos = None
        self.green_flag_pos = None

        # Path solving
        self.path = None
        self.path_visible = True

        # Create initial map
        self.create_maps(self.colormap)

    @measure_time(logger_instance=logger)
    def load_resources(self) -> None:
        """Load resources like images and sounds"""
        for sprite_name in ["redflag001.png", "greenflag001.png"]:
            self.resources[f"img_{sprite_name.split('.')[0]}"] = load_image_with_transparency(
                sprite_name, target_size=(30, 30)
            )

        # Set flag images directly on the Flag objects
        red_flag = self.map_view.get_element("red_flag")
        green_flag = self.map_view.get_element("green_flag")
        red_flag.image = self.resources["img_redflag001"]
        green_flag.image = self.resources["img_greenflag001"]

    @measure_time(logger_instance=logger)
    def create_maps(self, colors: TerrainColorGradient = None, generator: Optional[MapGenerator] = None):
        """
        Create and render a map with the specified color gradient.

        Args:
            colors: The color gradient to use for map render, defaults to self.colormap
            generator: The map generator to use for map generation
        """
        # Use the current colormap if none is provided
        colors_to_use = self.colormap if colors is None else colors

        if colors_to_use is None:
            raise ValueError("Color map must be provided")

        # Get the current renderer backend
        current_backend = RendererFactory.get_current_backend()

        # Get the terrain element and create maps with the current backend
        terrain = self.map_view.get_element("terrain")
        terrain.create_maps(colors_to_use, generator, current_backend)

        # Set the view to show the original map
        self.map_view.set_view(0)

    @measure_time(logger_instance=logger)
    def solve_path(self, solver: MapSolver = None) -> None:
        """Solve the path from a red flag to the green flag using the default solver"""
        if self.red_flag_pos is None or self.green_flag_pos is None:
            self.status_bar.set_text("Cannot solve path: Both red and green flags must be placed")
            return

        self.status_bar.set_text("Solving path...")
        # Solve the path
        self.path = solver.solve()
        self.status_bar.set_text("Path solved")
        logger.debug("Path solved")

    def handle_events(self) -> dict[int, int]:
        """Handle events and track event occurrences."""
        events = {}

        # Get the current renderer
        renderer = RendererFactory.get_current_renderer()

        # Get all events
        for event in renderer.get_events():
            events.update({event.type: events.get(event.type, 0) + 1})

            # Handle quit events
            if renderer.is_quit_event(event):
                self.running = False

            # Handle key down events
            elif renderer.is_keydown_event(event):
                key = renderer.get_key_from_event(event)
                self._handle_key_press(key)

            # Handle mouse button down events
            elif renderer.is_mouse_button_down_event(event):
                if renderer.is_left_mouse_button(event):
                    pos = renderer.get_mouse_pos_from_event(event)
                    self._handle_mouse_click(pos)

        return events

    def _handle_key_press(self, key):
        """Handle single key press events"""
        # Get the current renderer
        renderer = RendererFactory.get_current_renderer()

        # Map the key to a key name
        key_name = renderer.handle_key_press(key)

        # Handle the key press based on the key name
        if key_name == "q":
            self.running = False
        elif key_name == "n":
            self._handle_new_map()
        elif key_name == "s":
            # S: Solve a path
            self._handle_solve_path()
        elif key_name == "h":
            # H: Toggle path visibility
            self._handle_toggle_path_visibility()
        elif key_name == "v":
            # V: Switch view
            self._handle_view_switch()
        elif key_name == "t":
            # T: Toggle tooltip
            self._handle_tooltip_toggle()

    def _handle_new_map(self):
        """Generate a new map"""
        self.status_bar.set_text("Generating a new map...")
        self.status_bar.draw()
        if self.map_view.current_view == 1:
            self.map_view.switch_view()

        # Get the current renderer backend
        current_backend = RendererFactory.get_current_backend()
        # Clear the terrain texture cache in a renderer-agnostic way
        from map_solver_playground.map.render.element.element_renderer_factory import ElementRendererFactory

        ElementRendererFactory.clear_terrain_texture_cache(current_backend)

        self.create_maps(None)  # Use the current colormap from MapView
        # Reset flags and click counter when a new map is generated
        self.red_flag_pos = None
        self.green_flag_pos = None

        # Reset flag positions directly on the Flag objects
        red_flag = self.map_view.get_element("red_flag")
        green_flag = self.map_view.get_element("green_flag")
        red_flag.position = None
        green_flag.position = None

        # Clear any existing path
        self.path = None

        # Get the geo path element and clear its points
        geo_path = self.map_view.get_element("geo_path")
        geo_path.clear_points()
        geo_path.visible = True

        # Update the path_visible property for backward compatibility
        self.path_visible = True

        self.click_count = 0
        self.status_bar.set_text("New map created")

    def _handle_view_switch(self):
        """Switch between original and small map views"""
        message = self.map_view.switch_view()
        self.status_bar.set_text(message)
        self._update_info_panel()

    def _handle_tooltip_toggle(self):
        """Toggle the visibility of the tooltip panel"""
        self.tooltip_panel.toggle_visibility()

    def _handle_solve_path(self):
        """Solve the path from the red flag to the green flag using the default solver"""
        if self.red_flag_pos is None or self.green_flag_pos is None:
            self.status_bar.set_text("Cannot solve path: Both red and green flags must be placed")
            return

        try:
            # Get the map from the map view
            map_obj = self.map_view.map

            # Create a solver instance
            logger.debug(f"Creating solver: {DEFAULT_SOLVER}")
            solver = MapSolverFactory.create(
                DEFAULT_SOLVER, map_obj=map_obj, start_location=self.red_flag_pos, end_location=self.green_flag_pos
            )
            logger.debug(f"Solver created: {solver}")

            self.solve_path(solver)

            if self.path:
                # Get the geo path element and update its properties
                geo_path = self.map_view.get_element("geo_path")
                geo_path.path_points = self.path
                geo_path.color = get_color("blue")  # Use backend-independent color utility
                geo_path.visible = True

                # Update properties for backward compatibility
                self.path_visible = True
                self.status_bar.set_text(f"Path solved using {solver.__class__.__name__}")
            else:
                self.status_bar.set_text("No path found between the flags")
        except Exception as e:
            self.status_bar.set_text(f"Error solving path: {str(e)}")
            self._logger.error(f"Error solving path: {str(e)}")

    def _handle_toggle_path_visibility(self):
        """Toggle the visibility of the path"""
        if self.path is None:
            self.status_bar.set_text("No path to show/hide")
            return

        # Get the geo path element and toggle its visibility
        geo_path = self.map_view.get_element("geo_path")
        geo_path.toggle_visibility()

        # Update the path_visible property for backward compatibility
        self.path_visible = geo_path.visible

        status = "shown" if self.path_visible else "hidden"
        self.status_bar.set_text(f"Path {status}")

    def _handle_mouse_click(self, pos):
        """Handle mouse click events for flag placement

        Args:
            pos: The (x, y) position of the mouse click
        """
        # Only handle clicks in a high-resolution view
        if self.map_view.current_view != 0:
            return

        # Get flag sprite dimensions (both flags have the same dimensions)
        flag = self.resources["img_redflag001"]

        # Check if click is within safe area of the map
        is_within_safe_area, _, rel_x, rel_y = self.map_view.is_within_safe_area(
            pos, flag.get_width(), flag.get_height()
        )

        if not is_within_safe_area:
            self.status_bar.set_text("Cannot place flag: click is outside safe area")
            return

        # Update click count and handle flag placement based on click_count modulo 2
        if self.click_count % 2 == 0:
            if self.map_view.get_element("geo_path").visible:
                self.map_view.get_element("geo_path").toggle_visibility()
            # First click (or third, fifth, etc.) - place a red flag
            self.red_flag_pos = (rel_x, rel_y)
            self.green_flag_pos = None
            self.status_bar.set_text(f"Red flag placed at ({rel_x}, {rel_y})")
        else:  # self.click_count % 2 == 1
            # Second click (or fourth, sixth, etc.) - place a green flag
            self.green_flag_pos = (rel_x, rel_y)
            self.status_bar.set_text(f"Green flag placed at ({rel_x}, {rel_y})")

            # Log both coordinates
            self._logger.info(f"Red flag: {self.red_flag_pos}, Green flag: {self.green_flag_pos}")

            # Calculate coordinates on the smaller map
            block_size = DEFAULT_MAP_SIZE // DEFAULT_BLOCKS
            small_coords = {
                "red_x": self.red_flag_pos[0] // block_size,
                "red_y": self.red_flag_pos[1] // block_size,
                "green_x": self.green_flag_pos[0] // block_size,
                "green_y": self.green_flag_pos[1] // block_size,
            }

            # Log coordinates on the smaller map
            self._logger.info(
                f"Small map - Red flag: ({small_coords['red_x']}, {small_coords['red_y']}), "
                f"Green flag: ({small_coords['green_x']}, {small_coords['green_y']})"
            )

        # Update flag positions directly on the Flag objects
        red_flag = self.map_view.get_element("red_flag")
        green_flag = self.map_view.get_element("green_flag")
        red_flag.position = self.red_flag_pos
        green_flag.position = self.green_flag_pos
        self.click_count += 1

    def _update_info_panel(self):
        """Update the info panel with map information"""
        map_info = self.map_view.get_map_info()
        self.info_panel.set_text(map_info)

    def draw(self):
        """Draw everything to the screen"""
        # Clear the screen with gray color
        renderer = RendererFactory.get_current_renderer()
        renderer.clear(self.screen, (128, 128, 128))  # Gray

        # Draw all widgets
        for widget in self.widgets:
            widget.draw()

        # Present the renderer
        renderer.present(self.screen)

    def run(self):
        """Main game loop"""
        # Get the current renderer
        renderer = RendererFactory.get_current_renderer()

        # Initial update of info panel
        self._update_info_panel()
        self.draw()

        while self.running:
            if len(self.handle_events().items()) > 0:
                self._update_info_panel()
                self.draw()

        # Clean up the renderer
        renderer.quit()


def main():
    app = MapSolverApp()
    app.run()


if __name__ == "__main__":
    main()
