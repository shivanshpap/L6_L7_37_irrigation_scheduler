# Lab 7: Fuzzing for Input Validation Bugs — Comprehensive Report

**Student Name:** Shivansh Sharma  
**SRN:** PES2UG24CS474  
**Section:** H  
**Semester:** V  
**Course:** Software Engineering (UE22CS341AA)  
**Assigned Repository:** `L6_L7_37_irrigation_scheduler`  
**Application Under Test:** `processor.py` / `irrigation_scheduler.py`  
**Fuzz Testing Framework:** Hypothesis 6.170.15 with pytest 9.1.1  

---

## 1. Executive Summary

This laboratory investigates **Fuzz Testing (Property-Based Testing)** as an essential dynamic verification and security hardening technique. Using Python's **Hypothesis** library, the domain-specific **Irrigation Scheduler** application (`processor.py` / `irrigation_scheduler.py`) was subjected to automated input fuzzing.

While the baseline buggy application operated without issue under standard "happy-path" inputs, property-based fuzzing uncovered **7 severe input validation vulnerabilities**, including unhandled type conversions, negative physical quantities, IEEE 754 NaN bypasses, and structural unpacking failures.

The application was subsequently hardened via defensive programming principles, including strict scalar type checking, boundary enforcement, NaN/Infinity sanitization, and stage normalization. Re-running the Hypothesis fuzz suite achieved **100% test passage** across all 12 test suites with over 1,000 generated input permutations.

---

## 2. Core Concepts: Fuzzing & Hypothesis

### 2.1 What is Fuzz Testing?
Fuzz testing is a dynamic software testing methodology that automatically provides invalid, unexpected, or random data as inputs to a program. Its primary objectives are to:
- Detect unhandled exceptions and crashes before software deployment.
- Identify edge-case input boundary violations.
- Eliminate input validation vulnerabilities that could lead to Denial of Service (DoS) or security exploits.

### 2.2 Example-Based Testing vs. Property-Based Fuzzing
| Dimension | Traditional Unit Testing (pytest / unittest) | Property-Based Fuzzing (Hypothesis) |
|---|---|---|
| **Test Case Authoring** | Developer writes concrete input-output pairs manually. | Developer defines universal properties and input generators. |
| **Input Coverage** | Limited to scenarios envisioned by the test author. | Probes thousands of random, boundary, and pathological inputs. |
| **Cognitive Bias** | Highly susceptible to developer blind spots. | Actively searches for edge cases that break specifications. |
| **Failure Analysis** | Shows failure only for the exact hard-coded input. | Automatically **shrinks** inputs to the minimal failing case. |

### 2.3 Universal Properties Defined for Irrigation Scheduler
1. **Safety / Robustness Invariant:** For any arbitrary input $x$, $f(x)$ must either execute correctly and return a valid result conforming to the expected return type, or explicitly raise a documented validation error (`ValueError`, `TypeError`). It must never terminate with unexpected exceptions (`IndexError`, unhandled `TypeError`, etc.).
2. **Moisture Range Invariant:** Valid soil moisture must satisfy $0.0 \le \text{moisture} \le 100.0\%$.
3. **Precipitation Non-Negativity Invariant:** Valid rainfall must satisfy $\text{rain\_mm} \ge 0.0\text{ mm}$.
4. **Area Positivity Invariant:** Irrigated field area must be strictly positive: $\text{area\_m2} > 0.0\text{ m}^2$.
5. **Temperature Boundary Invariant:** Ambient temperature must lie within physically plausible environmental extremes: $-50.0^\circ\text{C} \le \text{temp\_c} \le 60.0^\circ\text{C}$.
6. **Water Budget Conservation Invariant:** In `schedule(zones, budget)`, the total volume of water allocated to scheduled zones must never exceed the available budget:
   $$\sum_{z \in \text{scheduled}} \text{water\_volume}(z) \le \text{budget}$$
