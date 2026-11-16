# L6_L7_37 — Irrigation Scheduler

**Course:** Software Engineering (UE22CS341AA)  
**Student:** Shivansh Sharma (PES2UG24CS474)  
**Section:** H | **Semester:** V  
**Institution:** PES University, Bengaluru  

---

## Repository Structure

This repository contains the laboratory implementations and testing suites for Scenario 37 (Irrigation Scheduler):

### [Lab 6: Code and Branch Coverage Analysis](lab6/)
- Module: [`lab6/irrigation_scheduler.py`](lab6/irrigation_scheduler.py)
- Statement Coverage Tests: [`lab6/CodeCoverageTest_irrigation_scheduler.py`](lab6/CodeCoverageTest_irrigation_scheduler.py) (100% Line Coverage)
- Branch Coverage Tests: [`lab6/BranchCoverageTest_irrigation_scheduler.py`](lab6/BranchCoverageTest_irrigation_scheduler.py) (100% Branch Coverage)
- Primary Test Runner: [`lab6/test_irrigation_scheduler.py`](lab6/test_irrigation_scheduler.py)
- Technical Report: [`lab6/COVERAGE_REPORT.md`](lab6/COVERAGE_REPORT.md)
- Formal Report: [`lab6/PES2UG24CS474_SE_LAB6.pdf`](lab6/PES2UG24CS474_SE_LAB6.pdf)
- Terminal Screenshots: [`lab6/screenshots/`](lab6/screenshots/)

### [Lab 7: Fuzzing for Input Validation Bugs](lab7/)
- Hardened Application: [`lab7/processor.py`](lab7/processor.py) / [`lab7/irrigation_scheduler.py`](lab7/irrigation_scheduler.py)
- Buggy Application (Baseline): [`lab7/buggy_processor.py`](lab7/buggy_processor.py) / [`lab7/buggy_irrigation_scheduler.py`](lab7/buggy_irrigation_scheduler.py)
- Hypothesis Fuzz Test Suite: [`lab7/test_processor.py`](lab7/test_processor.py) / [`lab7/test_irrigation_scheduler.py`](lab7/test_irrigation_scheduler.py) (12 passed, 100% success)
- Buggy Test Runner: [`lab7/test_buggy_processor.py`](lab7/test_buggy_processor.py) (Demonstrates 3 failures with shrinking)
- Technical Report: [`lab7/FUZZING_REPORT.md`](lab7/FUZZING_REPORT.md)
- Formal Report: [`lab7/PES2UG24CS474_SE_LAB7.pdf`](lab7/PES2UG24CS474_SE_LAB7.pdf)
- Terminal Screenshots: [`lab7/screenshots/`](lab7/screenshots/)
