import os
"""
여성 한강 사진에 모자챙 마운팅 브래킷 합성
- 타겟: glasses_lifestyle_female.png (5번 섹션 여성 사진)
- 참조: 모자 착용 사진.jpg (12번 - 남성, 모자챙 클립 브래킷 보임)
- 추가할 것: 갈색/다크 색상의 모자챙 클립 브래킷만
"""

from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
PICS    = Path("/home/jhkim/00.Projects/00.RunVision/Docs/product pictures")
MANUAL  = Path("/home/jhkim/00.Projects/00.RunVision/Docs/사용자 메뉴얼")

TARGET = PICS   / "glasses_lifestyle_female.png"
REF    = MANUAL / "모자 착용 사진.jpg"

client = genai.Client(api_key=API_KEY)

def load_part(path: Path) -> types.Part:
    data = path.read_bytes()
    mime = {"jpg":"image/jpeg","jpeg":"image/jpeg",
            "png":"image/png","webp":"image/webp"
            }.get(path.suffix.lower().lstrip("."), "image/jpeg")
    return types.Part.from_bytes(data=data, mime_type=mime)

prompt = """I have two images:
- IMAGE 1 (target): A Korean female runner jogging at Han River, wearing a dark Adidas cap and round glasses. There is a small white AR lens device visible on her glasses.
- IMAGE 2 (reference): A man wearing a black Adidas cap and glasses. The reference shows a dark brown/black mounting BRACKET — a clip-arm assembly that hooks OVER the cap brim from above, with an arm extending down to connect to the glasses frame.

YOUR TASK — Make ONE small addition to IMAGE 1 (the female runner):

ADD ONLY: The dark brown mounting bracket/clip assembly from the reference photo.
- The bracket clips OVER the top of the cap brim (the clip part is visible on the top surface of the brim)
- A thin dark arm extends downward from the clip to the glasses frame
- It connects to the white AR device already on her glasses
- Position: LEFT SIDE of the photo (her right eye side), where the white AR device already is
- Color: dark brown / matte black — same as reference
- The bracket should look naturally integrated, as if it was always there

KEEP EVERYTHING ELSE COMPLETELY IDENTICAL:
- The female runner's face, expression, skin, hair — unchanged
- The background (Han River, trees, Seoul skyline) — unchanged
- The dark cap shape and Adidas logo — unchanged
- Her glasses and the white AR lens device — unchanged
- Her clothing and running pose — unchanged
- The lighting and photo style — unchanged

IMPORTANT: Only the mounting bracket/clip is added. Nothing else changes."""

print("모자챙 브래킷 합성 중...")
target_part = load_part(TARGET)
ref_part    = load_part(REF)

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[target_part, ref_part, prompt],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
    ),
)

saved = False
for part in response.candidates[0].content.parts:
    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
        out = PICS / "glasses_lifestyle_with_bracket.png"
        out.write_bytes(part.inline_data.data)
        print(f"✓ 저장: {out}")
        saved = True
    elif hasattr(part, "text") and part.text:
        print(f"  텍스트: {part.text[:200]}")

if not saved:
    print("이미지 생성 실패")
