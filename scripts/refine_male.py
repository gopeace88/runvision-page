import os
"""
남성 이미지 세부 보정:
1. 제품을 모자 챙에 더 밀착 (위로 이동)
2. 클립/스트랩 색상을 어두운 색으로
"""

from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
PICS        = Path("/home/jhkim/00.Projects/00.RunVision/Docs/product pictures")
PRODUCT_REF = PICS / "05_product_module-on-glasses-side.png"

client = genai.Client(api_key=API_KEY)

def load_part(path: Path) -> types.Part:
    data = path.read_bytes()
    mime = {"jpg":"image/jpeg","jpeg":"image/jpeg",
            "png":"image/png","webp":"image/webp"
            }.get(path.suffix.lower().lstrip("."), "image/jpeg")
    return types.Part.from_bytes(data=data, mime_type=mime)

prompt = """Edit the runner photo with these TWO specific changes only:

CHANGE 1 — Device position (move UP):
- The white AR device on the cap brim needs to move UP so it is completely flush against the UNDERSIDE of the cap brim
- Currently there is still a small gap between the device and the brim — eliminate this gap entirely
- The top edge of the device must be touching/pressed against the bottom surface of the cap visor
- No gap, no space — the device appears as if it is attached directly to the brim underside

CHANGE 2 — Strap/clip color (make DARK):
- The mounting clip/strap/bracket that connects the device to the cap brim should be DARK colored (dark gray or black)
- This dark strap wraps over the top of the cap brim to secure the device
- The main white body of the device stays white
- Only the mounting clip/strap part changes to dark gray/black color

KEEP EVERYTHING ELSE IDENTICAL:
- Person's face, expression, skin, hair — unchanged
- Cap color, shape — unchanged
- Background, lighting — unchanged
- Clothing — unchanged
- Device shape and size — unchanged, only position and strap color change"""

print("남성 이미지 보정 중...")
runner_part  = load_part(PICS / "cap_male_corrected.png")
product_part = load_part(PRODUCT_REF)

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[runner_part, product_part, prompt],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
    ),
)

for part in response.candidates[0].content.parts:
    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
        out = PICS / "cap_male_refined.png"
        out.write_bytes(part.inline_data.data)
        print(f"  ✓ 저장: {out}")
    elif hasattr(part, "text") and part.text:
        print(f"  텍스트: {part.text[:200]}")