7. **Volume Proportionality Invariant:** For any valid stage and temperature, doubling the land area doubles the required water volume:
   $$\text{water\_volume}(2 \times A, S, T) = 2 \times \text{water\_volume}(A, S, T)$$

---

## 3. Application Architecture & Buggy Source Code Analysis

The target application module (`processor.py` / `irrigation_scheduler.py`) encapsulates three core agronomic functions:

### 3.1 `should_irrigate(moisture, rain_mm, stage)`
- **Purpose:** Evaluates whether a field zone requires active watering based on current moisture, recent rainfall, and crop growth stage.
- **Original Vulnerabilities:**
  - Performs direct numerical comparisons (e.g. `moisture >= 60`) without checking input types. Passing `None` or string values causes unhandled `TypeError: '>=' not supported between instances of 'NoneType' and 'int'`.
  - Accepts negative rainfall and negative moisture values, violating physical domain constraints.
  - Silently accepts unrecognized stage strings (e.g. `"INVALID"` or `None`) and falls through to the generic default branch without raising an error.

### 3.2 `water_volume(area_m2, stage, temp_c)`
- **Purpose:** Calculates the exact water volume (in Litres) required for a zone given its area, crop growth stage, and ambient temperature.
- **Original Vulnerabilities:**
  - Only checks `if area_m2 <= 0: raise ValueError(...)`. In Python, `float('nan') <= 0` evaluates to `False`. Thus, NaN values silently bypass the check and propagate into calculations, yielding NaN litres.
  - Non-numeric inputs for `area_m2` or `temp_c` cause unhandled `TypeError` exceptions.
  - Any unrecognized crop stage silently falls into `litres = 4` without validation.
  - Temperatures are unconstrained, accepting unrealistic values (e.g., $1000^\circ\text{C}$ or $-500^\circ\text{C}$).

### 3.3 `schedule(zones, budget)`
- **Purpose:** Performs greedy scheduling of zone irrigation within an allocated water budget.
- **Original Vulnerabilities:**
  - Assumes `zones` is an iterable of 6-tuples. If `zones` is `None` or an integer, it raises `TypeError: 'NoneType' object is not iterable`.
  - If a zone record has fewer or more than 6 elements, it crashes with unhandled `ValueError: not enough values to unpack`.
  - If `budget` is `None` or non-numeric, it crashes on `need > budget`.
  - Accepts negative budgets or NaN budgets, leading to non-deterministic scheduling behavior.

---

## 4. Hypothesis Fuzz Testing Design

To expose these vulnerabilities automatically, the test suite `test_processor.py` utilized Hypothesis's `strategies` (`st`) module:

```python
fuzz_scalars = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-1000, max_value=1000),
    st.floats(allow_nan=True, allow_infinity=True, width=32),
    st.text(max_size=25),
)
```

### Automated Shrinking Demonstrated
When executed against `buggy_processor.py`, Hypothesis immediately detected multiple invariant violations and shrank them to minimal counterexamples:

1. **`should_irrigate` Failure:**
   - **Counterexample Found:** `moisture=-1, rain_mm=False, stage=None`
   - **Root Cause:** Accepted negative moisture; accepted boolean for rainfall; failed type check on stage.
2. **`water_volume` Failure:**
   - **Counterexample Found:** `area_m2=float('nan'), stage='unknown_crop', temp_c=25.0`
   - **Root Cause:** NaN bypassed `<=` check; invalid crop stage silently allocated 4 L/m2.
3. **`schedule` Failure:**
   - **Counterexample Found:** `zones=None, budget=100.0`
   - **Root Cause:** Direct unvalidated iteration crashed with unhandled `TypeError`.

---

## 5. Comprehensive Bug Finding & Hardening Matrix

