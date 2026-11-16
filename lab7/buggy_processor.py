"""
Buggy Application Script: Irrigation Scheduler (Processor)
Course: Software Engineering (UE22CS341AA) - Lab 7: Fuzzing for Input Validation Bugs
Scenario 37: Irrigation Scheduler
Student: Shivansh Sharma (PES2UG24CS474)

This script contains the original, unhardened logic provided in the repository.
It lacks input validation, defensive type-checking, and bounds enforcement,
leaving it vulnerable to unhandled exceptions, crashes, and logical anomalies
when subjected to edge-case or malformed inputs discovered via Hypothesis fuzzing.
"""

def should_irrigate(moisture, rain_mm, stage):
    """
    Decides whether an agricultural field zone requires irrigation.
    BUG: Fails on non-numeric types, negative rainfall/moisture, None, NaN,
    or unrecognized stage strings.
    """
    if moisture >= 60:
        return False
    if rain_mm >= 10:
        return False
    if stage == "seedling":
        if moisture < 45:
            return True
        return False
    if stage == "flowering":
        return moisture < 55
    if rain_mm >= 5:
        return False
    return moisture < 40


def water_volume(area_m2, stage, temp_c):
    """
    Calculates total water required (in Litres) for a given zone area.
    BUG: Only checks area_m2 <= 0. Fails on None/non-numeric area or temp,
    NaN (bypasses <= 0 check), extreme temperatures, and silently defaults
    any unknown/invalid stage string to 4 litres.
    """
    if area_m2 <= 0:
        raise ValueError("invalid area")
    if stage == "seedling":
        litres = 2
    elif stage == "flowering":
        litres = 5
    else:
        litres = 4
    if temp_c > 35:
        litres = litres * 1.5
    elif temp_c < 10:
        litres = litres * 0.5
    return area_m2 * litres


def schedule(zones, budget):
    """
    Greedy scheduling of irrigation for zones within a given water budget.
    BUG: Crashes with TypeError if zones is None or non-iterable; crashes
    with ValueError on malformed zone tuples (wrong length); crashes with
    TypeError if budget is None; produces erratic behavior on negative or NaN budgets.
    """
    plan = []
    for name, area, moisture, rain, stage, temp in zones:
        if not should_irrigate(moisture, rain, stage):
            continue
        need = water_volume(area, stage, temp)
        if need > budget:
            break
        budget -= need
        plan.append(name)
    return plan


if __name__ == "__main__":
    print("=" * 65)
    print("   IRRIGATION SCHEDULER (BUGGY APPLICATION PROCESSOR)")
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
    print("[!] NOTICE: Buggy script runs on happy-path inputs, but crashes")
    print("    when presented with edge cases or malformed fuzz inputs.")
    print("=" * 65)
