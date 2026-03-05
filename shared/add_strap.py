import os
"""
여성 사진에 모자챙 클립 스트랩만 추가
- 사진의 나머지 요소는 완전히 동일하게 유지
- 옅은 색 (연회색/흰색) 얇은 마운팅 스트랩만 추가
"""

from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
PICS    = Path("/home/jhkim/00.Projects/00.RunVision/Docs/product pictures")
INPUT   = PICS / "cap_female_corrected copy.png"

client = genai.Client(api_key=API_KEY)

def load_part(path: Path) -> types.Part:
    data = path.read_bytes()
    mime = {"jpg":"image/jpeg","jpeg":"image/jpeg",
            "png":"image/png","webp":"image/webp"
            }.get(path.suffix.lower().lstrip("."), "image/jpeg")
    return types.Part.from_bytes(data=data, mime_type=mime)

prompt = """Make ONE very small change to this photo:

ADD ONLY: A small, thin mounting strap/bracket on the white AR device that is clipped to the cap brim.
- The strap should wrap OVER THE TOP of the cap brim (visible on the upper surface of the brim)
- The strap is LIGHT GRAY or WHITE colored — subtle, not dark
- It is thin (about 4-6mm wide) and short — just enough to show the device is clipped to the brim
- It appears on the LEFT SIDE of the photo where the white AR device is already attached

KEEP EVERYTHING ELSE COMPLETELY IDENTICAL:
- The woman's face, skin, hair, expression — unchanged
- The white cap shape, color, mesh texture — unchanged
- The white AR device body position and shape — unchanged
- The background (trees, park) — unchanged
- The coral pink shirt — unchanged
- The lighting — unchanged

Only the small light-colored mounting strap/clip on top of the brim is added. Nothing else changes."""

print("스트랩 추가 편집 중...")
img_part = load_part(INPUT)

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[img_part, prompt],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
    ),
)

for part in response.candidates[0].content.parts:
    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
        out = PICS / "cap_female_strap.png"
        out.write_bytes(part.inline_data.data)
        print(f"✓ 저장: {out}")
    elif hasattr(part, "text") and part.text:
        print(f"텍스트: {part.text[:200]}")
