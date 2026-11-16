"""
Hardened Application Script: Irrigation Scheduler (Processor)
Course: Software Engineering (UE22CS341AA) - Lab 7: Fuzzing for Input Validation Bugs
Scenario 37: Irrigation Scheduler
Student: Shivansh Sharma (PES2UG24CS474)

Hardened against input validation bugs and edge cases uncovered via Hypothesis fuzz testing.
Implements defensive programming:
  1. Strict type checking (rejecting booleans as ints/floats, non-iterables, None).
  2. Range validation (soil moisture 0-100%, rainfall >= 0, temperature -50 to 60 C, area > 0, budget >= 0).
  3. Handling of IEEE 754 special values (rejection of NaN and +/- Infinity).
  4. String normalization and validation for crop stages.
  5. Structural validation of zone tuples/lists.
"""

import math
from typing import List, Tuple, Sequence, Any, Union

# Recognized crop growth stages
VALID_STAGES = {"seedling", "flowering", "vegetative", "fruiting", "mature"}


def _validate_number(val: Any, name: str, min_val: float = None, max_val: float = None, allow_zero: bool = True) -> float:
    """
    Validate that val is a real finite number within optional bounds.
    Rejects booleans (since in Python bool subclasses int), None, and non-numeric types.
    Rejects NaN and Infinity.
    """
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise TypeError(f"'{name}' must be a numeric value (int or float), got {type(val).__name__}")
    if not math.isfinite(val):
        raise ValueError(f"'{name}' must be a finite number, got {val}")
    if min_val is not None:
        if allow_zero:
            if val < min_val:
                raise ValueError(f"'{name}' must be >= {min_val}, got {val}")
        else:
            if val <= min_val:
                raise ValueError(f"'{name}' must be > {min_val}, got {val}")
    if max_val is not None and val > max_val:
        raise ValueError(f"'{name}' must be <= {max_val}, got {val}")
    return float(val)


def _validate_stage(stage: Any) -> str:
    """Validate and normalize crop growth stage."""
    if not isinstance(stage, str):
        raise TypeError(f"'stage' must be a string, got {type(stage).__name__}")
    norm = stage.strip().lower()
    if not norm:
        raise ValueError("'stage' cannot be empty or whitespace only")
    if norm not in VALID_STAGES:
        raise ValueError(f"unrecognized crop stage '{stage}'. Supported stages: {sorted(list(VALID_STAGES))}")
    return norm


def should_irrigate(moisture: Any, rain_mm: Any, stage: Any) -> bool:
    """
    Decides whether an agricultural field zone requires irrigation.
    
    Validates:
      - moisture: Soil moisture percentage, finite number in [0.0, 100.0]
      - rain_mm: Recent rainfall in millimeters, finite number >= 0.0
      - stage: Crop growth stage string, must be one of VALID_STAGES
      
    Returns:
      bool: True if irrigation should occur, False otherwise.
    """
    moist = _validate_number(moisture, "moisture", min_val=0.0, max_val=100.0)
    rain = _validate_number(rain_mm, "rain_mm", min_val=0.0)
    stg = _validate_stage(stage)

    if moist >= 60.0:
        return False
    if rain >= 10.0:
        return False
    if stg == "seedling":
        if moist < 45.0:
            return True
        return False
    if stg == "flowering":
        return moist < 55.0
    if rain >= 5.0:
        return False
    return moist < 40.0


def water_volume(area_m2: Any, stage: Any, temp_c: Any) -> float:
    """
    Calculates total water required (in Litres) for a given zone area, crop stage, and temperature.
    
    Validates:
      - area_m2: Positive finite number > 0.0
      - stage: Valid crop stage string
      - temp_c: Temperature in Celsius, finite number in [-50.0, 60.0]
      
    Returns:
      float: Volume of water required in litres.
    """
    area = _validate_number(area_m2, "area_m2", min_val=0.0, allow_zero=False)
    stg = _validate_stage(stage)
    temp = _validate_number(temp_c, "temp_c", min_val=-50.0, max_val=60.0)

    if stg == "seedling":
        litres = 2.0
    elif stg == "flowering":
        litres = 5.0
    else:
        litres = 4.0

    if temp > 35.0:
        litres = litres * 1.5
    elif temp < 10.0:
        litres = litres * 0.5

    return area * litres


def schedule(zones: Any, budget: Any) -> List[str]:
    """
    Greedy scheduling of irrigation for zones within a given water budget.
    
    Validates:
      - zones: Iterable sequence of 6-element zone records (name, area, moisture, rain, stage, temp)
      - budget: Finite number >= 0.0
      
    Returns:
      List[str]: Names of zones scheduled for irrigation.
    """
    if zones is None or not hasattr(zones, "__iter__") or isinstance(zones, (str, bytes, dict)):
        raise TypeError("'zones' must be an iterable sequence of zone tuples/lists")
    
    bgt = _validate_number(budget, "budget", min_val=0.0)
    
    plan: List[str] = []
    for idx, item in enumerate(zones):
        if not isinstance(item, (tuple, list)):
            raise TypeError(f"Zone at index {idx} must be a tuple or list, got {type(item).__name__}")
        if len(item) != 6:
            raise ValueError(f"Zone at index {idx} must have exactly 6 elements (name, area, moisture, rain, stage, temp), got {len(item)}")
        
        name, area, moisture, rain, stage, temp = item
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Zone name at index {idx} must be a non-empty string, got {name!r}")
        
        if not should_irrigate(moisture, rain, stage):
            continue
        
        need = water_volume(area, stage, temp)
        if need > bgt:
            break
        bgt -= need
        plan.append(name.strip())
        
    return plan


if __name__ == "__main__":
    print("=" * 65)
    print("   IRRIGATION SCHEDULER (HARDENED / FIXED APPLICATION)")
    print("   Scenario 37 - PES University SE Lab 7: Fuzz Testing")
    print("   Student: Shivansh Sharma | SRN: PES2UG24CS474")
    print("=" * 65)
    
    sample_zones = [
        ("North-Paddock", 120.0, 32.0, 2.0, "seedling", 24.0),
        ("South-Orchard", 250.0, 52.0, 0.0, "flowering", 29.0),
        ("East-Greenhouse", 85.0, 18.0, 7.0, "vegetative", 16.0),
        ("West-Vineyard", 180.0, 38.0, 1.0, "vegetative", 36.0),
    ]
    water_budget = 2500.0

    print(f"\n[+] Configured Water Budget: {water_budget:.1f} Litres")
    print(f"[+] Total Registered Zones: {len(sample_zones)}\n")
    print(f"{'Zone Name':<18} {'Area (m2)':<10} {'Moist(%)':<10} {'Rain(mm)':<10} {'Stage':<12} {'Temp(C)':<8} {'Irrigate?':<10}")
    print("-" * 80)
    for z in sample_zones:
        irr = should_irrigate(z[2], z[3], z[4])
        print(f"{z[0]:<18} {z[1]:<10.1f} {z[2]:<10.1f} {z[3]:<10.1f} {z[4]:<12} {z[5]:<8.1f} {str(irr):<10}")

    print("\n[+] Running schedule() optimization plan...")
    scheduled_plan = schedule(sample_zones, water_budget)
    print(f"[+] Final Irrigation Plan: {scheduled_plan}")
    print("=" * 65)
    print("[+] VERIFICATION: All inputs strictly validated and hardened against")
    print("    fuzz testing edge cases, non-numeric types, NaN, Inf, and bounds.")
    print("=" * 65)
