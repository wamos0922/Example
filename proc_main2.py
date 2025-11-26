# ======================================================================
# File: ossimg/proc.py (Library Repository)
# 
# Contains 4 core editing features: Brightness, Saturation, Sharpness, and Shadows
# Also contains preset templates and the Manual Edit sequence function.
# ======================================================================

# --- General Utility ---

# --- Feature Implementations ---

# 1. BRIGHTNESS (General Luminance Control)

# 2. SATURATION (Color Intensity Control)

# 3. SHARPNESS (Detail/Edge Control)

# 4. SHADOWS (Tonal Control - Advanced Custom Curve)

# --- TEMPLATE FUNCTIONS (Library Presets) ---

def apply_pastel_matte(img: Image.Image) -> Image.Image:
    """
    Applies a 'Soft Pastel Matte' look.
    Over-brightness and aggressive shadow lift for the matte look.
    """
    img = adjust_saturation(img, 1.10)
    img = adjust_shadows(img, 0.70)
    img = adjust_brightness(img, 1.20)
    img = adjust_sharpness(img, 0.90)
    return img


# --- MANUAL EDIT SEQUENCE (New Library Function) ---
    
# Do not forget to keep the setup.py file in the outer ossimg directory!