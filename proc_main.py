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
def adjust_shadows(img: Image.Image, amount: float) -> Image.Image:
    """
    Lifts or darkens the shadow areas (darkest pixels) without affecting 
    the brightest areas significantly. Positive amount lifts shadows.
    """
    if not isinstance(img, Image.Image):
        raise TypeError("Input must be a PIL Image object.")
        
    img = img.convert("RGB")
    
    def shadow_curve(x):
        # Applies a gamma-like curve only to dark pixels (for shadows)
        x_norm = x / 255.0
        # Ensure the amount is clipped to prevent extreme gamma values
        gamma_exponent = max(-2.0, min(2.0, -amount))
        gamma = math.pow(2, gamma_exponent) 
        result_norm = math.pow(x_norm, gamma)
        return int(result_norm * 255)

    lut = [shadow_curve(i) for i in range(256)]
    
    # Apply the custom lookup table to all three RGB channels
    return img.point(lut * 3)


# --- TEMPLATE FUNCTIONS (Library Presets) ---



# --- MANUAL EDIT SEQUENCE (New Library Function) ---

    
# Do not forget to keep the setup.py file in the outer ossimg directory!