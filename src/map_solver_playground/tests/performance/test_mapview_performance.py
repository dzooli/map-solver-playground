"""
Performance test for MapView component.

This script tests how many flags can be displayed on a 500x500 terrain
within 1/30 seconds (33.33 ms) using both PyGame and SDL2 backends.
Results are displayed using rich console output and can be saved as a CSV file.
"""

import logging
import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.table import Table

from map_solver_playground.asset_loader.backend_independent_image_loader import load_image_with_transparency
from map_solver_playground.components.map_view import MapView
from map_solver_playground.map.map_data import Map
from map_solver_playground.map.render.color_maps import ColorGradient
from map_solver_playground.map.render.element.renderer_factory import RendererFactory, RendererBackend
from map_solver_playground.map.types.flag import Flag
from map_solver_playground.map.types.terrain import Terrain

app = typer.Typer()

console = Console()

# Configure rich handler for console output
rich_handler = RichHandler(rich_tracebacks=True, console=console)
rich_handler.setLevel(logging.INFO)

# Configure file handler for logging to file
RESULT_DIR = "test-results/performance"
os.makedirs(RESULT_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_handler = logging.FileHandler(f"{RESULT_DIR}/mapview_performance_{timestamp}.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Configure root logger
logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[rich_handler, file_handler])

logger = logging.getLogger(__name__)


def create_terrain(size: int = 500) -> Terrain:
    """
    Create a terrain with the specified size.

    Args:
        size: The size of the terrain (width and height)

    Returns:
        A Terrain object with the specified size
    """
    map_data = Map(size, size)
    map_data.data = np.random.default_rng(42).random((size, size))
    terrain = Terrain(map_data, map_size=size)
    terrain.create_maps(ColorGradient.TOPO_COLORS)
    return terrain


def run_performance_test(num_runs: int = 5, backend: Optional[RendererBackend] = None) -> pd.DataFrame:
    """
    Run the performance test multiple times with the specified backend.

    Args:
        num_runs: The number of test runs to perform
        backend: The renderer backend to use (if None, uses the current backend)

    Returns:
        A pandas DataFrame containing the test results
    """
    results = []
    backend_name = backend.value if backend else RendererFactory.get_current_backend().value

    console.print(f"[bold blue]Running performance test with {backend_name} backend...[/bold blue]")

    # Create a progress bar for test runs
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=False,
    ) as progress:
        # Task for tracking test runs
        run_task = progress.add_task(f"[cyan]Testing {backend_name} backend", total=num_runs)

        # Task for tracking flag rendering within each test run
        test_task = progress.add_task("[cyan]Testing flag rendering performance", total=100, visible=False)

        for run in range(1, num_runs + 1):
            logger.info(f"Starting test run {run}/{num_runs} with {backend_name} backend")

            # Reset the test task for each run
            progress.update(test_task, completed=0, visible=True, num_flags=0)

            max_flags = test_mapview_performance(backend, progress, test_task)

            # Hide the test task after completion
            progress.update(test_task, visible=False)

            logger.info(f"Test run {run}/{num_runs} completed: {max_flags} flags within 1/30 second (33.33ms)")
            progress.update(
                run_task,
                advance=1,
                description=f"[cyan]Testing {backend_name} backend - Run {run}/{num_runs}: {max_flags} flags",
            )

            results.append({"run": run, "backend": backend_name, "max_flags": max_flags})

    df = pd.DataFrame(results)

    return df


def test_mapview_performance(backend: Optional[RendererBackend] = None, progress=None, task_id=None) -> int:
    """
    Test how many flags can be displayed on a 500x500 terrain within 1/30 seconds (33.33 ms).

    Args:
        backend: The renderer backend to use (if None, uses the current backend)
        progress: Optional progress bar to update during testing
        task_id: ID of the task in the progress bar to update

    Returns:
        The maximum number of flags that can be displayed within 1/30 seconds (33.33 ms)
    """
    screen, map_view = _setup_test_environment(backend)
    flag_images, flag_width, flag_height = _prepare_flag_images()

    test_params = {
        "running": True,
        "num_flags": 0,
        "target_frame_time": 1 / 30,  # 33.33ms (30 FPS)
        "max_flags_in_target_time": 0,
        "iteration": 0,
        "max_iterations": 100,
        "batch_size": 1000,
    }

    max_flags = _run_test_loop(screen, map_view, flag_images, flag_width, flag_height, test_params, progress, task_id)

    renderer = RendererFactory.get_current_renderer()
    renderer.quit()

    return max_flags


