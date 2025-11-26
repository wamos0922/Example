from PIL import Image, ImageEnhance
import math
from typing import Generator, Tuple, Union


# --- General Utility ---
def load_image(path: str) -> Image.Image:
    """Loads an image from a file path."""
    return Image.open(path)


# --- Feature Implementations ---

# 1. BRIGHTNESS (General Luminance Control)
def adjust_brightness(img: Image.Image, factor: float) -> Image.Image:
    """
    Adjusts the overall brightness of the image.
    Factor 1.0 = original, > 1.0 = brighter, < 1.0 = darker.
    """
    if not isinstance(img, Image.Image):
        raise TypeError("Input must be a PIL Image object.")
    
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)



# 2. SATURATION (Color Intensity Control)
def adjust_saturation(img: Image.Image, factor: float) -> Image.Image:
    """
    Adjusts the intensity of colors (saturation).
    
    Factor 1.0 = original, 0.0 = grayscale, > 1.0 = more vibrant colors.
    """
    if not isinstance(img, Image.Image):
        raise TypeError("Input must be a PIL Image object.")
        
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(factor)






# 3. SHARPNESS (Detail/Edge Control)
def adjust_sharpness(img: Image.Image, factor: float) -> Image.Image:
    """
    Adjusts the image sharpness.
    
    Factor 1.0 = original, > 1.0 = sharper, < 1.0 = blurrier.
    """
    if not isinstance(img, Image.Image):
        raise TypeError("Input must be a PIL Image object.")
        
    enhancer = ImageEnhance.Sharpness(img)
    return enhancer.enhance(factor)



# 4. SHADOWS (Tonal Control - Advanced Custom Curve)




# --- TEMPLATE FUNCTIONS (Library Presets) ---

#goldenhourtemplate
def apply_golden_hour(img: Image.Image) -> Image.Image:
    """
    Applies a warm, soft 'Golden Hour' look.
    Uses Saturation to boost warm colors, Brightness for overall glow.
    """
    img = adjust_saturation(img, 1.30) 
    img = adjust_shadows(img, 0.30)
    img = adjust_brightness(img, 1.15)
    img = adjust_sharpness(img, 0.80)
    return img

def apply_gritty_contrast(img: Image.Image) -> Image.Image:
    """
    Applies an 'Urban Gritty Contrast' look.
    Low saturation and crushed shadows for high contrast.
    """
    img = adjust_sharpness(img, 2.50)
    img = adjust_brightness(img, 0.90)
    img = adjust_shadows(img, -0.20)
    img = adjust_saturation(img, 0.80) 
    return img

#grittytemplate

#pastelTemplate





# --- MANUAL EDIT SEQUENCE (New Library Function) ---


    
# Do not forget to keep the setup.py file in the outer ossimg directory!