"""
PIL로 여성 사진 모자챙 위에 얇은 마운팅 스트랩 추가
- 챙 상단면에 연회색 스트랩 그리기
- 사다리꼴 형태로 챙 각도 반영
- 반투명으로 자연스럽게 블렌딩
"""

from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

PICS  = Path("/home/jhkim/00.Projects/00.RunVision/Docs/product pictures")
INPUT = PICS / "cap_female_corrected copy.png"
OUT   = PICS / "cap_female_with_strap.png"

base = Image.open(INPUT).convert("RGBA")
W, H = base.size
print(f"Image size: {W}x{H}")

# ── 스트랩 레이어 (투명 배경) ──────────────────────────
strap_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(strap_layer)

# 챙 상단면 좌표 (디버그에서 확인)
# 챙이 약간 왼쪽 위→오른쪽 아래 방향으로 기울어짐
# 스트랩: 모자챙 클립이 올라가는 부분 (x: 574~648, y: 108~132)
# 챙 각도 반영: 왼쪽이 약간 더 높음

sx1, sx2 = 574, 650   # x 범위 (디바이스 폭과 맞춤)
# 사다리꼴: 챙 각도 반영 (왼쪽 2px 높음)
top_y_left  = 106
top_y_right = 109
bot_y_left  = 126
bot_y_right = 128

# ── 메인 스트랩 (연회색, 반투명) ──────────────────────
strap_color = (180, 180, 182, 210)  # 연회색, 약간 투명
draw.polygon([
    (sx1, top_y_left),
    (sx2, top_y_right),
    (sx2, bot_y_right),
    (sx1, bot_y_left),
], fill=strap_color)

# ── 하이라이트 라인 (스트랩 상단 밝은 선) ─────────────
highlight_color = (220, 220, 222, 180)
draw.polygon([
    (sx1,     top_y_left),
    (sx2,     top_y_right),
    (sx2,     top_y_right + 5),
    (sx1,     top_y_left  + 5),
], fill=highlight_color)

# ── 그림자 라인 (스트랩 하단 어두운 선) ──────────────
shadow_color = (140, 140, 142, 160)
draw.polygon([
    (sx1,     bot_y_left  - 5),
    (sx2,     bot_y_right - 5),
    (sx2,     bot_y_right),
    (sx1,     bot_y_left),
], fill=shadow_color)

# ── 스트랩 가장자리 살짝 블러 (자연스럽게) ────────────
strap_layer = strap_layer.filter(ImageFilter.GaussianBlur(radius=1.2))

# ── 원본에 합성 ───────────────────────────────────────
result = Image.alpha_composite(base, strap_layer)

# ── RGB로 저장 ────────────────────────────────────────
result.convert("RGB").save(OUT, quality=97)
print(f"✓ 저장: {OUT}")

# ── 디버그: 스트랩 위치 확인용 크롭 (3x 확대) ─────────
debug_crop = result.crop((540, 90, 720, 260))
w, h = debug_crop.size
debug_big = debug_crop.resize((w*3, h*3), Image.LANCZOS)
debug_big.save("/tmp/strap_debug_zoom.png")
print("디버그 크롭 저장: /tmp/strap_debug_zoom.png")
