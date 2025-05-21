import pytest
from map_solver_playground.components.tooltip_panel import ToolTipPanel


class TestToolTipPanel:
    @pytest.fixture
    def tooltip_panel(self, pygame_screen, pygame_font):
        return ToolTipPanel(screen=pygame_screen, width=1000, height=900, font=pygame_font)

    def test_toggle_visibility(self, tooltip_panel):
        initial_visibility = tooltip_panel.visible
        tooltip_panel.toggle_visibility()
        assert tooltip_panel.visible != initial_visibility
