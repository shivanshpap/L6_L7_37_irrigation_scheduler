"""
Hardened Application Script: Irrigation Scheduler (Processor)
Course: Software Engineering (UE22CS341AA) - Lab 7: Fuzzing for Input Validation Bugs
Scenario 37: Irrigation Scheduler
Student: Shivansh Sharma (PES2UG24CS474)

Hardened against input validation bugs and edge cases uncovered via Hypothesis fuzz testing.
"""

from processor import (
    VALID_STAGES,
    _validate_number,
    _validate_stage,
    should_irrigate,
    water_volume,
    schedule,
)

if __name__ == "__main__":
    import processor
    # Run the main demo
    processor.__name__ = "__main__"
    import sys
    sys.exit(0)