def _setup_test_environment(backend: Optional[RendererBackend] = None):
    """
    Setup renderer and create map view

    Args:
        backend: The renderer backend to use (if None, uses PyGame)
    """
    if backend:
        RendererFactory.set_backend(backend)
    else:
        RendererFactory.set_backend(RendererBackend.PYGAME)

    renderer = RendererFactory.get_current_renderer()
    renderer.init()

    screen_width, screen_height = 500, 500
    _, screen = renderer.create_window(screen_width, screen_height, "MapView Performance Test")

    terrain = create_terrain(500)
    map_view = MapView(screen, screen_width, screen_height, terrain, map_size=500)

    return screen, map_view


def _prepare_flag_images():
    """Load and resize flag images if needed"""
    renderer = RendererFactory.get_current_renderer()

    red_flag_image = load_image_with_transparency("redflag001.png")
    green_flag_image = load_image_with_transparency("greenflag001.png")
    flag_images = [red_flag_image, green_flag_image]

    flag_width = max(renderer.get_image_width(img) for img in flag_images)
    flag_height = max(renderer.get_image_height(img) for img in flag_images)
    logger.info(f"Flag dimensions: {flag_width}x{flag_height}")

    if flag_width > 100 or flag_height > 100:
        flag_images, flag_width, flag_height = _resize_flags(flag_images, flag_width, flag_height)

    return flag_images, flag_width, flag_height


def _resize_flags(flag_images, flag_width, flag_height):
    """Resize flags to appropriate dimensions"""
    renderer = RendererFactory.get_current_renderer()

    new_width = min(flag_width, 50)
    new_height = min(flag_height, 50)
    aspect_ratio = flag_width / flag_height

    if aspect_ratio > 1:
        new_height = int(new_width / aspect_ratio)
    else:
        new_width = int(new_height * aspect_ratio)

    resized_images = [renderer.scale_image(img, (new_width, new_height)) for img in flag_images]

    return resized_images, new_width, new_height


def _run_test_loop(screen, map_view, flag_images, flag_width, flag_height, params, progress=None, task_id=None):
    """Run the main test loop"""
    while params["running"] and params["iteration"] < params["max_iterations"]:

        params["iteration"] += 1
        params["running"] = _handle_events()

        params["num_flags"] = _add_flag_batch(
            map_view, flag_images, flag_width, flag_height, params["num_flags"], params["batch_size"]
        )
        frame_time = _measure_frame_time(screen, map_view)

        if frame_time > 0:
            flags_per_target_time = int(params["num_flags"] * (params["target_frame_time"] / frame_time))
            fps = 1 / frame_time
            params["max_flags_in_target_time"] = flags_per_target_time

            # Update progress bar if provided
            if progress and task_id is not None:
                progress.update(
                    task_id,
                    advance=1,
                    num_flags=params["num_flags"],
                    description=f"[cyan]Testing flag rendering performance - FPS: {fps:.2f}",
                )

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
    renderer = RendererFactory.get_current_renderer()

    renderer.clear(screen, (0, 0, 0))  # Black
    start_time = time.time()
    map_view.draw()
    end_time = time.time()
    renderer.present(screen)
    return end_time - start_time


