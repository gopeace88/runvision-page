"""
카페24 상세페이지 생성기
- 와디즈 버전 기반으로 카페24 전용 copy 패치
- 1200px 렌더링 → 860px 리사이즈 (카페24 표준)
"""
import os
import sys
import copy
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.html_sections import make_section_html, screenshot_html, SECTION_LIST
from scripts.runvision_brief import create_runvision_brief

OUTPUT_DIR = "output/runvision-caffe24/sections"
CAFFE24_WIDTH = 860

# 와디즈 → 카페24 HTML 문자열 치환
REPLACEMENTS = [
    ("와디즈에서 후원하기 →",         "지금 구매하기 →"),
    ("RunVision 와디즈 얼리버드 · 한정 수량", "RunVision 공식 스토어 · 한정 수량"),
    ("🎁 얼리버드:",                  "🎁 구매 혜택:"),
    ("와디즈 얼리버드 특가",           "런치 특가"),
    ("와디즈 펀딩 특성상 제품 수령 후 불만족 시 메이커에게 직접 문의해 주세요.",
     "제품 수령 후 7일 이내 교환/반품 가능합니다. 고객센터로 문의해 주세요."),
    ("성실하게 대응하겠습니다.",        ""),
    ("🏃 얼리버드 100명 한정",         "🏃 한정 수량"),
    ("지금 후원하고,<br>첫번째 런비전 러너가 되세요", "지금 구매하고,<br>첫번째 런비전 러너가 되세요"),
]


def patch_html(html: str) -> str:
    for old, new in REPLACEMENTS:
        html = html.replace(old, new)
    return html


def resize_to_860(src: str, dst: str):
    img = Image.open(src)
    w, h = img.size
    new_h = int(h * CAFFE24_WIDTH / w)
    resized = img.resize((CAFFE24_WIDTH, new_h), Image.LANCZOS)
    resized.save(dst)


def main():
    brief = create_runvision_brief()
    # 카페24용 brief 패치
    brief["urgency"]["value"] = "한정 수량"
    brief["urgency"]["bonus"] = "가민 · 갤럭시 워치 앱 평생 무료"
    brief["price"]["period"] = "런치 특가"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tmp = "/tmp/cafe24_section_tmp.png"

    for section in SECTION_LIST:
        html, w, h = make_section_html(section, brief)
        html = patch_html(html)
        screenshot_html(html, tmp, w, h)
        out = f"{OUTPUT_DIR}/{section}.png"
        resize_to_860(tmp, out)
        print(f"  ✓ {section} → {CAFFE24_WIDTH}px")

    print(f"\n완료: {len(SECTION_LIST)}개 섹션 → {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
