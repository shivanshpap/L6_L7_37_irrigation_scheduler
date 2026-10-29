import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# ==============================================================================
# Branch Coverage Test Suite
# Target Application: irrigation_scheduler.py
# Objective: Achieve 100% Branch Coverage and 100% Statement Coverage
#            by thoroughly covering all decision paths, boundary conditions,
#            and loop edge conditions.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Tests for should_irrigate(moisture, rain_mm, stage)
# ------------------------------------------------------------------------------

def test_should_irrigate_moisture_ge_60_true():
    """Branch: moisture >= 60 evaluates to True (boundary at 60, above at 75)."""
    assert should_irrigate(60, 0, "seedling") is False
    assert should_irrigate(75, 0, "seedling") is False


def test_should_irrigate_moisture_ge_60_false():
    """Branch: moisture >= 60 evaluates to False (boundary at 59, proceeds to rain check)."""
    assert should_irrigate(59, 12, "seedling") is False


def test_should_irrigate_rain_ge_10_true():
    """Branch: rain_mm >= 10 evaluates to True (boundary at 10, above at 15)."""
    assert should_irrigate(50, 10, "seedling") is False
    assert should_irrigate(50, 15, "seedling") is False


def test_should_irrigate_rain_ge_10_false():
    """Branch: rain_mm >= 10 evaluates to False (boundary at 9, proceeds to stage check)."""
    assert should_irrigate(40, 9, "seedling") is True


def test_should_irrigate_stage_seedling_moisture_lt_45_true():
    """Stage == 'seedling' (True), moisture < 45 (True: boundary 44, nominal 30)."""
    assert should_irrigate(44, 2, "seedling") is True
    assert should_irrigate(30, 0, "seedling") is True


def test_should_irrigate_stage_seedling_moisture_lt_45_false():
    """Stage == 'seedling' (True), moisture < 45 (False: boundary 45, nominal 50)."""
    assert should_irrigate(45, 2, "seedling") is False
    assert should_irrigate(50, 0, "seedling") is False


def test_should_irrigate_stage_flowering_true():
    """Stage == 'flowering' (True), moisture < 55 (True: boundary 54, nominal 40)."""
    assert should_irrigate(54, 2, "flowering") is True
    assert should_irrigate(40, 0, "flowering") is True


def test_should_irrigate_stage_flowering_false():
    """Stage == 'flowering' (True), moisture < 55 (False: boundary 55, nominal 58)."""
    assert should_irrigate(55, 2, "flowering") is False
    assert should_irrigate(58, 0, "flowering") is False


def test_should_irrigate_other_stage_rain_ge_5_true():
    """Other stage (vegetative/fruiting), rain_mm >= 5 (True: boundary 5, nominal 8)."""
    assert should_irrigate(30, 5, "vegetative") is False
    assert should_irrigate(30, 8, "fruiting") is False


def test_should_irrigate_other_stage_moisture_lt_40_true():
    """Other stage, rain_mm < 5, moisture < 40 (True: boundary 39, nominal 25)."""
    assert should_irrigate(39, 4, "vegetative") is True
    assert should_irrigate(25, 0, "maturation") is True


def test_should_irrigate_other_stage_moisture_lt_40_false():
    """Other stage, rain_mm < 5, moisture < 40 (False: boundary 40, nominal 50)."""
    assert should_irrigate(40, 4, "vegetative") is False
    assert should_irrigate(50, 2, "maturation") is False


# ------------------------------------------------------------------------------
# 2. Tests for water_volume(area_m2, stage, temp_c)
# ------------------------------------------------------------------------------

def test_water_volume_invalid_area_zero_and_negative():
    """Branch: area_m2 <= 0 evaluates to True (boundary 0, negative -10) -> raises ValueError."""
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(0, "seedling", 25)
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(-10, "seedling", 25)


def test_water_volume_seedling_stage():
    """Branch: stage == 'seedling' -> True (base litres = 2)."""
    assert water_volume(10, "seedling", 25) == 20.0


def test_water_volume_flowering_stage():
    """Branch: stage == 'flowering' -> True (base litres = 5)."""
    assert water_volume(10, "flowering", 25) == 50.0


def test_water_volume_other_stage():
    """Branch: stage not seedling or flowering -> True (base litres = 4)."""
    assert water_volume(10, "vegetative", 25) == 40.0
    assert water_volume(10, "harvest", 25) == 40.0


def test_water_volume_temp_gt_35():
    """Branch: temp_c > 35 -> True (1.5x multiplier, boundary 36, nominal 40)."""
    assert water_volume(10, "seedling", 36) == 30.0
    assert water_volume(10, "flowering", 40) == 75.0


def test_water_volume_temp_lt_10():
    """Branch: temp_c < 10 -> True (0.5x multiplier, boundary 9, nominal 5)."""
    assert water_volume(10, "seedling", 9) == 10.0
    assert water_volume(10, "flowering", 5) == 25.0


def test_water_volume_temp_normal_boundaries():
    """
    Branch: 10 <= temp_c <= 35 evaluates to True (neither temp > 35 nor temp < 10 branch taken).
    Tests lower boundary (10), upper boundary (35), and intermediate (20).
    """
    assert water_volume(10, "seedling", 10) == 20.0
    assert water_volume(10, "seedling", 35) == 20.0
    assert water_volume(10, "seedling", 20) == 20.0


# ------------------------------------------------------------------------------
# 3. Tests for schedule(zones, budget)
# ------------------------------------------------------------------------------

def test_schedule_empty_zones():
    """Branch: for-loop does not execute when zones list is empty -> returns []."""
    assert schedule([], 100) == []


def test_schedule_all_zones_skip_irrigation():
    """Branch: loop executes, should_irrigate is False for all zones -> continue (line 37)."""
    zones = [
        ("Z1", 10, 75, 0, "seedling", 20),
        ("Z2", 10, 50, 15, "flowering", 20),
    ]
    assert schedule(zones, 100) == []


def test_schedule_all_zones_fit_budget():
    """
    Branch: loop executes, all zones fit within budget and plan finishes naturally without break.
    Exercises branch 35->43 (loop normal completion).
    """
    zones = [
        ("ZoneA", 10, 30, 0, "seedling", 20),    # need = 20, remaining budget = 80
        ("ZoneB", 10, 30, 0, "vegetative", 20),  # need = 40, remaining budget = 40
    ]
    assert schedule(zones, 100) == ["ZoneA", "ZoneB"]


def test_schedule_budget_exhausted_break():
    """Branch: need > budget evaluates to True -> break statement (line 40)."""
    zones = [
        ("ZoneA", 10, 30, 0, "seedling", 20),    # need = 20, remaining budget = 30
        ("ZoneB", 10, 30, 0, "flowering", 20),   # need = 50, > 30 budget -> break
        ("ZoneC", 10, 30, 0, "seedling", 20),    # unreachable due to break
    ]
    assert schedule(zones, 50) == ["ZoneA"]


def test_schedule_exact_budget_match():
    """Edge case: need == budget (need > budget evaluates to False, remaining budget becomes 0)."""
    zones = [
        ("ZoneExact", 10, 30, 0, "seedling", 20),  # need = 20, budget = 20 -> remaining = 0
    ]
    assert schedule(zones, 20) == ["ZoneExact"]
