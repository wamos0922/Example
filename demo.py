# ======================================================================
# File: OSS_AI/demo.py (Sample Usage Repository)
#
# Demonstrates library usage with templates and manual input, including
# step-by-step previews.
#
# - 기본 동작:
#   * 입력 이미지가 있으면 그걸 사용
#   * 인자를 안 주면 더미(gradient) 이미지를 생성해서 사용
#   * 사용자에게 Brightness, Gamma 값을 입력받아서
#     단계별(preview) 결과 이미지를 저장
#
# - 사용 예시:
#   python demo.py                # 더미 이미지로 실행
#   python demo.py sample.png     # sample.png로 실행
# ======================================================================

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

# 여기 import 부분만 실제 라이브러리 이름에 맞춰 바꾸면 된다.
# D:\OSS_AI 기준으로는 from ossimg import ... 으로 사용 중.
from ossimg import (
    load_image,
    save_image,
    adjust_brightness,
    adjust_gamma,
    # 필요하면 아래 것들도 나중에 확장 가능
    # adjust_saturation,
    # adjust_sharpness,
    # adjust_shadows,
)


# Helper function to safely get a float input from the user.
def _ask_float(
    prompt: str,
    default: Optional[float] = None,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
) -> float:
    """
    사용자에게 float 값을 안전하게 입력받는다.
    엔터만 치면 default를 사용하고, 범위를 벗어나면 다시 입력받는다.
    """
    while True:
        raw = input(prompt).strip()

        # 빈 입력 → 기본값 사용
        if raw == "":
            if default is not None:
                return default
            print("값을 입력하거나 기본값을 설정하세요.")
            continue

        try:
            val = float(raw)
        except ValueError:
            print("숫자를 입력해야 합니다. 다시 시도하세요.")
            continue

        if min_val is not None and val < min_val:
            print(f"값은 최소 {min_val} 이상이어야 합니다.")
            continue
        if max_val is not None and val > max_val:
            print(f"값은 최대 {max_val} 이하여야 합니다.")
            continue

        return val


# Create Dummy Image
def create_dummy_image(width: int = 512, height: int = 320) -> "Image.Image":
    """
    입력 파일이 없을 때 사용할 더미 이미지를 생성한다.
    좌우로 밝기가 변하는 그라디언트 + 상단에 컬러 블록을 넣어서
    Brightness / Gamma 변화가 잘 보이도록 했다.
    """
    from PIL import Image, ImageDraw  # 로컬 import (의존성 최소화)

    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 수평 그라디언트 (왼쪽 어둡고 → 오른쪽 밝게)
    for x in range(width):
        v = int(255 * x / (width - 1))
        for y in range(height // 2, height):
            draw.point((x, y), fill=(v, v, v))

    # 상단에 컬러 블록 3개 (Red, Green, Blue)
    block_w = width // 3
    draw.rectangle([0, 0, block_w - 1, height // 2 - 1], fill=(220, 30, 30))
    draw.rectangle(
        [block_w, 0, 2 * block_w - 1, height // 2 - 1], fill=(40, 200, 60)
    )
    draw.rectangle(
        [2 * block_w, 0, width - 1, height // 2 - 1], fill=(30, 80, 220)
    )

    return img


# --- MANUAL EDIT LOGIC (Collects Input, Runs Process, Saves Previews) ---
def run_manual_edit(
    input_path: Optional[str] = None,
    output_dir: str = "outputs_manual",
) -> None:
    """
    - 입력 이미지 또는 더미 이미지에서 시작해서
    - Brightness / Gamma 값을 사용자에게 입력받고
    - 단계별(preview) 결과를 파일로 저장한다.
    """
    os.makedirs(output_dir, exist_ok=True)

    if input_path is None:
        print("[demo] 입력 이미지 없음 → 더미 이미지 생성")
        img = create_dummy_image()
        base_name = "dummy"
    else:
        print(f"[demo] 입력 이미지 사용: {input_path}")
        img = load_image(input_path)
        base_name = Path(input_path).stem

    # Step 0: 원본 저장
    step0_path = os.path.join(output_dir, f"{base_name}_step0_original.png")
    save_image(img, step0_path)
    print(f"  [step0] 원본 저장 -> {step0_path}")

    print("\n=== 수동 편집 입력 ===")
    print("Enter를 누르면 대괄호 안의 기본값이 사용됩니다.\n")

    # Brightness: 0.0 ~ 3.0, 기본 1.0
    brightness = _ask_float(
        "밝기 (Brightness) factor [기본 1.0, 권장 0.0~3.0]: ",
        default=1.0,
        min_val=0.0,
        max_val=3.0,
    )

    # Gamma: 0.1 ~ 5.0, 기본 1.0
    gamma = _ask_float(
        "감마 (Gamma) 값 [기본 1.0, 권장 0.1~5.0, 값이 클수록 더 밝게]: ",
        default=1.0,
        min_val=0.1,
        max_val=5.0,
    )

    print("\n=== 필터 적용 순서 ===")
    print("1) Brightness → 2) Gamma 순서로 적용하여 preview를 생성합니다.\n")

    # Step 1: Brightness 적용
    img_step1 = adjust_brightness(img, brightness)
    step1_path = os.path.join(
        output_dir, f"{base_name}_step1_brightness_{brightness:.2f}.png"
    )
    save_image(img_step1, step1_path)
    print(f"  [step1] Brightness={brightness:.2f} 적용 -> {step1_path}")

    # Step 2: Gamma 적용
    img_step2 = adjust_gamma(img_step1, gamma)
    step2_path = os.path.join(
        output_dir, f"{base_name}_step2_gamma_{gamma:.2f}.png"
    )
    save_image(img_step2, step2_path)
    print(f"  [step2] Gamma={gamma:.2f} 적용 -> {step2_path}")

    print("\n=== 요약 ===")
    print(f"  입력 이미지     : {input_path if input_path else '(dummy image)'}")
    print(f"  출력 디렉터리   : {Path(output_dir).resolve()}")
    print(f"  적용 Brightness : {brightness:.2f}")
    print(f"  적용 Gamma      : {gamma:.2f}")
    print("  step0 / step1 / step2 이미지를 비교해서 보고서/PPT에 사용하면 된다.")


# --- MAIN ENTRY POINT ---
if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2:
        in_path = sys.argv[1]
    else:
        in_path = None  # None이면 dummy 이미지 사용

    run_manual_edit(in_path)
