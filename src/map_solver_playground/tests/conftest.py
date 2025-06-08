import pygame
import pytest

pytest.mark.unit = pytest.mark.define("Unit tests")
pytest.mark.integration = pytest.mark.define("Integration tests")


@pytest.fixture
def pygame_screen():
    """Fixture for creating a Pygame screen surface."""
    pygame.init()
    screen = pygame.display.set_mode((1000, 900))
    yield screen
    pygame.quit()


@pytest.fixture
def pygame_font():
    """Fixture for creating a Pygame font."""
    pygame.font.init()
    return pygame.font.Font(None, 24)


def pytest_configure(config):
    """Disable pytest-teamcity's coverage integration."""
    config.option.teamcity_no_coverage = True