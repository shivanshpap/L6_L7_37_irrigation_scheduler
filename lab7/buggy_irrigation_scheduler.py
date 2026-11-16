"""
Buggy Application Script: Irrigation Scheduler (Scenario 37)
Course: Software Engineering (UE22CS341AA) - Lab 7: Fuzzing for Input Validation Bugs
Student: Shivansh Sharma (PES2UG24CS474)
"""

from buggy_processor import (
    should_irrigate,
    water_volume,
    schedule,
)

if __name__ == "__main__":
    import subprocess
    import sys
    sys.exit(subprocess.call([sys.executable, "buggy_processor.py"]))
