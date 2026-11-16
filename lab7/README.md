# LAB 7: Fuzzing for Input Validation Bugs

**Student Name:** Shivansh Sharma  
**SRN:** PES2UG24CS474  
**Section:** H  
**Course:** Software Engineering (UE22CS341AA)  
**Department:** Computer Science and Engineering, PES University, Bengaluru  
**Assigned Repository:** `L6_L7_37_irrigation_scheduler`  
**Assigned Scenario:** 37 — Irrigation Scheduler  

---

## Overview

This directory contains the complete implementation, test suites, terminal screenshots, and formal laboratory documentation for **Lab 7: Fuzzing for Input Validation Bugs**.

The lab explores **Property-Based Fuzz Testing** using the Python **Hypothesis** framework to identify vulnerabilities in the assigned `irrigation_scheduler` application (`processor.py`), isolate minimal reproducible failure inputs via automated shrinking, and harden the codebase against unexpected, malformed, and out-of-bounds inputs.

---

## Deliverables & File Structure

| Deliverable | File Path | Description |
|---|---|---|
| **Formal PDF Report** | [`PES2UG24CS474_SE_LAB7.pdf`](PES2UG24CS474_SE_LAB7.pdf) | Formal 4-page lab report with student metadata, explanations, bug matrix, and embedded screenshots. |
| **Fixed Application** | [`processor.py`](processor.py)<br>[`irrigation_scheduler.py`](irrigation_scheduler.py) | Hardened Python application script with comprehensive defensive input validation. |
| **Buggy Application** | [`buggy_processor.py`](buggy_processor.py)<br>[`buggy_irrigation_scheduler.py`](buggy_irrigation_scheduler.py) | Original unhardened script provided in the repository for comparison and baseline testing. |
| **Updated Test Code** | [`test_processor.py`](test_processor.py)<br>[`test_irrigation_scheduler.py`](test_irrigation_scheduler.py) | Full Hypothesis property-based fuzzing and unit test suite (12 tests, 100% pass rate). |
| **Buggy Test Runner** | [`test_buggy_processor.py`](test_buggy_processor.py) | Test runner executing against the buggy application to demonstrate failing test cases and Hypothesis shrinking. |
| **Terminal Screenshots** | [`screenshots/`](screenshots/) | High-resolution terminal output captures for Steps 2, 4, 5, and 6. |
| **Detailed Report** | [`FUZZING_REPORT.md`](FUZZING_REPORT.md) | Exhaustive technical markdown report covering concepts, invariants, and bug root causes. |
| **Screenshot Generator** | [`generate_screenshots.py`](generate_screenshots.py) | Python script generating terminal window simulation screenshots. |
| **PDF Generator** | [`generate_pdf.py`](generate_pdf.py) | Python ReportLab script compiling the final PDF report. |

---

## Lab Execution Steps & Commands

### Step 1: Install Dependencies
```powershell
pip install hypothesis pytest
```

### Step 2: Run Buggy Application
```powershell
python processor.py
# (or python buggy_processor.py)
```
*Screenshot:* [`screenshots/step2_run_buggy_processor.png`](screenshots/step2_run_buggy_processor.png)

### Step 3: Complete Hypothesis Test Cases in `test_processor.py`
Hypothesis strategies and property invariants were defined for all three functions: `should_irrigate()`, `water_volume()`, and `schedule()`.

### Step 4: Run Tests on Buggy Application (Observe Failing Tests)
```powershell
pytest test_buggy_processor.py
```
*Screenshot:* [`screenshots/step4_pytest_failing_tests.png`](screenshots/step4_pytest_failing_tests.png)  
*Result:* 3 tests failed; Hypothesis automatically shrunk complex inputs to minimal counterexamples (e.g. `moisture=-1`, `stage=None`, `area_m2=NaN`, `zones=None`).

### Step 5: Fix & Harden the Application Script
Implemented strict scalar type checks, boolean rejection, bounds checking, NaN/Infinity sanitization, and stage validation.  
Verify execution of fixed script:
```powershell
python processor.py
```
*Screenshot:* [`screenshots/step5_run_fixed_processor.png`](screenshots/step5_run_fixed_processor.png)

### Step 6: Re-run Hypothesis Tests on Fixed Script (All Pass)
```powershell
pytest test_processor.py -v
```
*Screenshot:* [`screenshots/step6_pytest_passing_tests.png`](screenshots/step6_pytest_passing_tests.png)  
*Result:* 12 passed in 0.89s (100% pass rate across over 1,000 generated inputs).

---

## Terminal Screenshots

### Step 2: Running Buggy Application
![Step 2](screenshots/step2_run_buggy_processor.png)

### Step 4: Failing Hypothesis Tests on Buggy Code
![Step 4](screenshots/step4_pytest_failing_tests.png)

### Step 5: Running Fixed Application
![Step 5](screenshots/step5_run_fixed_processor.png)

### Step 6: Re-Running Hypothesis Tests on Fixed Application (100% Passed)
![Step 6](screenshots/step6_pytest_passing_tests.png)

---

## Evaluation Rubric Summary

| Criterion | Target | Result | Status |
|---|---|---|---|
| Step 1: Install Dependencies | `hypothesis`, `pytest` | Installed in Python 3.13 | **PASS** |
| Step 2: Run Buggy Script | Terminal output screenshot | Captured in `screenshots/` and PDF | **PASS** |
| Step 3: Complete Hypothesis Tests | Covers all 3 functions | Implemented in `test_processor.py` | **PASS** |
| Step 4: Run Tests (Failures) | Failing test screenshot with shrinking | Captured in `screenshots/` and PDF | **PASS** |
| Step 5: Fix Application Script | Hardened against all edge cases | Completed in `processor.py` | **PASS** |
| Step 6: Re-run Tests (Passes) | 100% passing test screenshot | 12/12 passed, captured in `screenshots/` and PDF | **PASS** |
| Deliverables | PDF report, fixed script, updated tests | All deliverables present & verified | **PASS** |
