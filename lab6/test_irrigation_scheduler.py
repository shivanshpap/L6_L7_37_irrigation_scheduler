import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# ==============================================================================
# Code Coverage (Statement Coverage) Test Suite
# Target Application: irrigation_scheduler.py
# Objective: Achieve at least 90% (100%) statement code coverage.
# ==============================================================================

def test_wet_soil_no_irrigation():
    """Covers lines 1-3: should_irrigate returns False when moisture >= 60."""
    assert should_irrigate(70, 0, "seedling") is False


def test_heavy_rain_no_irrigation():
    """Covers lines 4-5: should_irrigate returns False when rain_mm >= 10."""
    assert should_irrigate(50, 15, "seedling") is False


def test_seedling_needs_irrigation():
    """Covers lines 6-8: should_irrigate returns True for seedling when moisture < 45."""
    assert should_irrigate(40, 2, "seedling") is True


def test_seedling_dry_enough_no_irrigation():
    """Covers line 9: should_irrigate returns False for seedling when moisture >= 45."""
    assert should_irrigate(50, 2, "seedling") is False


def test_flowering_needs_irrigation():
    """Covers lines 10-11: should_irrigate returns True for flowering when moisture < 55."""
    assert should_irrigate(50, 2, "flowering") is True


def test_other_stage_moderate_rain():
    """Covers lines 12-13: should_irrigate returns False for other stages when rain_mm >= 5."""
    assert should_irrigate(35, 8, "vegetative") is False


def test_other_stage_needs_irrigation():
    """Covers line 14: should_irrigate returns True for other stages when moisture < 40."""
    assert should_irrigate(35, 2, "vegetative") is True


def test_invalid_area_volume():
    """Covers lines 18-19: water_volume raises ValueError when area_m2 <= 0."""
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(0, "seedling", 20)


def test_seedling_volume_high_temp():
    """Covers lines 20-21, 26-27, 30: seedling stage with temp_c > 35 (1.5x multiplier)."""
    assert water_volume(10, "seedling", 40) == 30.0


def test_flowering_volume_low_temp():
    """Covers lines 22-23, 28-30: flowering stage with temp_c < 10 (0.5x multiplier)."""
    assert water_volume(10, "flowering", 5) == 25.0


def test_other_stage_volume():
    """Covers lines 24-25, 26-27, 30: other stage (vegetative) with temp_c > 35."""
    assert water_volume(10, "vegetative", 40) == 60.0


def test_schedule_execution():
    """
    Covers lines 34-43: schedule execution covering continue (lines 36-37),
    water_volume computation (line 38), break (lines 39-40), budget update (line 41),
    and plan append (line 42).
    """
    zones = [
        ("ZoneA", 10, 70, 0, "seedling", 40),   # should_irrigate is False -> line 37 (continue)
        ("ZoneB", 10, 40, 0, "seedling", 40),   # needs 30L, fits in budget 50L -> lines 41-42
        ("ZoneC", 10, 40, 0, "flowering", 40),  # needs 75L, budget is 20L -> line 40 (break)
    ]
    assert schedule(zones, 50) == ["ZoneB"]
