# Lab 6: Code and Branch Coverage Analysis Report

**Student Name:** Shivansh Sharma  
**SRN:** PES2UG24CS474  
**Course:** Software Engineering (UE22CS341AA / Lab Component)  
**Assigned Repository:** `L6_L7_37_irrigation_scheduler`  
**Application Under Test:** `irrigation_scheduler.py`  

---

## 1. Executive Summary

This laboratory exercise analyzes and evaluates the difference between **Code Coverage (Statement Coverage)** and **Branch Coverage (Decision Coverage)** using Python's `coverage.py` library and `pytest`. 

A series of targeted unit test suites were developed for the `irrigation_scheduler` module:
1. **Initial Baseline:** The starter test suite covered only **29% statement coverage** and **24% branch coverage**.
2. **Phase 1 (Code Coverage):** Expanded test cases in `CodeCoverageTest_irrigation_scheduler.py` (and `CodeCoverageTest_xxxx_application.py`) achieved **100% statement coverage**. However, running branch analysis revealed that even with 100% line coverage, **branch coverage was 97%** because several decision outcomes (such as the default temperature branch and natural loop completion) remained unexercised.
3. **Phase 2 (Branch Coverage):** A comprehensive test suite in `BranchCoverageTest_irrigation_scheduler.py` (and `BranchCoverageTest_xxxx_application.py`) achieved **100% statement coverage** and **100% branch coverage** (all 28 branches fully exercised in both True and False outcomes, with 0 missing branches).

---

## 2. Theoretical Foundations

### 2.1 Coverage Metrics Defined
| Coverage Type | Formal Definition | Scope in Testing |
|---|---|---|
| **Line / Statement Coverage** | Measures the percentage of executable lines of source code executed at least once during test execution. | $\frac{\text{Executed Statements}}{\text{Total Executable Statements}} \times 100\%$ |
| **Branch / Decision Coverage** | Measures whether every control structure (e.g., `if`, `elif`, `else`, `for`) evaluates to all possible outcomes (both `True` and `False`). | $\frac{\text{Exercised Decision Outcomes}}{\text{Total Decision Outcomes}} \times 100\%$ |
| **Path Coverage** | Measures whether all possible distinct end-to-end execution paths through the code are executed. | Combinatorial product of all decision branches. |
| **Function Coverage** | Measures whether every declared function in the module was called during tests. | $\frac{\text{Invoked Functions}}{\text{Total Declared Functions}} \times 100\%$ |

### 2.2 Why Line Coverage Can Give a False Sense of Security
As demonstrated in the laboratory handout and verified empirically here, **100% line coverage does not guarantee thorough testing**:
- An `if` statement without an `else` might have its body executed (achieving 100% line coverage for that block), yet the scenario where the condition evaluates to `False` might never be tested.
- A `for` loop that always breaks early executes all statements in its body, yet the loop's normal exit condition (`35->43`) is never exercised.
- Temperature compensation in `water_volume` has branches for `temp_c > 35` and `temp_c < 10`. Executing only hot and cold temperatures passes through all calculation lines, leaving the nominal range (`10 <= temp_c <= 35`) untested as a decision branch (`28->30`).

---

## 3. Analysis of Application Under Test (`irrigation_scheduler.py`)

The module under test contains 38 executable statements organized into three functions:

### 3.1 `should_irrigate(moisture, rain_mm, stage)`
Decides whether an agricultural field zone requires irrigation based on soil moisture, rainfall, and crop growth stage.
- **Decision Points & Branches:**
  1. `moisture >= 60`:
     - `True` $\rightarrow$ returns `False` (line 3).
     - `False` $\rightarrow$ proceeds to rain check.
  2. `rain_mm >= 10`:
     - `True` $\rightarrow$ returns `False` (line 5).
     - `False` $\rightarrow$ proceeds to stage check.
  3. `stage == "seedling"`:
     - `True` $\rightarrow$ evaluates `if moisture < 45`:
       - `True` $\rightarrow$ returns `True` (line 8).
       - `False` $\rightarrow$ returns `False` (line 9).
     - `False` $\rightarrow$ proceeds to flowering check.
  4. `stage == "flowering"`:
     - `True` $\rightarrow$ returns `moisture < 55` (line 11).
     - `False` $\rightarrow$ proceeds to other stage check.
  5. `rain_mm >= 5`:
     - `True` $\rightarrow$ returns `False` (line 13).
     - `False` $\rightarrow$ returns `moisture < 40` (line 14).

