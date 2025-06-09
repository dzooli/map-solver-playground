"""
Performance test for MapView component.

This script tests how many flags can be displayed on a 500x500 terrain
within 1/30 seconds (33.33 ms).
"""

import logging
import os
import random
import time
from datetime import datetime
from typing import List, Any, Tuple

import numpy as np

from map_solver_playground.asset_loader.backend_independent_image_loader import load_image_with_transparency
from map_solver_playground.components.map_view import MapView
from map_solver_playground.map.map_data import Map
from map_solver_playground.map.render.color_maps import ColorGradient
from map_solver_playground.map.render.element.renderer_factory import RendererFactory, RendererBackend
from map_solver_playground.map.types.flag import Flag
from map_solver_playground.map.types.terrain import Terrain

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create a file handler for logging results
RESULT_DIR = "test-results/performance"
os.makedirs(RESULT_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_handler = logging.FileHandler(f"{RESULT_DIR}/mapview_performance_{timestamp}.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)


def create_terrain(size: int = 500) -> Terrain:
    """
    Create a terrain with the specified size.

    Args:
        size: The size of the terrain (width and height)

    Returns:
        A Terrain object with the specified size
    """
    # Create a map with the specified size
    map_data = Map(size, size)

    # Fill the map with random height values
    map_data.data = np.random.default_rng(42).random((size, size))

    # Create a terrain with the map data
    terrain = Terrain(map_data, map_size=size)

    # Create maps with a color gradient
    terrain.create_maps(ColorGradient.TOPO_COLORS)

    return terrain


def run_performance_test(num_runs: int = 5) -> List[int]:
    """
    Run the performance test multiple times.

    Args:
        num_runs: The number of test runs to perform

    Returns:
        A list of the maximum number of flags that can be displayed within 1/30 seconds (33.33 ms)
    """
    results = []

    for run in range(1, num_runs + 1):
        logger.info(f"Starting test run {run}/{num_runs}")
        max_flags = test_mapview_performance()
        logger.info(f"Test run {run}/{num_runs} completed: {max_flags} flags within 1/30 second (33.33ms)")
        results.append(max_flags)

    return results


def test_mapview_performance() -> int:
    """
    Test how many flags can be displayed on a 500x500 terrain within 1/30 seconds (33.33 ms).

    Returns:
        The maximum number of flags that can be displayed within 1/30 seconds (33.33 ms)
    """
    # Setup test environment
    screen, map_view = _setup_test_environment()

    # Load and prepare flag images
    flag_images, flag_width, flag_height = _prepare_flag_images()

    # Test variables
    test_params = {
        "running": True,
        "num_flags": 0,
        "target_frame_time": 1 / 30,  # 33.33ms (30 FPS)
        "max_flags_in_target_time": 0,
        "iteration": 0,
        "max_iterations": 100,
        "batch_size": 1000,
    }

    # Run test loop
    max_flags = _run_test_loop(screen, map_view, flag_images, flag_width, flag_height, test_params)

    # Cleanup
    renderer = RendererFactory.get_current_renderer()
    renderer.quit()

    return max_flags


def _setup_test_environment():
    """Setup renderer and create map view"""
    # Set the renderer backend to pygame
    RendererFactory.set_backend(RendererBackend.PYGAME)

    # Initialize the renderer
    renderer = RendererFactory.get_current_renderer()
    renderer.init()

    screen_width, screen_height = 500, 500
    _, screen = renderer.create_window(screen_width, screen_height, "MapView Performance Test")

    terrain = create_terrain(500)
    map_view = MapView(screen, screen_width, screen_height, terrain, map_size=500)

    return screen, map_view


def _prepare_flag_images():
    """Load and resize flag images if needed"""
    # Get the current renderer
    renderer = RendererFactory.get_current_renderer()

    red_flag_image = load_image_with_transparency("redflag001.png")
    green_flag_image = load_image_with_transparency("greenflag001.png")
    flag_images = [red_flag_image, green_flag_image]

    flag_width = max(renderer.get_image_width(img) for img in flag_images)
    flag_height = max(renderer.get_image_height(img) for img in flag_images)
    print(f"Flag dimensions: {flag_width}x{flag_height}")

    if flag_width > 100 or flag_height > 100:
        flag_images, flag_width, flag_height = _resize_flags(flag_images, flag_width, flag_height)

    return flag_images, flag_width, flag_height


def _resize_flags(flag_images, flag_width, flag_height):
    """Resize flags to appropriate dimensions"""
    # Get the current renderer
    renderer = RendererFactory.get_current_renderer()

    new_width = min(flag_width, 50)
    new_height = min(flag_height, 50)
    aspect_ratio = flag_width / flag_height

    if aspect_ratio > 1:
        new_height = int(new_width / aspect_ratio)
    else:
        new_width = int(new_height * aspect_ratio)

    resized_images = [renderer.scale_image(img, (new_width, new_height)) for img in flag_images]
    print(f"Resized flags to: {new_width}x{new_height}")

    return resized_images, new_width, new_height


def _run_test_loop(screen, map_view, flag_images, flag_width, flag_height, params):
    """Run the main test loop"""
    while params["running"] and params["iteration"] < params["max_iterations"]:
        params["iteration"] += 1

        # Handle events
        params["running"] = _handle_events()

        # Add flags
        params["num_flags"] = _add_flag_batch(
            map_view, flag_images, flag_width, flag_height, params["num_flags"], params["batch_size"]
        )

        # Measure performance
        frame_time = _measure_frame_time(screen, map_view)

        # Calculate results
        if frame_time > 0:
            flags_per_target_time = int(params["num_flags"] * (params["target_frame_time"] / frame_time))
            fps = 1 / frame_time
            print(
                f"Iteration {params['iteration']}: {params['num_flags']} flags, "
                f"{frame_time*1000:.2f}ms, {fps:.2f} FPS, estimated "
                f"{flags_per_target_time} flags in {params['target_frame_time']*1000:.2f}ms"
            )
            params["max_flags_in_target_time"] = flags_per_target_time

    return params["max_flags_in_target_time"]


def _handle_events():
    """Handle renderer events"""
    # Get the current renderer
    renderer = RendererFactory.get_current_renderer()

    for event in renderer.get_events():
        if renderer.is_quit_event(event):
            return False
    return True


def _add_flag_batch(map_view, flag_images, flag_width, flag_height, num_flags, batch_size):
    """Add a batch of flags to the map"""
    for _ in range(batch_size):
        x = random.randint(flag_width // 2, 500 - flag_width // 2)
        y = random.randint(flag_height // 2, 500 - flag_height // 2)

        is_safe, is_within_map, rel_x, rel_y = map_view.is_within_safe_area((x, y), flag_width, flag_height)

        if is_safe and is_within_map:
            flag = Flag(position=(rel_x, rel_y), image=random.choice(flag_images))
            map_view.add_element(f"flag_{num_flags}", flag)
            num_flags += 1

    return num_flags


def _measure_frame_time(screen, map_view):
    """Measure time taken to render frame"""
    # Get the current renderer
    renderer = RendererFactory.get_current_renderer()

    renderer.clear(screen, (0, 0, 0))  # Black
    start_time = time.time()
    map_view.draw()
    end_time = time.time()
    renderer.present(screen)
    return end_time - start_time


def main():
    """
    Main function to run the performance test.
    """
    logger.info("Starting MapView performance test")

    # Run the performance test multiple times
    results = run_performance_test(5)

    # Calculate and log the average result
    avg_result = sum(results) / len(results)
    logger.info(f"Performance test results: {results}")
    logger.info(f"Average number of flags within 1/30 second (33.33ms): {avg_result:.2f}")

    # Log individual run results
    for i, result in enumerate(results, 1):
        logger.info(f"Run {i}: {result} flags within 1/30 second (33.33ms)")

    logger.info("MapView performance test completed")


if __name__ == "__main__":
    main()