| Target Function | Fuzz Input Trigger | Buggy Behavior / Crash | Root Cause in Starter Code | Defensive Hardening Fix |
|---|---|---|---|---|
| `should_irrigate()` | `moisture = None`<br/>`moisture = "high"` | Unhandled `TypeError: '>=' not supported between NoneType and int` | Missing type verification prior to numeric comparisons | Implemented `_validate_number()` rejecting non-numeric types and booleans |
| `should_irrigate()` | `moisture = -1.0`<br/>`rain_mm = -5.0` | Accepted negative values; returned illogical `True` | No physical lower bound checks on moisture or rain | Enforced `0.0 <= moisture <= 100.0` and `rain_mm >= 0.0` |
| `should_irrigate()` | `stage = None`<br/>`stage = "garlic"` | Silently treated unrecognized stage as other; returned flawed bool | Lack of membership checking against known crop stages | Enforced membership in `VALID_STAGES` set; raised `ValueError` |
| `water_volume()` | `area_m2 = float('nan')` | Bypassed `area_m2 <= 0`; returned `nan` volume | IEEE 754 NaN comparisons always evaluate to `False` | Enforced `math.isfinite()` check rejecting NaN and Infinity |
| `water_volume()` | `stage = None`<br/>`stage = "unknown"` | Silently allocated 4 L/m2 via fallback `else` branch | No stage validation prior to base rate selection | Enforced `_validate_stage()` before rate lookup |
| `schedule()` | `zones = None`<br/>`zones = 42` | Unhandled `TypeError: 'NoneType' object is not iterable` | Blind `for ... in zones:` iteration | Verified iterable container type; raised `TypeError` on scalars |
| `schedule()` | `zones = [("Z1", 100)]` (malformed tuple) | Unhandled `ValueError: not enough values to unpack` | Blind 6-variable unpacking in loop statement | Validated `isinstance(item, (tuple, list))` and `len(item) == 6` |
| `schedule()` | `budget = -50.0`<br/>`budget = None` | Unhandled `TypeError` or erroneous greedy allocations | No validation on budget parameter | Enforced `budget >= 0.0` and finite numeric type |

---

## 6. Defensive Hardening Implementation

The hardened application `processor.py` integrates comprehensive input sanitization routines:

```python
def _validate_number(val: Any, name: str, min_val: float = None, max_val: float = None, allow_zero: bool = True) -> float:
    # Explicitly reject booleans (which subclass int in Python)
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
```

---

## 7. Verification & Test Execution Results

### 7.1 Execution Commands
```powershell
# 1. Execute baseline application
python processor.py

# 2. Run Hypothesis tests against buggy code (demonstrates 3 failures)
pytest test_buggy_processor.py

# 3. Run Hypothesis tests against hardened code (demonstrates 12 passes)
pytest test_processor.py -v
```

### 7.2 Results Summary
```
============================= test session starts =============================
platform win32 -- Python 3.13.0, pytest-9.1.1, pluggy-1.6.0
hypothesis profile 'default' (version 6.170.15)
rootdir: C:\Users\SHIVANSH\Documents\sem-V l\labs\SE\lab-7
collected 12 items

test_processor.py::test_fuzz_should_irrigate_safety PASSED               [  8%]
test_processor.py::test_should_irrigate_properties_on_valid_inputs PASSED [ 16%]
test_processor.py::test_fuzz_water_volume_safety PASSED                  [ 25%]
test_processor.py::test_water_volume_proportionality PASSED              [ 33%]
test_processor.py::test_fuzz_schedule_safety PASSED                      [ 41%]
test_processor.py::test_schedule_budget_invariant PASSED                 [ 50%]
test_processor.py::test_should_irrigate_happy_path PASSED                [ 58%]
test_processor.py::test_should_irrigate_edge_case_rejections PASSED       [ 66%]
test_processor.py::test_water_volume_happy_path PASSED                   [ 75%]
test_processor.py::test_water_volume_edge_case_rejections PASSED         [ 83%]
test_processor.py::test_schedule_happy_path PASSED                       [ 91%]
test_processor.py::test_schedule_edge_case_rejections PASSED             [100%]

============================= 12 passed in 0.89s ==============================
```

All 12 test suites passed cleanly with 0 errors and 0 warnings.
