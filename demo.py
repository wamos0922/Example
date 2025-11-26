# ======================================================================
# File: OSS_AI/demo.py (Sample Usage Repository)
# 
# Demonstrates library usage with templates and manual input, including 
# step-by-step previews.
# ======================================================================

import os
from PIL import Image

# Helper function to safely get a float input from the user.
def get_float_input(prompt: str, default_value: float) -> float:
    """
    사용자에게 float 값을 안전하게 입력받는다.
    - 빈 입력(Enter)이면 default_value 반환
    - 숫자가 아니면 다시 입력 요구
    """
    while True:
        try:
            user_input = input(f"{prompt} (Default: {default_value:.2f}): ").strip()
            if not user_input:
                return default_value
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")

def create_dummy_image(filename: str = "sample_input.png") -> None:
    """Creates a basic image if no input file exists for testing."""
    if not os.path.exists(filename):
        print(f"--- Creating a dummy image: {filename} ---")
        img = Image.new("RGB", (300, 200), color="#6A5ACD")
        img.save(filename)

# --- Library Imports ---
try:
    from ossimg.proc import (
        load_image,
        adjust_brightness,
        adjust_saturation,
        adjust_sharpness,
        adjust_shadows,
        apply_golden_hour,
        apply_gritty_contrast,
        apply_pastel_matte,
        # New manual edit sequence function (generator)
        process_manual_edits,
    )
except ImportError:
    print(
        "FATAL ERROR: Library 'ossimg' not found. "
        "Please run 'pip3 install -e .' in the ossimg folder."
    )
    raise SystemExit(1)

# --- MANUAL EDIT LOGIC (Collects Input, Runs Process, Saves Previews) ---

def run_manual_edit(img: Image.Image) -> Image.Image:
    print("\n--- Starting Manual Edit Mode (Enter values for 4 edits) ---")

    # 1. COLLECT ALL INPUTS FIRST
    print("\n[1/4] ADJUST SATURATION: (1.0 = original, 0.0 = B&W, > 1.0 = vibrant)")
    saturation_factor = get_float_input("Enter Saturation Factor", 1.0)

    print("\n[2/4] ADJUST SHADOWS: (0.0 = neutral, + to lift shadows, - to crush shadows)")
    shadows_amount = get_float_input("Enter Shadows Amount", 0.0)

    print("\n[3/4] ADJUST BRIGHTNESS: (1.0 = original, > 1.0 = brighter)")
    brightness_factor = get_float_input("Enter Brightness Factor", 1.0)

    print("\n[4/4] ADJUST SHARPNESS: (1.0 = original, > 1.0 = sharper)")
    sharpness_factor = get_float_input("Enter Sharpness Factor", 1.0)

    # 2. RUN THE EDITS AND HANDLE PREVIEWS

    print("\n--- Applying Edits Step-by-Step and Saving Previews ---")

    # process_manual_edits 는 제너레이터를 반환한다고 가정
    edit_sequence = process_manual_edits(
        img,
        saturation_factor,
        shadows_amount,
        brightness_factor,
        sharpness_factor,
    )

    final_img = None
    step_count = 1
    for feature_name, current_img in edit_sequence:
        preview_name = f"preview_{step_count:02d}_{feature_name}.png"
        current_img.save(preview_name)
        print(
            f"📸 Step {step_count}: {feature_name.upper()} applied. "
            f"Preview saved: {preview_name}"
        )
        final_img = current_img  # 마지막 결과 보존
        step_count += 1

    # 3. FINAL OUTPUT
    if final_img is not None:
        final_img_name = "output_FINAL_MANUAL_EDIT.png"
        final_img.save(final_img_name)
        print(f"\n🎉 Final combined edit saved as: {final_img_name}")
        return final_img

    # 방어적 코드: 이론상 여기까지 오면 안 됨
    return img

# --- MAIN ENTRY POINT ---

def main() -> None:
    INPUT_FILE = "sample_input.png"
    create_dummy_image(INPUT_FILE)

    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file '{INPUT_FILE}' is missing.")
        return

    try:
        original_img = load_image(INPUT_FILE)

        print("\n=======================================================")
        print("    Welcome to the Image Editor Demo")
        print("=======================================================")
        print("Choose an option:")
        print(" 1: Apply 'Golden Hour Warmth' Template (Warm, Soft)")
        print(" 2: Apply 'Urban Gritty Contrast' Template (High Detail, Deep Blacks)")
        print(" 3: Apply 'Soft Pastel Matte' Template (Faded, Bright)")
        print(" 4: Manually Edit All 4 Features (Your custom look)")
        print("=======================================================")

        choice = input("Enter your choice (1, 2, 3, or 4): ").strip()

        final_img = None
        output_suffix: str | None = None

        if choice == "1":
            print("--- Applying Template: Golden Hour Warmth ---")
            final_img = apply_golden_hour(original_img)
            output_suffix = "GOLDEN_HOUR"

        elif choice == "2":
            print("--- Applying Template: Urban Gritty Contrast ---")
            final_img = apply_gritty_contrast(original_img)
            output_suffix = "GRITTY_CONTRAST"

        elif choice == "3":
            print("--- Applying Template: Soft Pastel Matte ---")
            final_img = apply_pastel_matte(original_img)
            output_suffix = "PASTEL_MATTE"

        elif choice == "4":
            final_img = run_manual_edit(original_img)
            output_suffix = "MANUAL_EDIT"
            # run_manual_edit 안에서 이미 최종 출력 저장하므로,
            # 아래 공통 저장 블록은 건너뛴다.

        else:
            print("\n⚠️ Invalid choice. Exiting demo.")
            return

        if final_img is not None and output_suffix is not None and choice != "4":
            final_output_name = f"output_FINAL_{output_suffix}.png"
            final_img.save(final_output_name)
            print(f"\n✅ Processing complete. Image saved as: {final_output_name}")

    except Exception as e:
        print(f"\nAn error occurred during image processing: {e}")

if __name__ == "__main__":
    main()
