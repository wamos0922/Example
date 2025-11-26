# ======================================================================
# File: mycats/demo.py (Sample Usage Repository)
# 
# Demonstrates library usage with templates and manual input, including 
# step-by-step previews.
# ======================================================================
import os 
from PIL import Image


# Helper function to safely get a float input from the user.


# Create Dummy Image




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
    
    # Call the library function, which is now a generator
    edit_sequence = process_manual_edits(
        img, 
        saturation_factor, 
        shadows_amount, 
        brightness_factor, 
        sharpness_factor
    )
    
    final_img = None
    step_count = 1
    for feature_name, current_img in edit_sequence:
        preview_name = f"preview_{step_count:02d}_{feature_name}.png"
        current_img.save(preview_name)
        print(f"📸 Step {step_count}: {feature_name.upper()} applied. Preview saved: {preview_name}")
        final_img = current_img # Keep the latest image reference
        step_count += 1

    # 3. FINAL OUTPUT
    if final_img:
        final_img_name = "output_FINAL_MANUAL_EDIT.png"
        final_img.save(final_img_name)
        print(f"\n🎉 Final combined edit saved as: {final_img_name}")
        return final_img
    
    # Should not happen, but for safety
    return img 




# --- MAIN ENTRY POINT ---
def main():
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
        
        choice = input("Enter your choice (1, 2, 3, or 4): ")

        final_img = None
        output_suffix = None
        
        if choice == '1':
            print("--- Applying Template: Golden Hour Warmth ---")
            final_img = apply_golden_hour(original_img)
            output_suffix = "GOLDEN_HOUR"
        
        elif choice == '2':
            print("--- Applying Template: Urban Gritty Contrast ---")
            final_img = apply_gritty_contrast(original_img)
            output_suffix = "GRITTY_CONTRAST"
            
        elif choice == '3':
            print("--- Applying Template: Soft Pastel Matte ---")
            final_img = apply_pastel_matte(original_img)
            output_suffix = "PASTEL_MATTE"
            
        elif choice == '4':
            final_img = run_manual_edit(original_img)
            output_suffix = "MANUAL_EDIT"
            # Note: run_manual_edit already saves the final image, 
            # so we skip the final save block below for this case.
            
        else:
            print("\n⚠️ Invalid choice. Exiting demo.")
            return

        if final_img and output_suffix and choice != '4':
            FINAL_OUTPUT_NAME = f"output_FINAL_{output_suffix}.png"
            final_img.save(FINAL_OUTPUT_NAME)
            print(f"\n✅ Processing complete. Image saved as: {FINAL_OUTPUT_NAME}")

    except Exception as e:
        print(f"\nAn error occurred during image processing: {e}")

if __name__ == "__main__":
    main()