def run_performance_tests(num_runs: int, save_csv: bool, save_df: bool, output_dir: str):
    """
    Run performance tests with SDL2 and PyGame backends and compare results.

    Args:
        num_runs: Number of test runs per backend
        save_csv: Whether to save results to CSV file
        save_df: Whether to save results to DataFrame pickle file
        output_dir: Output directory for saved results
    """
    logger.info("Starting MapView performance test with multiple backends")
    console.print("[bold magenta]Starting MapView Performance Test[/bold magenta]")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    pygame_results = run_performance_test(num_runs, RendererBackend.PYGAME)
    sdl2_results = run_performance_test(num_runs, RendererBackend.SDL2)
    all_results = pd.concat([pygame_results, sdl2_results], ignore_index=True)

    # Generate summary statistics
    summary = generate_summary(all_results)

    # Print results table
    print_results_table(summary)

    # Save results if requested
    save_results(all_results, output_path, save_csv, save_df)

    console.print("[bold green]MapView performance test completed[/bold green]")
    logger.info("MapView performance test completed")


def generate_summary(all_results: pd.DataFrame) -> pd.DataFrame:
    """Generate summary statistics from test results"""
    return all_results.groupby("backend")["max_flags"].agg(["mean", "std", "min", "max"]).reset_index()


def print_results_table(summary: pd.DataFrame):
    """Print formatted results table"""
    console.print("\n[bold yellow]Performance Test Summary[/bold yellow]")
    table = create_table()

    pygame_mean = summary[summary["backend"] == "pygame"]["mean"].values[0]
    sdl2_mean = summary[summary["backend"] == "sdl2"]["mean"].values[0]
    better_backend = "pygame" if pygame_mean > sdl2_mean else "sdl2"

    populate_table(table, summary, better_backend)
    console.print(table)
    logger.info(f"Performance test summary:\n{summary.to_string()}")


def create_table() -> Table:
    """Create results table with columns"""
    table = Table(show_header=True, header_style="bold")
    table.add_column("Backend")
    table.add_column("Mean Flags", justify="right")
    table.add_column("Std Dev", justify="right")
    table.add_column("Min Flags", justify="right")
    table.add_column("Max Flags", justify="right")
    return table


def populate_table(table: Table, summary: pd.DataFrame, better_backend: str):
    """Populate table with formatted rows"""
    for _, row in summary.iterrows():
        backend = row["backend"]
        style = "[green]" if backend == better_backend else ""
        table.add_row(
            f"{style}{backend}[/]" if style else backend,
            f"{style}{row['mean']:.2f}[/]" if style else f"{row['mean']:.2f}",
            f"{style}{row['std']:.2f}[/]" if style else f"{row['std']:.2f}",
            f"{style}{row['min']:.0f}[/]" if style else f"{row['min']:.0f}",
            f"{style}{row['max']:.0f}[/]" if style else f"{row['max']:.0f}",
        )


def save_results(results: pd.DataFrame, output_path: Path, save_csv: bool, save_df: bool):
    """Save results to files if requested"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if save_csv:
        csv_path = output_path / f"mapview_performance_{timestamp}.csv"
        results.to_csv(csv_path, index=False)
        console.print(f"[blue]Results saved to CSV: {csv_path}[/blue]")
        logger.info(f"Results saved to CSV: {csv_path}")

    if save_df:
        df_path = output_path / f"mapview_performance_{timestamp}.pkl"
        results.to_pickle(df_path)
        console.print(f"[blue]Results saved to DataFrame pickle: {df_path}[/blue]")
        logger.info(f"Results saved to DataFrame pickle: {df_path}")


@app.command()
def main(
    runs: int = typer.Option(5, "--runs", "-r", help="Number of test runs per backend"),
    save_csv: bool = typer.Option(False, "--save-csv", help="Save results to CSV file"),
    save_df: bool = typer.Option(False, "--save-df", help="Save results to DataFrame pickle file"),
    output_dir: Path = typer.Option(
        Path("test-results/performance"),
        "--output-dir",
        "-o",
        help="Output directory for saved results",
        exists=False,
        file_okay=False,
        dir_okay=True,
        writable=True,
    ),
):
    """
    Run performance tests with SDL2 and PyGame backends and compare results.
    """
    # Run the performance tests with the parameters provided by typer
    run_performance_tests(runs, save_csv, save_df, output_dir)


if __name__ == "__main__":
    app()
