"""
Hypothesis Fuzz Testing Suite executed against Buggy Application
Course: Software Engineering (UE22CS341AA) - Lab 7: Fuzzing for Input Validation Bugs
Scenario 37: Irrigation Scheduler
Student: Shivansh Sharma (PES2UG24CS474)

This test suite exposes input validation vulnerabilities in the unhardened application:
  - should_irrigate crashes on None, strings, booleans, NaN, out-of-range values.
  - water_volume crashes on None/strings, allows NaN to bypass area checks, silences invalid stages.
  - schedule crashes on None zones, malformed tuples, None/negative/NaN budgets.
"""

import math
import pytest
from hypothesis import given, settings, strategies as st

# Import functions from buggy application
from buggy_processor import should_irrigate, water_volume, schedule


# =====================================================================
# Strategy Definitions for Fuzz Testing
# =====================================================================

fuzz_scalars = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-1000, max_value=1000),
    st.floats(allow_nan=True, allow_infinity=True, width=32),
    st.text(max_size=20),
)

valid_stages = st.sampled_from(["seedling", "flowering", "vegetative", "fruiting", "mature"])


# =====================================================================
# 1. Fuzz Testing should_irrigate()
# =====================================================================

@given(moisture=fuzz_scalars, rain_mm=fuzz_scalars, stage=fuzz_scalars)
@settings(max_examples=100)
def test_fuzz_should_irrigate_robustness(moisture, rain_mm, stage):
    """
    PROPERTY: should_irrigate must never crash with unhandled TypeErrors or
    AttributeErrors. It must either return a bool (if input is valid) or
    safely raise (ValueError, TypeError).
    """
    try:
        res = should_irrigate(moisture, rain_mm, stage)
        # Invariant: If it returned, result must be boolean
        assert isinstance(res, bool)
        # Invariant: Valid moisture must be in 0..100
        assert isinstance(moisture, (int, float)) and not isinstance(moisture, bool)
        assert math.isfinite(moisture) and 0.0 <= moisture <= 100.0
        # Invariant: Valid rain must be >= 0
        assert isinstance(rain_mm, (int, float)) and not isinstance(rain_mm, bool)
        assert math.isfinite(rain_mm) and rain_mm >= 0.0
        # Invariant: Stage must be a recognized string
        assert isinstance(stage, str) and stage.strip().lower() in ["seedling", "flowering", "vegetative", "fruiting", "mature"]
    except (ValueError, TypeError):
        # Graceful, expected rejection
        pass


# =====================================================================
# 2. Fuzz Testing water_volume()
# =====================================================================

@given(area_m2=fuzz_scalars, stage=fuzz_scalars, temp_c=fuzz_scalars)
@settings(max_examples=100)
def test_fuzz_water_volume_robustness(area_m2, stage, temp_c):
    """
    PROPERTY: water_volume must never return NaN, Inf, or negative numbers,
    must never silently accept invalid stages, and must strictly raise
    (ValueError, TypeError) on malformed inputs.
    """
    try:
        vol = water_volume(area_m2, stage, temp_c)
        # Invariant: Volume must be a finite positive number
        assert isinstance(vol, (int, float)) and not isinstance(vol, bool)
        assert math.isfinite(vol) and vol > 0.0
        # Invariant: Stage must be recognized (buggy script silently accepts unknown stage as 4L!)
        assert isinstance(stage, str) and stage.strip().lower() in ["seedling", "flowering", "vegetative", "fruiting", "mature"]
        # Invariant: Area must be finite positive
        assert isinstance(area_m2, (int, float)) and not isinstance(area_m2, bool)
        assert math.isfinite(area_m2) and area_m2 > 0.0
    except (ValueError, TypeError):
        # Graceful, expected rejection
        pass


# =====================================================================
# 3. Fuzz Testing schedule()
# =====================================================================

fuzz_zones = st.one_of(
    st.none(),
    st.integers(),
    st.text(),
    st.lists(
        st.one_of(
            st.tuples(st.text(), fuzz_scalars, fuzz_scalars, fuzz_scalars, fuzz_scalars, fuzz_scalars),
            st.tuples(st.text()), # malformed length
            st.none(),
        ),
        max_size=10
    )
)

@given(zones=fuzz_zones, budget=fuzz_scalars)
@settings(max_examples=100)
def test_fuzz_schedule_robustness(zones, budget):
    """
    PROPERTY: schedule must never crash on malformed zone structures,
    NoneType objects, or invalid budgets.
    """
    try:
        plan = schedule(zones, budget)
        assert isinstance(plan, list)
        assert all(isinstance(name, str) for name in plan)
        # Invariant: Valid budget must be non-negative finite number
        assert isinstance(budget, (int, float)) and not isinstance(budget, bool)
        assert math.isfinite(budget) and budget >= 0.0
    except (ValueError, TypeError):
        # Graceful, expected rejection
        pass
