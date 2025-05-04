"""
This script creates a simple map viewer application with keyboard controls.
"""

import logging
from typing import Dict, Any

import pygame

from map_solver_playground.asset_loader import load_image_with_transparency
from map_solver_playground.components import StatusBar, InfoPanel, ToolTipPanel, MapView
from map_solver_playground.maps.generators import MapGeneratorFactory
from map_solver_playground.maps.visualization.color_maps import ColorGradient, TerrainColorGradient
from map_solver_playground.metrics import measure_time

logger: logging.Logger = logging.getLogger("mapsolver")
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture the timing logs
logger.propagate = False  # Prevent propagation to the root logger to avoid duplicate logs
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

MAP_SIZE = 600
BLOCKS = 10


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
        self._generator_name = generator
        self.map_generator = MapGeneratorFactory.create(self._generator_name, width=MAP_SIZE, height=MAP_SIZE)

        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Map Generator Demo")
        self.font = pygame.font.SysFont(None, 24)

        self._logger: logging.Logger | None = map_logger

        self.colormap: TerrainColorGradient = ColorGradient.TOPO_COLORS if colormap is None else colormap
        # Create the map view component
        self.map_view = MapView(self.screen, self.width, self.height, map_size, block_size, self.colormap)
        # Status bar for displaying messages
        self.status_bar = StatusBar(self.screen, self.width, self.height, self.font)
        # Info panel for displaying map information
        self.info_panel = InfoPanel(self.screen, self.width, self.height, self.font)
        # Tooltip panel for displaying instructions
        self.tooltip_panel = ToolTipPanel(self.screen, self.width, self.height, self.font)
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

    @measure_time(logger_instance=logger)
    def load_resources(self) -> None:
        """Load resources like images and sounds"""
        for sprite_name in ["redflag001.png", "greenflag001.png"]:
            self.resources[f"img_{sprite_name.split('.')[0]}"] = load_image_with_transparency(
                sprite_name, target_size=(30, 30)
            )

        # Set flag images in map view
        self.map_view.set_flag_images(self.resources["img_redflag001"], self.resources["img_greenflag001"])

    @measure_time(logger_instance=logger)
    def create_maps(self, colors: TerrainColorGradient = None):
        """Create new maps using the map view component"""
        self.map_view.create_maps(self.colormap if colors is None else colors)

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
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_n:
            self._handle_new_map()
        elif key == pygame.K_s:
            self._handle_view_switch()
        elif key == pygame.K_h:
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
        self.map_view.set_flag_positions(None, None)
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

    def _handle_mouse_click(self, pos):
        """Handle mouse click events for flag placement

        Args:
            pos: The (x, y) position of the mouse click
        """
        # Only handle clicks in high resolution view
        if self.map_view.current_view != 0:
            return

        # Get flag sprite dimensions (both flags have the same dimensions)
        flag = self.resources["img_redflag001"]

        # Check if click is within safe area of the map
        is_within_safe_area, is_within_map, rel_x, rel_y = self.map_view.is_within_safe_area(
            pos, flag.get_width(), flag.get_height()
        )

        if is_within_safe_area:
            # Update click count and handle flag placement based on click_count modulo 2
            if self.click_count % 2 == 0:
                # First click (or third, fifth, etc.) - place red flag
                self.red_flag_pos = (rel_x, rel_y)
                self.green_flag_pos = None
                self.status_bar.set_text(f"Red flag placed at ({rel_x}, {rel_y})")
            else:  # self.click_count % 2 == 1
                # Second click (or fourth, sixth, etc.) - place green flag
                self.green_flag_pos = (rel_x, rel_y)
                self.status_bar.set_text(f"Green flag placed at ({rel_x}, {rel_y})")

                # Log both coordinates
                if self._logger:
                    self._logger.info(f"Red flag: {self.red_flag_pos}, Green flag: {self.green_flag_pos}")

                    # Calculate coordinates on the smaller map
                    block_size = MAP_SIZE // BLOCKS
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

            # Update flag positions in map view
            self.map_view.set_flag_positions(self.red_flag_pos, self.green_flag_pos)
            self.click_count += 1
        elif is_within_map:
            # Click is within map but too close to the edge for flag placement
            self.status_bar.set_text("Cannot place flag: too close to map edge")

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