### 3.2 `water_volume(area_m2, stage, temp_c)`
Calculates the volume of irrigation water in litres for a given field area, growth stage, and ambient temperature.
- **Decision Points & Branches:**
  1. `area_m2 <= 0`:
     - `True` $\rightarrow$ raises `ValueError("invalid area")` (line 19).
     - `False` $\rightarrow$ proceeds to stage base rate.
  2. `stage == "seedling"` vs. `elif stage == "flowering"` vs. `else`:
     - "seedling": `litres = 2` (line 21).
     - "flowering": `litres = 5` (line 23).
     - other stages: `litres = 4` (line 25).
  3. `temp_c > 35` vs. `elif temp_c < 10` vs. nominal:
     - `temp_c > 35`: `litres = litres * 1.5` (line 27).
     - `temp_c < 10`: `litres = litres * 0.5` (line 29).
     - `10 <= temp_c <= 35`: no multiplier applied (`28->30`).
  4. Returns `area_m2 * litres` (line 30).

### 3.3 `schedule(zones, budget)`
Iterates through agricultural zones, filters zones that need irrigation, calculates required water, and allocates within an aggregate water budget.
- **Decision Points & Branches:**
  1. `for name, area, moisture, rain, stage, temp in zones`:
     - Empty zones list $\rightarrow$ skips loop entirely and returns `[]`.
     - Normal loop completion $\rightarrow$ branch `35->43`.
  2. `if not should_irrigate(...)`:
     - `True` $\rightarrow$ `continue` (line 37).
     - `False` $\rightarrow$ calculates `need = water_volume(...)`.
  3. `if need > budget`:
     - `True` $\rightarrow$ `break` (line 40).
     - `False` $\rightarrow$ deducts `need` from `budget` and appends zone to plan (lines 41-42).

---

## 4. Test Design & Traceability Matrix

### 4.1 Phase 1: Code Coverage Suite (`CodeCoverageTest_irrigation_scheduler.py`)
Designed to execute every statement line at least once:

| Test Name | Targeted Lines | Outcome |
|---|---|---|
| `test_wet_soil_no_irrigation` | Lines 1–3 | Returns `False` when `moisture >= 60` |
| `test_heavy_rain_no_irrigation` | Lines 4–5 | Returns `False` when `rain_mm >= 10` |
| `test_seedling_needs_irrigation` | Lines 6–8 | Returns `True` when seedling and `moisture < 45` |
| `test_seedling_dry_enough_no_irrigation` | Line 9 | Returns `False` when seedling and `moisture >= 45` |
| `test_flowering_needs_irrigation` | Lines 10–11 | Returns `True` when flowering and `moisture < 55` |
| `test_other_stage_moderate_rain` | Lines 12–13 | Returns `False` when other stage and `rain_mm >= 5` |
| `test_other_stage_needs_irrigation` | Line 14 | Returns `True` when other stage and `moisture < 40` |
| `test_invalid_area_volume` | Lines 18–19 | Raises `ValueError` when `area_m2 <= 0` |
| `test_seedling_volume_high_temp` | Lines 20–21, 26–27, 30 | Seedling base litres with `temp_c > 35` |
| `test_flowering_volume_low_temp` | Lines 22–23, 28–30 | Flowering base litres with `temp_c < 10` |
| `test_other_stage_volume` | Lines 24–25, 26–27, 30 | Other stage base litres with `temp_c > 35` |
| `test_schedule_execution` | Lines 34–43 | Exercises continue, water calculation, break, deduction |

**Results:**
- Statement Coverage: **100%** (38/38 statements in `irrigation_scheduler.py`).
- Branch Coverage: **97%** (28 branches, 2 partial: `28->30`, `35->43`).

---

### 4.2 Phase 2: Complete Branch Coverage Suite (`BranchCoverageTest_irrigation_scheduler.py`)
Designed to evaluate every decision branch to both `True` and `False`, with rigorous boundary value analysis (BVA):

