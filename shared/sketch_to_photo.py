import os
"""
스케치 → 실사 변환
Gemini가 모자 착용 스케치를 실제 사진처럼 변환
"""

from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
SKETCH     = Path("/home/jhkim/00.Projects/00.RunVision/Docs/사용자 메뉴얼/모자 착용 이미지.jpg")
PRODUCT_REF = Path("/home/jhkim/00.Projects/00.RunVision/Docs/product pictures/05_product_module-on-glasses-side.png")
OUTPUT_DIR = Path("/home/jhkim/00.Projects/00.RunVision/Docs/product pictures")

client = genai.Client(api_key=API_KEY)

def load_part(path: Path) -> types.Part:
    data = path.read_bytes()
    ext  = path.suffix.lower().lstrip(".")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png", "webp": "image/webp"}.get(ext, "image/jpeg")
    return types.Part.from_bytes(data=data, mime_type=mime)

prompt = """I am providing two images:
1. A line sketch showing a person wearing a running cap with an AR display device mounted on the cap brim
2. A product reference photo of the actual white AR display device (RunVision)

TASK: Convert the sketch (image 1) into a PHOTOREALISTIC sports photograph.

CRITICAL — preserve the exact layout of the sketch:
- Same head/cap angle and perspective
- The white AR device is mounted FLUSH on the UNDERSIDE of the cap brim, LEFT side of photo (person's own right eye)
- ZERO gap between the device and the brim — device touches the brim directly
- Device shape must match the product reference photo (image 2): white curved elongated body with angled display tip
- The glasses (round frames) stay as shown in the sketch
- The Adidas cap stays as shown

PERSON: Korean male runner, mid-30s, athletic build, slight beard/stubble, weathered athletic look
OUTFIT: Running athletic shirt
BACKGROUND: Outdoor running environment — Han river park Seoul, golden hour warm light, soft bokeh
STYLE: Professional DSLR sports photography, sharp focus on face and device, photorealistic, cinematic quality

Make it look like an actual photo shoot, not AI-generated. High detail, natural skin texture, realistic lighting."""

print("스케치 → 실사 변환 중...")
sketch_part  = load_part(SKETCH)
product_part = load_part(PRODUCT_REF)

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[sketch_part, product_part, prompt],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
    ),
)

for part in response.candidates[0].content.parts:
    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
        out = OUTPUT_DIR / "cap_male_sketch2photo.png"
        out.write_bytes(part.inline_data.data)
        print(f"✓ 저장: {out}")
    elif hasattr(part, "text") and part.text:
        print(f"텍스트: {part.text[:300]}")
