import os
"""
안경 마운트 라이프스타일 사진 생성
- 원본: 남성, 실내, 안경+AR디바이스 착용 사진 (참고용)
- 목표: 여성 한국 러너, 한강 조깅, 동일 제품 착용
"""

from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
PICS     = Path("/home/jhkim/00.Projects/00.RunVision/Docs/product pictures")
MANUAL   = Path("/home/jhkim/00.Projects/00.RunVision/Docs/사용자 메뉴얼")
INPUT    = MANUAL / "모자 착용 사진.jpg"

client = genai.Client(api_key=API_KEY)

def load_part(path: Path) -> types.Part:
    data = path.read_bytes()
    mime = {"jpg":"image/jpeg","jpeg":"image/jpeg",
            "png":"image/png","webp":"image/webp"
            }.get(path.suffix.lower().lstrip("."), "image/jpeg")
    return types.Part.from_bytes(data=data, mime_type=mime)

prompt = """Create a photorealistic lifestyle photo of a Korean female runner jogging along the Han River in Seoul.

REFERENCE: The attached photo shows a man wearing a black Adidas cap and round glasses with a white AR display device clipped onto the glasses frame. Use this as the PRODUCT REFERENCE ONLY.

SCENE:
- Location: Han River (한강) riverside running path in Seoul, South Korea
- Time: Morning golden hour, bright sunshine, beautiful sky
- Action: Korean female runner jogging energetically and happily — dynamic running pose, slight motion blur on legs
- Background: Han River visible behind her, Seoul city skyline and bridge faintly visible, lush green trees along the path

PERSON:
- Korean female runner, approximately 28-32 years old
- Athletic build, sporty and energetic look
- Wearing: dark navy or black running cap (similar brim style to reference)
- Wearing: thin round-frame sports glasses (similar to reference photo)
- Wearing: bright athletic outfit — colorful running shirt and shorts
- Hair: ponytail

PRODUCT (critical — must be visible):
- The SAME white AR display device from the reference photo is clipped onto her glasses frame
- The white device is on her RIGHT eye side (LEFT side of photo)
- The device is a small white teardrop/oval shape with a thin arm bracket
- It is attached to the GLASSES NOSE BRIDGE AREA / inner frame side
- The device should be clearly visible but not obtrusive
- BOTH eyes must be visible and unobstructed by the device

PHOTO STYLE:
- Professional sports photography, wide-angle shot
- Bright and energetic mood
- Shallow depth of field — runner in sharp focus, Han River background slightly blurred
- Horizontal landscape orientation (16:9)
- High resolution, magazine quality"""

print("한강 여성 러너 생성 중...")
ref_part = load_part(INPUT)

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[ref_part, prompt],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
    ),
)

saved = False
for part in response.candidates[0].content.parts:
    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
        out = PICS / "glasses_lifestyle_female.png"
        out.write_bytes(part.inline_data.data)
        print(f"✓ 저장: {out}")
        saved = True
    elif hasattr(part, "text") and part.text:
        print(f"  텍스트: {part.text[:200]}")

if not saved:
    print("이미지 생성 실패")
