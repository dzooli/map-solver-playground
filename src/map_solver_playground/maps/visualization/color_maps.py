"""
Color maps module.

This module provides color maps for map visualization.
"""

from typing import List, Tuple

TerrainColor = Tuple[int, int, int]
TerrainColorGradient = List[TerrainColor]


# List of RGB tuples representing different terrain types
class ColorGradient:
    UNDEFINED: TerrainColorGradient = [(0, 0, 0)]
    TOPO_COLORS: List[TerrainColor] = [
        # Water (blues)
        (0, 20, 80),  # 0: Deep ocean
        (0, 40, 150),  # 1: Ocean
        (0, 80, 200),  # 2: Coastal waters
        (0, 120, 255),  # 3: Shallow water
        # Plains and hills (greens to yellows)
        (100, 220, 100),  # 4: Coastal plains
        (150, 220, 50),  # 5: Grasslands
        (180, 200, 50),  # 6: Savanna
        (200, 180, 50),  # 7: Dry plains
        (180, 160, 50),  # 8: Low hills
        (160, 140, 40),  # 9: Rolling hills
        (140, 120, 30),  # 10: High hills
        # Mountains (browns to grays)
        (120, 100, 30),  # 11: Foothills
        (100, 80, 30),  # 12: Low mountains
        (80, 60, 30),  # 13: Mountains
        (60, 40, 20),  # 14: High mountains
        (40, 20, 10),  # 15: Peak mountains
    ]

    HEATMAP_COLORS: List[TerrainColor] = [
        # Cold (blues)
        (0, 0, 255),  # 0: Coldest
        (0, 60, 255),  # 1: Very cold
        (0, 120, 255),  # 2: Cold
        (0, 180, 255),  # 3: Cool
        # Transition (cyan to yellow)
        (0, 255, 255),  # 4: Cool-neutral
        (60, 255, 240),  # 5: Neutral-cool
        (120, 255, 180),  # 6: Neutral
        (180, 255, 120),  # 7: Neutral-warm
        (255, 255, 60),  # 8: Warm-neutral
        # Hot (yellows to reds)
        (255, 240, 0),  # 9: Warm
        (255, 180, 0),  # 10: Very warm
        (255, 120, 0),  # 11: Hot
        (255, 60, 0),  # 12: Very hot
        (255, 0, 0),  # 13: Extremely hot
        (200, 0, 0),  # 14: Dangerously hot
        (160, 0, 0),  # 15: Critically hot
    ]