| Test Name | Function | Branch Condition & Input | Expected Output |
|---|---|---|---|
| `test_should_irrigate_moisture_ge_60_true` | `should_irrigate` | `moisture = 60` (boundary), `75` | `False` |
| `test_should_irrigate_moisture_ge_60_false` | `should_irrigate` | `moisture = 59` (boundary) | Proceeds to rain check |
| `test_should_irrigate_rain_ge_10_true` | `should_irrigate` | `rain_mm = 10` (boundary), `15` | `False` |
| `test_should_irrigate_rain_ge_10_false` | `should_irrigate` | `rain_mm = 9` (boundary) | Proceeds to stage check |
| `test_should_irrigate_stage_seedling_moisture_lt_45_true` | `should_irrigate` | `stage = 'seedling'`, `moisture = 44` (boundary), `30` | `True` |
| `test_should_irrigate_stage_seedling_moisture_lt_45_false` | `should_irrigate` | `stage = 'seedling'`, `moisture = 45` (boundary), `50` | `False` |
| `test_should_irrigate_stage_flowering_true` | `should_irrigate` | `stage = 'flowering'`, `moisture = 54` (boundary), `40` | `True` |
| `test_should_irrigate_stage_flowering_false` | `should_irrigate` | `stage = 'flowering'`, `moisture = 55` (boundary), `58` | `False` |
| `test_should_irrigate_other_stage_rain_ge_5_true` | `should_irrigate` | `stage = 'vegetative'`, `rain_mm = 5` (boundary), `8` | `False` |
| `test_should_irrigate_other_stage_moisture_lt_40_true` | `should_irrigate` | `stage = 'vegetative'`, `moisture = 39` (boundary), `25` | `True` |
| `test_should_irrigate_other_stage_moisture_lt_40_false` | `should_irrigate` | `stage = 'vegetative'`, `moisture = 40` (boundary), `50` | `False` |
| `test_water_volume_invalid_area_zero_and_negative` | `water_volume` | `area_m2 = 0` (boundary), `-10` | Raises `ValueError` |
| `test_water_volume_seedling_stage` | `water_volume` | `stage = 'seedling'`, `temp_c = 25` | `20.0` (2 L/m²) |
| `test_water_volume_flowering_stage` | `water_volume` | `stage = 'flowering'`, `temp_c = 25` | `50.0` (5 L/m²) |
| `test_water_volume_other_stage` | `water_volume` | `stage = 'vegetative'`, `temp_c = 25` | `40.0` (4 L/m²) |
| `test_water_volume_temp_gt_35` | `water_volume` | `temp_c = 36` (boundary), `40` | Multiplier 1.5x |
| `test_water_volume_temp_lt_10` | `water_volume` | `temp_c = 9` (boundary), `5` | Multiplier 0.5x |
| `test_water_volume_temp_normal_boundaries` | `water_volume` | `temp_c = 10`, `35` (boundaries), `20` | Multiplier 1.0x (branch `28->30`) |
| `test_schedule_empty_zones` | `schedule` | `zones = []` | Loop skips $\rightarrow$ `[]` |
| `test_schedule_all_zones_skip_irrigation` | `schedule` | All zones `should_irrigate == False` | `continue` $\rightarrow$ `[]` |
| `test_schedule_all_zones_fit_budget` | `schedule` | All zones fit budget | Normal completion $\rightarrow$ `35->43` |
| `test_schedule_budget_exhausted_break` | `schedule` | Zone 2 exceeds remaining budget | `break` (line 40) |
| `test_schedule_exact_budget_match` | `schedule` | `need == budget` | Appended, budget = 0 |

**Results:**
- Statement Coverage: **100%** (38/38 statements in `irrigation_scheduler.py`).
- Branch Coverage: **100%** (28/28 branches fully exercised, 0 partial branches, 0 missed).

---

## 5. Comparative Coverage Metrics

| Stage / Test Suite | Executable Statements | Missed Statements | Line Coverage | Total Branches | Partial / Missed Branches | Branch Coverage | Total Tests |
|---|---|---|---|---|---|---|---|
| **Starter Test** (`test_irrigation_scheduler.py`) | 38 | 27 | **29%** | 28 | 5 | **24%** | 2 |
| **Code Coverage Test** (`CodeCoverageTest_*.py`) | 38 | 0 | **100%** | 28 | 2 (`28->30`, `35->43`) | **97%** | 12 |
| **Branch Coverage Test** (`BranchCoverageTest_*.py`)| 38 | 0 | **100%** | 28 | 0 (None) | **100%** | 23 |

---

## 6. Git Commits and Deliverables

As specified in the lab evaluation rubric, the repository includes distinct commits:
- **Commit 1:** Added Code Coverage test suite (`CodeCoverageTest_irrigation_scheduler.py`, `CodeCoverageTest_xxxx_application.py`, and initial update to `test_irrigation_scheduler.py`) achieving 100% statement coverage, along with terminal screenshots `screenshots/code_coverage_line_report.png` and `screenshots/code_coverage_branch_report.png`.
- **Commit 2:** Added Branch Coverage test suite (`BranchCoverageTest_irrigation_scheduler.py`, `BranchCoverageTest_xxxx_application.py`, and updated `test_irrigation_scheduler.py`) achieving 100% branch coverage, along with terminal screenshot `screenshots/branch_coverage_report.png`, formal PDF report, and updated documentation.

---

## 7. Execution Guide

To reproduce the coverage analysis locally:

```powershell
# Navigate to lab6 directory
cd lab6

# Run line coverage for Code Coverage suite
coverage erase
coverage run -m pytest CodeCoverageTest_irrigation_scheduler.py
coverage report -m

# Run branch coverage for Code Coverage suite (shows unexercised branches)
coverage erase
coverage run --branch -m pytest CodeCoverageTest_irrigation_scheduler.py
coverage report -m

# Run 100% branch coverage suite
coverage erase
coverage run --branch -m pytest BranchCoverageTest_irrigation_scheduler.py
coverage report -m
```
