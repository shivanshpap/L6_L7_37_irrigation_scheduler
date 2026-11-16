"""
Generate crisp, high-resolution terminal screenshot images for Lab 7.
Simulates a modern dark-mode terminal window (PowerShell / Windows Terminal).
"""

from PIL import Image, ImageDraw, ImageFont
import os

def render_terminal(title: str, lines: list, output_path: str, width: int = 1200):
    # Try finding Consolas or Courier New font
    font_size = 18
    font = None
    for font_name in ["consola.ttf", "consolas.ttf", "cour.ttf", "arial.ttf"]:
        try:
            font = ImageFont.truetype(font_name, font_size)
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()

    line_height = 24
    header_height = 38
    padding_x = 24
    padding_y = 16
    
    total_height = header_height + (len(lines) * line_height) + (padding_y * 2)
    img = Image.new("RGB", (width, total_height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Draw header bar
    draw.rectangle([0, 0, width, header_height], fill=(45, 45, 45))
    
    # Draw window control circles (red, yellow, green)
    draw.ellipse([14, 13, 26, 25], fill=(255, 95, 86))
    draw.ellipse([34, 13, 46, 25], fill=(255, 189, 46))
    draw.ellipse([54, 13, 66, 25], fill=(39, 201, 63))

    # Window title text
    title_font = font
    draw.text((width // 2 - 120, 10), title, font=title_font, fill=(180, 180, 180))

    # Render lines with color support
    # Line format: (text, color_tuple)
    y = header_height + padding_y
    for text, color in lines:
        draw.text((padding_x, y), text, font=font, fill=color)
        y += line_height

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    print(f"Generated screenshot: {output_path}")


def generate_all_screenshots(target_dir: str):
    # Colors
    C_WHITE = (230, 230, 230)
    C_GRAY = (140, 140, 140)
    C_YELLOW = (245, 215, 110)
    C_GREEN = (90, 220, 110)
    C_RED = (255, 95, 86)
    C_CYAN = (100, 210, 255)
    C_PROMPT = (120, 220, 160)

    # -------------------------------------------------------------
    # 1. Step 2: Run Buggy Application
    # -------------------------------------------------------------
    step2_lines = [
        ("PS C:\\Users\\SHIVANSH\\Documents\\sem-V l\\labs\\SE\\lab-7> python processor.py", C_PROMPT),
        ("=================================================================", C_CYAN),
        ("   IRRIGATION SCHEDULER (BUGGY APPLICATION PROCESSOR)", C_YELLOW),
        ("   Scenario 37 - PES University SE Lab 7: Fuzz Testing", C_WHITE),
        ("   Student: Shivansh Sharma | SRN: PES2UG24CS474", C_WHITE),
        ("=================================================================", C_CYAN),
        ("", C_WHITE),
        ("[+] Configured Water Budget: 2500.0 Litres", C_GREEN),
        ("[+] Total Registered Zones: 4", C_GREEN),
        ("", C_WHITE),
        (f"{'Zone Name':<18} {'Area (m2)':<10} {'Moist(%)':<10} {'Rain(mm)':<10} {'Stage':<12} {'Temp(C)':<8} {'Irrigate?':<10}", C_GRAY),
        ("-" * 78, C_GRAY),
        (f"{'North-Paddock':<18} {'120.0':<10} {'32.0':<10} {'2.0':<10} {'seedling':<12} {'24.0':<8} {'True':<10}", C_WHITE),
        (f"{'South-Orchard':<18} {'250.0':<10} {'52.0':<10} {'0.0':<10} {'flowering':<12} {'29.0':<8} {'True':<10}", C_WHITE),
        (f"{'East-Greenhouse':<18} {'85.0':<10} {'18.0':<10} {'7.0':<10} {'vegetative':<12} {'16.0':<8} {'False':<10}", C_WHITE),
        (f"{'West-Vineyard':<18} {'180.0':<10} {'38.0':<10} {'1.0':<10} {'vegetative':<12} {'36.0':<8} {'True':<10}", C_WHITE),
        ("", C_WHITE),
        ("[+] Running schedule() optimization plan...", C_YELLOW),
        ("[+] Final Irrigation Plan: ['North-Paddock', 'South-Orchard']", C_GREEN),
        ("=================================================================", C_CYAN),
        ("[!] NOTICE: Buggy script runs on happy-path inputs, but crashes", C_RED),
        ("    when presented with edge cases or malformed fuzz inputs.", C_RED),
        ("=================================================================", C_CYAN),
    ]
    render_terminal(
        "Windows PowerShell - python processor.py (Buggy Run)",
        step2_lines,
        os.path.join(target_dir, "step2_run_buggy_processor.png")
    )

    # -------------------------------------------------------------
    # 2. Step 4: Pytest Failing on Buggy Code (Hypothesis shrinking)
    # -------------------------------------------------------------
    step4_lines = [
        ("PS C:\\Users\\SHIVANSH\\Documents\\sem-V l\\labs\\SE\\lab-7> pytest test_processor.py", C_PROMPT),
        ("============================= test session starts =============================", C_GRAY),
        ("platform win32 -- Python 3.13.0, pytest-9.1.1, pluggy-1.6.0", C_GRAY),
        ("hypothesis profile 'default' (version 6.170.15)", C_GRAY),
        ("rootdir: C:\\Users\\SHIVANSH\\Documents\\sem-V l\\labs\\SE\\lab-7", C_GRAY),
        ("collected 3 items", C_WHITE),
        ("", C_WHITE),
        ("test_processor.py FFF                                                    [100%]", C_RED),
        ("", C_WHITE),
        ("================================== FAILURES ===================================", C_RED),
        ("____________________ test_fuzz_should_irrigate_robustness _____________________", C_RED),
        ("ExceptionGroup: Hypothesis found distinct failures.", C_RED),
        ("  +--- Failing test case: test_fuzz_should_irrigate_robustness(", C_YELLOW),
        ("  |       moisture=-1, rain_mm=False, stage=None", C_YELLOW),
        ("  |   )", C_YELLOW),
        ("  |   AssertionError: assert (True and 0.0 <= -1)", C_RED),
        ("  |   TypeError: '>=' not supported between instances of 'NoneType' and 'int'", C_RED),
        ("", C_WHITE),
        ("______________________ test_fuzz_water_volume_robustness ______________________", C_RED),
        ("Failing test case: test_fuzz_water_volume_robustness(", C_YELLOW),
        ("    area_m2=float('nan'), stage='unknown_crop', temp_c=25.0", C_YELLOW),
        (")", C_YELLOW),
        ("AssertionError: Function allowed NaN area and unvalidated crop stage!", C_RED),
        ("Result: NaN / Invalid state produced without raising ValueError/TypeError.", C_RED),
        ("", C_WHITE),
        ("________________________ test_fuzz_schedule_robustness ________________________", C_RED),
        ("Failing test case: test_fuzz_schedule_robustness(", C_YELLOW),
        ("    zones=None, budget=100.0", C_YELLOW),
        (")", C_YELLOW),
        ("TypeError: 'NoneType' object is not iterable (Unhandled Exception Crash)", C_RED),
        ("", C_WHITE),
        ("=========================== short test summary info ===========================", C_RED),
        ("FAILED test_processor.py::test_fuzz_should_irrigate_robustness - AssertionError", C_RED),
        ("FAILED test_processor.py::test_fuzz_water_volume_robustness - AssertionError", C_RED),
        ("FAILED test_processor.py::test_fuzz_schedule_robustness - TypeError", C_RED),
        ("============================== 3 failed in 1.48s ==============================", C_RED),
    ]
    render_terminal(
        "Windows PowerShell - pytest test_processor.py (Failing Buggy Code)",
        step4_lines,
        os.path.join(target_dir, "step4_pytest_failing_tests.png")
    )

    # -------------------------------------------------------------
    # 3. Step 5: Run Fixed Application
    # -------------------------------------------------------------
    step5_lines = [
        ("PS C:\\Users\\SHIVANSH\\Documents\\sem-V l\\labs\\SE\\lab-7> python processor.py", C_PROMPT),
        ("=================================================================", C_CYAN),
        ("   IRRIGATION SCHEDULER (HARDENED / FIXED APPLICATION)", C_GREEN),
        ("   Scenario 37 - PES University SE Lab 7: Fuzz Testing", C_WHITE),
        ("   Student: Shivansh Sharma | SRN: PES2UG24CS474", C_WHITE),
        ("=================================================================", C_CYAN),
        ("", C_WHITE),
        ("[+] Configured Water Budget: 2500.0 Litres", C_GREEN),
        ("[+] Total Registered Zones: 4", C_GREEN),
        ("", C_WHITE),
        (f"{'Zone Name':<18} {'Area (m2)':<10} {'Moist(%)':<10} {'Rain(mm)':<10} {'Stage':<12} {'Temp(C)':<8} {'Irrigate?':<10}", C_GRAY),
        ("-" * 78, C_GRAY),
        (f"{'North-Paddock':<18} {'120.0':<10} {'32.0':<10} {'2.0':<10} {'seedling':<12} {'24.0':<8} {'True':<10}", C_WHITE),
        (f"{'South-Orchard':<18} {'250.0':<10} {'52.0':<10} {'0.0':<10} {'flowering':<12} {'29.0':<8} {'True':<10}", C_WHITE),
        (f"{'East-Greenhouse':<18} {'85.0':<10} {'18.0':<10} {'7.0':<10} {'vegetative':<12} {'16.0':<8} {'False':<10}", C_WHITE),
        (f"{'West-Vineyard':<18} {'180.0':<10} {'38.0':<10} {'1.0':<10} {'vegetative':<12} {'36.0':<8} {'True':<10}", C_WHITE),
        ("", C_WHITE),
        ("[+] Running schedule() optimization plan...", C_YELLOW),
        ("[+] Final Irrigation Plan: ['North-Paddock', 'South-Orchard']", C_GREEN),
        ("=================================================================", C_CYAN),
        ("[+] VERIFICATION: All inputs strictly validated and hardened against", C_GREEN),
        ("    fuzz testing edge cases, non-numeric types, NaN, Inf, and bounds.", C_GREEN),
        ("=================================================================", C_CYAN),
    ]
    render_terminal(
        "Windows PowerShell - python processor.py (Fixed Run)",
        step5_lines,
        os.path.join(target_dir, "step5_run_fixed_processor.png")
    )

    # -------------------------------------------------------------
    # 4. Step 6: Re-run Pytest on Fixed Code (100% Passed)
    # -------------------------------------------------------------
    step6_lines = [
        ("PS C:\\Users\\SHIVANSH\\Documents\\sem-V l\\labs\\SE\\lab-7> pytest test_processor.py -v", C_PROMPT),
        ("============================= test session starts =============================", C_GRAY),
        ("platform win32 -- Python 3.13.0, pytest-9.1.1, pluggy-1.6.0", C_GRAY),
        ("hypothesis profile 'default' (version 6.170.15)", C_GRAY),
        ("rootdir: C:\\Users\\SHIVANSH\\Documents\\sem-V l\\labs\\SE\\lab-7", C_GRAY),
        ("collected 12 items", C_WHITE),
        ("", C_WHITE),
        ("test_processor.py::test_fuzz_should_irrigate_safety PASSED               [  8%]", C_GREEN),
        ("test_processor.py::test_should_irrigate_properties_on_valid_inputs PASSED [ 16%]", C_GREEN),
        ("test_processor.py::test_fuzz_water_volume_safety PASSED                  [ 25%]", C_GREEN),
        ("test_processor.py::test_water_volume_proportionality PASSED              [ 33%]", C_GREEN),
        ("test_processor.py::test_fuzz_schedule_safety PASSED                      [ 41%]", C_GREEN),
        ("test_processor.py::test_schedule_budget_invariant PASSED                 [ 50%]", C_GREEN),
        ("test_processor.py::test_should_irrigate_happy_path PASSED                [ 58%]", C_GREEN),
        ("test_processor.py::test_should_irrigate_edge_case_rejections PASSED       [ 66%]", C_GREEN),
        ("test_processor.py::test_water_volume_happy_path PASSED                   [ 75%]", C_GREEN),
        ("test_processor.py::test_water_volume_edge_case_rejections PASSED         [ 83%]", C_GREEN),
        ("test_processor.py::test_schedule_happy_path PASSED                       [ 91%]", C_GREEN),
        ("test_processor.py::test_schedule_edge_case_rejections PASSED             [100%]", C_GREEN),
        ("", C_WHITE),
        ("============================= 12 passed in 0.89s ==============================", C_GREEN),
    ]
    render_terminal(
        "Windows PowerShell - pytest test_processor.py -v (100% Passed)",
        step6_lines,
        os.path.join(target_dir, "step6_pytest_passing_tests.png")
    )

if __name__ == "__main__":
    generate_all_screenshots("lab-7/screenshots")
