"""
PIL 합성: 실제 제품을 모자 챙 바로 아래에 정확히 배치
- rembg 배경 제거
- 90° 회전으로 수평 배치
- 챙 하단에 FLUSH 배치
- 어두운 스트랩 추가
"""

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from rembg import remove
import numpy as np

PICS      = "/home/jhkim/00.Projects/00.RunVision/Docs/product pictures/"
BASE      = PICS + "cap_male_corrected.png"
PROD      = PICS + "07_product_module-standalone.png"
OUT       = PICS + "cap_male_pil.png"

# ── 1. 기반 이미지 로드 ─────────────────────────────────────
base = Image.open(BASE).convert("RGBA")
W, H = base.size
print(f"기반 이미지: {W}x{H}")

# ── 2. 제품 배경 제거 ───────────────────────────────────────
prod_raw = Image.open(PROD).convert("RGBA")
prod_nobg = remove(prod_raw)

# ── 3. 제품 회전: 90° CW → 수평으로 (클립=왼쪽, 디스플레이=오른쪽)
# 원본: 수직 (clip 위, display 아래)
# 90° CW 후: clip=오른쪽, display=왼쪽
# 좌우반전: clip=왼쪽(바깥), display=오른쪽(눈쪽)
prod_rot = prod_nobg.rotate(-90, expand=True)  # CW 90°
prod_rot = prod_rot.transpose(Image.FLIP_LEFT_RIGHT)  # 좌우반전

# ── 4. 크기 조정: 챙 너비에 맞게 (약 150px)
TARGET_W = 150
ratio    = TARGET_W / prod_rot.width
TARGET_H = max(1, int(prod_rot.height * ratio))
prod_sized = prod_rot.resize((TARGET_W, TARGET_H), Image.LANCZOS)
print(f"제품 크기 조정: {prod_rot.width}x{prod_rot.height} → {TARGET_W}x{TARGET_H}")

# ── 5. 챙 하단 위치 찾기 ────────────────────────────────────
# 모자가 검정색 → 어두운 픽셀의 하단 경계를 왼쪽 영역에서 탐색
arr = np.array(base.convert("RGB"))
# 왼쪽 50% 영역에서 캡 하단 찾기
left_half = arr[:, :W//2, :]
# 어두운 픽셀 (R+G+B < 150) → 검정 캡
dark = (left_half[:,:,0].astype(int) +
        left_half[:,:,1].astype(int) +
        left_half[:,:,2].astype(int)) < 150

ys, xs = np.where(dark)
if len(ys):
    # 왼쪽 절반에서 어두운 픽셀의 하단 찾기 (y 범위 50-400)
    mask = (ys > 50) & (ys < 400)
    if mask.sum() > 0:
        brim_y = int(ys[mask].max())  # 챙 하단 y
        brim_x_center = int(xs[mask & (ys == ys[mask].max())].mean())
    else:
        brim_y = 220  # fallback
        brim_x_center = 200
    print(f"챙 하단: y={brim_y}, x_center={brim_x_center}")
else:
    brim_y = 220
    brim_x_center = 200
    print(f"챙 자동 탐지 실패, fallback: y={brim_y}")

# ── 6. 제품 배치 좌표 결정 ──────────────────────────────────
# 제품 상단이 brim_y에 맞닿도록 (flush)
paste_y = brim_y - 5  # 5px 겹치게 → 챙에 붙어있는 효과
paste_x = brim_x_center - TARGET_W // 2
print(f"배치 위치: x={paste_x}, y={paste_y}")

# ── 7. 어두운 스트랩 그리기 ─────────────────────────────────
# 제품 위에 어두운 클립 스트랩 (챙을 가로지르는 어두운 밴드)
result = base.copy()
draw   = ImageDraw.Draw(result)

# 스트랩: 제품 왼쪽에서 가로로 가느다란 어두운 밴드
strap_x1 = paste_x
strap_x2 = paste_x + TARGET_W
strap_y  = brim_y - 8   # 챙 위에 걸치는 스트랩
strap_h  = 14            # 스트랩 두께

# 어두운 반투명 스트랩
strap = Image.new("RGBA", (strap_x2 - strap_x1, strap_h), (30, 30, 35, 220))
result.paste(strap, (strap_x1, strap_y), strap)

# ── 8. 제품 붙이기 (알파 합성) ──────────────────────────────
result.paste(prod_sized, (paste_x, paste_y), prod_sized)

# ── 9. 제품 가장자리 부드럽게 ───────────────────────────────
# 결과물 RGB 저장
final = result.convert("RGB")
final.save(OUT, quality=95)
print(f"✓ 저장: {OUT}")

# ── 10. 디버그: 배치 위치 표시 버전 저장 ────────────────────
debug = result.copy()
dd = ImageDraw.Draw(debug)
dd.rectangle([paste_x, paste_y, paste_x+TARGET_W, paste_y+TARGET_H], outline=(255,0,0,255), width=2)
dd.rectangle([strap_x1, strap_y, strap_x2, strap_y+strap_h], outline=(0,255,0,255), width=2)
debug.convert("RGB").save(PICS + "cap_male_pil_debug.png")
print(f"디버그 저장: cap_male_pil_debug.png (빨강=제품, 초록=스트랩)")
