import os
"""
디바이스 없는 깨끗한 베이스 러너 이미지 생성
"""
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
OUT = Path("/home/jhkim/00.Projects/00.RunVision/Docs/product pictures/cap_male_base.png")

client = genai.Client(api_key=API_KEY)

prompt = """Photorealistic DSLR sports photography portrait.

SUBJECT: Korean male runner, early 30s, athletic build, slight stubble/beard
OUTFIT: Navy blue athletic running shirt
CAP: Black running cap, slightly tilted, cap brim casting shadow over forehead
POSE: 3/4 angle facing right, looking forward into the distance
NO DEVICE: There is absolutely NO device, gadget, clip, or attachment on the cap or face — clean cap only
EXPRESSION: Focused, intense, slightly open mouth breathing after run
BACKGROUND: Han river park Seoul, golden hour warm sunset light from right side, blurred bokeh
STYLE: Sharp focus on face, shallow depth of field, professional sports photography, cinematic quality, photorealistic

Image should be portrait orientation (2:3 ratio). Close-up head and shoulders shot."""

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt],
    config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
)

for part in response.candidates[0].content.parts:
    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
        OUT.write_bytes(part.inline_data.data)
        print(f"✓ 저장: {OUT}")
    elif hasattr(part, "text") and part.text:
        print(f"텍스트: {part.text[:100]}")
