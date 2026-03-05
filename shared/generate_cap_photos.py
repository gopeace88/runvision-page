"""
RunVision 모자 착용 실사 사진 생성
Gemini Imagen API + 제품 참고 이미지 사용
"""

import os
import base64
import json
from pathlib import Path
from google import genai
from google.genai import types

# ── 경로 설정 ──────────────────────────────────────────────
PICS_DIR   = Path("/home/jhkim/00.Projects/00.RunVision/Docs/product pictures")
OUTPUT_DIR = Path("/home/jhkim/00.Projects/00.RunVision/Docs/product pictures")
API_KEY = os.environ.get("GEMINI_API_KEY", "")

# 제품 참고 이미지 (실제 제품 side view)
PRODUCT_REF = PICS_DIR / "05_product_module-on-glasses-side.png"

# ── Gemini 클라이언트 ────────────────────────────────────────
client = genai.Client(api_key=API_KEY)

def load_image_part(path: Path) -> types.Part:
    """이미지 파일을 Gemini Part로 변환"""
    data = path.read_bytes()
    ext  = path.suffix.lower().lstrip(".")
    mime = {"png": "image/png", "jpg": "image/jpeg",
            "jpeg": "image/jpeg", "webp": "image/webp"}.get(ext, "image/png")
    return types.Part.from_bytes(data=data, mime_type=mime)

def generate_runner_photo(subject: str, output_filename: str):
    """
    subject: 'male' or 'female'
    """
    if subject == "male":
        person_desc = "Korean male runner in his early 30s, wearing a black running cap, navy athletic shirt, sweating face, determined intense expression"
        bg_desc     = "Han river park Seoul background, golden hour sunlight"
    else:
        person_desc = "Korean female runner in her late 20s, wearing a white mesh running cap, coral pink athletic shirt, focused expression"
        bg_desc     = "Seoul park with trees background, natural daylight"

    prompt = f"""Using the product reference image provided, generate a photorealistic DSLR sports photography portrait.

SUBJECT: {person_desc}

PRODUCT PLACEMENT (CRITICAL — extremely precise):
- The white AR module is attached FLUSH to the UNDERSIDE of the cap brim/visor — ZERO GAP between device and brim
- The device is touching the brim directly, like it is glued to the bottom surface of the visor
- Position: LEFT SIDE of the photo (= person's own RIGHT eye side)
- Because the device is flush under the brim with no gap, it appears as part of the brim itself — the device bottom edge is at the same line as the brim bottom edge
- The person's eye is BELOW the brim, so the device is ABOVE the eye level — the person would tilt their gaze slightly upward to see the display
- The device is NOT floating below the brim — it is ATTACHED TO THE BRIM with no space between them
- NO device on the right side of the photo, only left side

PRODUCT SHAPE (match reference image exactly):
- White curved elongated slim body, approximately 8-10cm
- Mounted flat against the underside surface of the cap visor
- Angled display module at the inner tip pointing downward toward the right eye
- Sleek white plastic, slim and minimal — looks like part of the cap brim

PHOTO STYLE:
- {bg_desc}
- Close-up portrait, 3/4 angle facing slightly right
- Sharp focus on face and the device
- Soft bokeh background
- Photorealistic, professional sports photography
- No illustration, no cartoon"""

    print(f"\n[{subject}] 생성 중...")

    ref_image = load_image_part(PRODUCT_REF)

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[ref_image, prompt],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    # 결과 저장
    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.mime_type.startswith("image/"):
            out_path = OUTPUT_DIR / output_filename
            out_path.write_bytes(part.inline_data.data)
            print(f"  ✓ 저장: {out_path}")
            return str(out_path)
        elif hasattr(part, "text") and part.text:
            print(f"  텍스트 응답: {part.text[:200]}")

    print("  ⚠ 이미지 없음")
    return None


if __name__ == "__main__":
    print("RunVision 모자 착용 사진 생성 (Gemini Imagen)")
    print(f"제품 참고 이미지: {PRODUCT_REF.name}")

    generate_runner_photo("male",   "cap_male_gemini.png")
    generate_runner_photo("female", "cap_female_gemini.png")

    print("\n완료!")
