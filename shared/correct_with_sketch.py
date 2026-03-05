import os
"""
기존 러너 사진 + 스케치 레이아웃 참고로 제품 위치 보정
Gemini: (runner photo) + (sketch reference) + (product ref) → corrected photo
"""

from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
PICS        = Path("/home/jhkim/00.Projects/00.RunVision/Docs/product pictures")
SKETCH      = Path("/home/jhkim/00.Projects/00.RunVision/Docs/사용자 메뉴얼/모자 착용 이미지.jpg")
PRODUCT_REF = PICS / "05_product_module-on-glasses-side.png"

client = genai.Client(api_key=API_KEY)

def load_part(path: Path) -> types.Part:
    data = path.read_bytes()
    mime = {"jpg":"image/jpeg","jpeg":"image/jpeg",
            "png":"image/png","webp":"image/webp"
            }.get(path.suffix.lower().lstrip("."), "image/jpeg")
    return types.Part.from_bytes(data=data, mime_type=mime)

def correct_photo(runner_path: Path, output_name: str, gender: str):
    if gender == "male":
        person = "Korean male runner, navy athletic shirt, black running cap"
    else:
        person = "Korean female runner, coral pink athletic shirt, white mesh running cap"

    prompt = f"""You have 3 reference images:
- Image 1: A photo of a {person} with an AR device on the cap (current photo to be corrected)
- Image 2: A line sketch showing the EXACT correct position of the AR device on the cap brim
- Image 3: The actual product photo showing what the AR device looks like

TASK: Edit Image 1 to correct the AR device placement and shape.

WHAT TO CHANGE:
1. The AR device position must match the sketch (Image 2) EXACTLY:
   - Device clips from ABOVE the cap brim, bracket folds over the brim
   - Device body is FLUSH against the UNDERSIDE of the cap brim — ZERO gap
   - Positioned on LEFT side of photo (= person's own RIGHT eye)
   - The display module tip hangs down just below the brim edge, pointing toward the right eye

2. The AR device shape must match the product photo (Image 3):
   - White curved elongated body (~8cm)
   - Curved hook/clip that grips the brim from above
   - Angled display tip at the inner end

WHAT TO KEEP UNCHANGED:
- Person's face, expression, skin, hair — keep identical
- Cap style, color, position — keep identical
- Background, lighting — keep identical
- Clothing — keep identical

Only modify the AR device: its shape, position, and attachment to the cap brim."""

    print(f"\n[{gender}] 보정 중...")
    runner_part  = load_part(runner_path)
    sketch_part  = load_part(SKETCH)
    product_part = load_part(PRODUCT_REF)

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[runner_part, sketch_part, product_part, prompt],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.mime_type.startswith("image/"):
            out = PICS / output_name
            out.write_bytes(part.inline_data.data)
            print(f"  ✓ 저장: {out}")
            return
        elif hasattr(part, "text") and part.text:
            print(f"  텍스트: {part.text[:200]}")


# 여성 보정
correct_photo(PICS / "cap_female_gemini.png", "cap_female_corrected.png", "female")

# 남성 보정
correct_photo(PICS / "cap_male_gemini copy.png", "cap_male_corrected.png", "male")

print("\n완료!")
