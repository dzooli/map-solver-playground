"""
This script creates a simple map viewer application with keyboard controls.
"""

import logging
from typing import Dict, Any, cast, Optional

import pygame

from map_solver_playground.asset_loader import load_image_with_transparency
from map_solver_playground.components import StatusBar, InfoPanel, ToolTipPanel, MapView
from map_solver_playground.constants import DEFAULT_MAP_SIZE, DEFAULT_BLOCKS
from map_solver_playground.map.generator import MapGeneratorFactory, MapGenerator
from map_solver_playground.map.render.color_maps import ColorGradient, TerrainColorGradient
from map_solver_playground.map.solver import MapSolverFactory, MapSolver
from map_solver_playground.map.types import Terrain, GeoPath, Flag
from map_solver_playground.profile import measure_time

logger: logging.Logger = logging.getLogger("mapsolver")
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture the timing logs
logger.propagate = False  # Prevent propagation to the root logger to avoid duplicate logs
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
        map_logger: logging.Logger = None,
        generator: str = "RecursiveDiamondSquareGenerator",
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

        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Map Generator Demo")
        self.font = pygame.font.SysFont(None, 24)

        self._logger: logging.Logger | None = map_logger

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
        Create and render map with the specified color gradient.

        Args:
            colors: The color gradient to use for map render, defaults to self.colormap
            generator: The map generator to use for map generation
        """
        # Use the current colormap if none is provided
        colors_to_use = self.colormap if colors is None else colors

        if colors_to_use is None:
            raise ValueError("Color map must be provided")

        # Get the terrain element and create maps
        terrain = self.map_view.get_element("terrain")
        terrain.create_maps(colors_to_use, generator)

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
        """Handle pygame events and track event occurrences."""
        events = {}
        for event in pygame.event.get():
            events.update({event.type: events.get(event.type, 0) + 1})
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_key_press(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                self._handle_mouse_click(event.pos)
        return events

    def _handle_key_press(self, key):
        """Handle single key press events"""
        if key == pygame.K_q:
            self.running = False
        elif key == pygame.K_n:
            self._handle_new_map()
        elif key == pygame.K_s:
            # S: Solve a path
            self._handle_solve_path()
        elif key == pygame.K_h:
            # H: Toggle path visibility
            self._handle_toggle_path_visibility()
        elif key == pygame.K_v:
            # V: Switch view
            self._handle_view_switch()
        elif key == pygame.K_t:
            # T: Toggle tooltip
            self._handle_tooltip_toggle()

    def _handle_new_map(self):
        """Generate a new map"""
        self.status_bar.set_text("Generating a new map...")
        self.status_bar.draw()
        if self.map_view.current_view == 1:
            self.map_view.switch_view()
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
                geo_path.color = pygame.color.THECOLORS["blue"][:3]  # Convert RGBA to RGB
                geo_path.visible = True

                # Update properties for backward compatibility
                self.path_visible = True
                self.status_bar.set_text(f"Path solved using {solver.__class__.__name__}")
            else:
                self.status_bar.set_text("No path found between the flags")
        except Exception as e:
            self.status_bar.set_text(f"Error solving path: {str(e)}")
            if self._logger:
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
            if self._logger:
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
        self.screen.fill(pygame.color.THECOLORS["gray"])

        for widget in self.widgets:
            widget.draw()

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()

        # Initial update of info panel
        self._update_info_panel()
        self.draw()

        while self.running:
            if len(self.handle_events().items()) > 0:
                self._update_info_panel()
                self.draw()
            clock.tick(60)  # 60 FPS

        pygame.quit()


def main():
    app = MapSolverApp(map_logger=logger)
    app.run()


if __name__ == "__main__":
    main()
