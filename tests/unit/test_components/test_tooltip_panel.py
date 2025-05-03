import pytest
from map_solver_playground.components.tooltip_panel import ToolTipPanel


class TestToolTipPanel:
    @pytest.fixture
    def tooltip_panel(self, pygame_screen, pygame_font):
        return ToolTipPanel(screen=pygame_screen, width=1000, height=900, font=pygame_font)

    def test_initialization(self, tooltip_panel):
        assert tooltip_panel.visible is True
        assert len(tooltip_panel.tooltips) == 4
        assert tooltip_panel.position == (10, 750)
        assert tooltip_panel.size == (880, 100)

    def test_set_tooltips(self, tooltip_panel):
        new_tooltips = ["Tip 1", "Tip 2"]
        tooltip_panel.tooltips = new_tooltips
        assert tooltip_panel.tooltips == new_tooltips

    def test_set_tooltips_validation(self, tooltip_panel):
        with pytest.raises(ValueError):
            tooltip_panel.tooltips = None
        with pytest.raises(TypeError):
            tooltip_panel.tooltips = 1234567890

    def test_toggle_visibility(self, tooltip_panel):
        initial_visibility = tooltip_panel.visible
        tooltip_panel.toggle_visibility()
        assert tooltip_panel.visible != initial_visibility
