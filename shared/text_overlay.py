"""
한글 텍스트 오버레이 모듈
Gemini가 생성한 비주얼 배경 위에 PIL로 한글 텍스트를 합성합니다.
Gemini의 한글 렌더링 불가 문제를 해결하는 핵심 모듈.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from PIL import Image, ImageDraw, ImageFont

# 폰트 경로
FONT_PATHS = {
    "bold": "/usr/share/fonts/truetype/nanum/NanumSquareB.ttf",
    "extrabold": "/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf",
    "regular": "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
    "noto_kr": "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
}

# 섹션별 텍스트 오버레이 색상 프리셋
COLORS = {
    "white": (255, 255, 255, 255),
    "white_80": (255, 255, 255, 204),
    "cyan": (0, 229, 255, 255),
    "dark": (10, 20, 50, 255),
    "gray": (180, 190, 210, 255),
    "light_gray": (240, 242, 248, 255),
    "blue": (0, 102, 255, 255),
    "red_accent": (255, 60, 60, 255),
}


def get_font(style: str = "bold", size: int = 48) -> ImageFont.FreeTypeFont:
    path = FONT_PATHS.get(style, FONT_PATHS["bold"])
    if not os.path.exists(path):
        path = FONT_PATHS["noto_kr"]
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def draw_text_with_shadow(
    draw: ImageDraw.ImageDraw,
    text: str,
    position: Tuple[int, int],
    font: ImageFont.FreeTypeFont,
    fill: Tuple,
    shadow_offset: int = 3,
    shadow_color: Tuple = (0, 0, 0, 180),
    align: str = "center",
    max_width: int = 1100,
):
    """그림자 효과와 함께 텍스트 그리기. 줄바꿈(\\n) 지원."""
    lines = text.split("\n")
    x, y = position

    for line in lines:
        # 텍스트 폭 측정
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]

        if align == "center":
            tx = x - text_w // 2
        elif align == "right":
            tx = x - text_w
        else:
            tx = x

        # 그림자
        draw.text((tx + shadow_offset, y + shadow_offset), line, font=font, fill=shadow_color)
        # 본문
        draw.text((tx, y), line, font=font, fill=fill)

        line_h = bbox[3] - bbox[1]
        y += line_h + 12


def draw_pill_badge(
    draw: ImageDraw.ImageDraw,
    text: str,
    center_x: int,
    y: int,
    font: ImageFont.FreeTypeFont,
    bg_color: Tuple,
    text_color: Tuple,
    padding_x: int = 32,
    padding_y: int = 14,
):
    """둥근 배지(pill) 그리기."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    rx = center_x - tw // 2 - padding_x
    ry = y
    rw = center_x + tw // 2 + padding_x
    rh = y + th + padding_y * 2
    draw.rounded_rectangle([rx, ry, rw, rh], radius=30, fill=bg_color)
    draw.text((center_x - tw // 2, y + padding_y), text, font=font, fill=text_color)


def draw_divider_line(
    draw: ImageDraw.ImageDraw,
    y: int,
    color: Tuple = (0, 229, 255, 180),
    width: int = 60,
    center_x: int = 600,
    thickness: int = 3,
):
    draw.rectangle(
        [center_x - width // 2, y, center_x + width // 2, y + thickness],
        fill=color,
    )


def overlay_section(
    section_key: str,
    image_path: str,
    brief: Dict[str, Any],
    output_path: Optional[str] = None,
) -> str:
    """섹션 이미지 위에 한글 텍스트를 오버레이합니다."""
    copy = brief.get("copy", {})
    img = Image.open(image_path).convert("RGBA")
    W, H = img.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    cx = W // 2  # 중심 x

    if section_key == "01_hero":
        # 상단 배지
        draw_pill_badge(
            draw, "🏃 러닝 전용 AR 아이웨어", cx, 50,
            get_font("bold", 28), (0, 229, 255, 220), (10, 20, 50, 255),
        )
        # 메인 헤드라인
        draw_text_with_shadow(
            draw, copy.get("hero_headline", "가민워치 이제 보지마세요,\n시야에 띄우세요"),
            (cx, H // 2 - 120),
            get_font("bold", 72), COLORS["white"], shadow_offset=4,
        )
        # 서브 헤드라인
        draw_text_with_shadow(
            draw, copy.get("hero_sub", "RunVision — 러닝 전용 AR 아이웨어"),
            (cx, H // 2 + 80),
            get_font("regular", 34), COLORS["cyan"],
        )
        # CTA 버튼
        draw_pill_badge(
            draw, "와디즈 얼리버드 후원하기 →", cx, H - 130,
            get_font("bold", 32), (0, 102, 255, 240), (255, 255, 255, 255),
            padding_x=48, padding_y=18,
        )

    elif section_key == "02_pain":
        draw_text_with_shadow(
            draw, copy.get("pain_intro", "이런 경험 있으신가요?"),
            (cx, 60), get_font("bold", 52), COLORS["dark"],
        )
        draw_divider_line(draw, 140, color=(0, 102, 255, 200), width=80)
        pain_points = copy.get("pain_points", [])
        for i, point in enumerate(pain_points):
            y_pos = 200 + i * 130
            # 번호 원
            draw.ellipse([cx - 500, y_pos - 5, cx - 455, y_pos + 40], fill=(0, 102, 255, 200))
            draw.text((cx - 488, y_pos), str(i + 1), font=get_font("bold", 28), fill=(255, 255, 255, 255))
            draw_text_with_shadow(
                draw, point, (cx - 200, y_pos),
                get_font("bold", 34), COLORS["dark"], shadow_offset=1,
                shadow_color=(0, 0, 0, 40), align="left",
            )

    elif section_key == "03_problem":
        draw_text_with_shadow(
            draw, copy.get("problem_root", "문제는 러닝이 아니라,\n'확인하는 방식'이었습니다"),
            (cx, H // 2 - 80), get_font("bold", 58), COLORS["dark"],
        )
        draw_divider_line(draw, H // 2 + 80, color=(0, 229, 255, 220), width=100)

    elif section_key == "04_story":
        draw_text_with_shadow(
            draw, "Before", (cx // 2, 60), get_font("bold", 42), COLORS["gray"],
        )
        draw_text_with_shadow(
            draw, copy.get("story_before", "손목을 드는 순간, 페이스가 끊긴다"),
            (cx // 2, 130), get_font("regular", 30), COLORS["dark"], align="center",
        )
        draw_text_with_shadow(
            draw, "After", (cx + cx // 2, 60), get_font("bold", 42), COLORS["cyan"],
        )
        draw_text_with_shadow(
            draw, copy.get("story_after", "시야 안에서 바로 확인, 흐름을 유지"),
            (cx + cx // 2, 130), get_font("regular", 30), COLORS["dark"], align="center",
        )
        # 중앙 화살표 라벨
        draw_text_with_shadow(
            draw, "→", (cx, H // 2), get_font("bold", 80), COLORS["blue"],
        )

    elif section_key == "05_solution":
        draw_text_with_shadow(
            draw, "RunVision", (cx, H // 2 - 100),
            get_font("bold", 80), COLORS["white"],
        )
        draw_divider_line(draw, H // 2 + 10, color=(0, 229, 255, 220), width=120)
        draw_text_with_shadow(
            draw, copy.get("solution_define", "러닝 전용 증강현실(AR) 아이웨어"),
            (cx, H // 2 + 40), get_font("regular", 36), COLORS["white_80"],
        )

    elif section_key == "06_how_it_works":
        draw_text_with_shadow(
            draw, "이렇게 작동합니다", (cx, 50), get_font("bold", 52), COLORS["dark"],
        )
        draw_divider_line(draw, 130, color=(0, 102, 255, 200))
        steps = copy.get("how_it_works", [])
        step_x_positions = [250, 600, 950]
        for i, (step, sx) in enumerate(zip(steps, step_x_positions)):
            draw.ellipse([sx - 40, 180, sx + 40, 260], fill=(0, 102, 255, 230))
            draw.text((sx - 12, 195), str(i + 1), font=get_font("bold", 42), fill=(255, 255, 255, 255))
            draw_text_with_shadow(
                draw, step, (sx, 290), get_font("regular", 28), COLORS["dark"],
                shadow_offset=1, shadow_color=(0, 0, 0, 30),
            )

    elif section_key == "07_social_proof":
        draw_text_with_shadow(
            draw, copy.get("social_proof_stat", "베타 테스터 27명 | 만족도 4.8/5.0"),
            (cx, 60), get_font("bold", 42), COLORS["blue"],
        )
        draw_divider_line(draw, 130)
        draw_text_with_shadow(
            draw, '"달리면서 워치 안 봐도 되니까\n너무 편해요. 페이스도 잘 유지되고."',
            (cx, 200), get_font("regular", 36), COLORS["dark"],
        )
        draw_text_with_shadow(
            draw, "— 베타테스터 김O러 (풀마라톤 완주자)",
            (cx, 380), get_font("regular", 28), COLORS["gray"],
        )

    elif section_key == "08_authority":
        draw_text_with_shadow(
            draw, copy.get("authority", "러너를 위해, 러너가 만든 제품"),
            (cx, H // 2 - 60), get_font("bold", 48), COLORS["dark"],
        )
        draw_text_with_shadow(
            draw, "RunVision Labs",
            (cx, H // 2 + 40), get_font("bold", 34), COLORS["blue"],
        )

    elif section_key == "09_benefits":
        draw_text_with_shadow(
            draw, "RunVision으로 얻는 것", (cx, 50), get_font("bold", 52), COLORS["white"],
        )
        draw_divider_line(draw, 130, color=(0, 229, 255, 220))
        features = copy.get("features", [])
        for i, feat in enumerate(features):
            y_pos = 180 + i * 85
            draw.text((cx - 450, y_pos), "✓", font=get_font("bold", 40), fill=COLORS["cyan"])
            draw_text_with_shadow(
                draw, feat, (cx - 380, y_pos),
                get_font("bold", 36), COLORS["white"],
                shadow_offset=2, align="left",
            )

    elif section_key == "10_risk_removal":
        draw_text_with_shadow(
            draw, "100% 만족 보장", (cx, 60), get_font("bold", 52), COLORS["dark"],
        )
        draw_text_with_shadow(
            draw, "와디즈 펀딩 특성상 환불 정책 및\n제품 문의는 메이커에게 직접 연락해 주세요.",
            (cx, 180), get_font("regular", 32), COLORS["dark"],
        )
        draw_text_with_shadow(
            draw, "runvision.ai@gmail.com",
            (cx, 360), get_font("bold", 30), COLORS["blue"],
        )

    elif section_key == "11_comparison":
        draw_text_with_shadow(
            draw, "기존 방식", (cx // 2, 40), get_font("bold", 44), COLORS["gray"],
        )
        draw_text_with_shadow(
            draw, "RunVision", (cx + cx // 2, 40), get_font("bold", 44), COLORS["blue"],
        )
        befores = ["손목 들어서 확인", "리듬이 끊김", "위험한 시선 분산"]
        afters = ["시야에서 바로 확인", "흐름 유지", "안전한 러닝"]
        for i, (b, a) in enumerate(zip(befores, afters)):
            y = 140 + i * 90
            draw.text((cx // 2 - 150, y), "✕  " + b, font=get_font("regular", 30), fill=COLORS["gray"])
            draw.text((cx + cx // 2 - 150, y), "✓  " + a, font=get_font("bold", 30), fill=COLORS["blue"])

    elif section_key == "12_target_filter":
        draw_text_with_shadow(
            draw, "이런 러너에게 추천합니다", (cx // 2, 40), get_font("bold", 38), COLORS["dark"],
        )
        draw_text_with_shadow(
            draw, "이런 분은 맞지 않을 수 있어요", (cx + cx // 2, 40), get_font("bold", 38), COLORS["gray"],
        )
        for_list = ["페이스 관리가 중요한 러너", "Garmin 워치 사용자", "마라톤/하프 도전 예정인 분"]
        not_for = ["GPS 워치 없는 분", "실내 러닝(트레드밀) 전용", "스마트폰 GPS만 사용"]
        for i, (f, n) in enumerate(zip(for_list, not_for)):
            y = 140 + i * 90
            draw.text((80, y), "✓  " + f, font=get_font("bold", 30), fill=COLORS["blue"])
            draw.text((cx + 80, y), "–  " + n, font=get_font("regular", 30), fill=COLORS["gray"])

    elif section_key == "13_final_cta":
        draw_text_with_shadow(
            draw, copy.get("cta_final", "지금 후원하고, 첫 번째 러너가 되세요"),
            (cx, 80), get_font("bold", 60), COLORS["white"],
        )
        draw_divider_line(draw, 180, color=(0, 229, 255, 220), width=120)
        price = brief.get("price", {})
        draw_text_with_shadow(
            draw, price.get("original", "299,000원"),
            (cx, 230), get_font("regular", 38), COLORS["gray"],
        )
        draw_text_with_shadow(
            draw, price.get("discounted", "199,000원"),
            (cx, 300), get_font("bold", 72), COLORS["cyan"],
        )
        draw_text_with_shadow(
            draw, price.get("period", "와디즈 얼리버드"),
            (cx, 400), get_font("regular", 30), COLORS["white_80"],
        )
        draw_pill_badge(
            draw, brief.get("urgency", {}).get("value", "얼리버드 한정"),
            cx, 470, get_font("bold", 28),
            (0, 229, 255, 220), (10, 20, 50, 255),
        )
        draw_pill_badge(
            draw, "지금 후원하기 →", cx, H - 130,
            get_font("bold", 38), (0, 102, 255, 240), (255, 255, 255, 255),
            padding_x=60, padding_y=22,
        )

    # 원본 이미지와 합성
    result = Image.alpha_composite(img, overlay)
    out_path = output_path or image_path
    result.convert("RGB").save(out_path, "PNG", optimize=True)
    print(f"Text overlay applied: {out_path}")
    return out_path


def overlay_all_sections(
    sections_dir: str,
    brief: Dict[str, Any],
    output_dir: Optional[str] = None,
) -> List[str]:
    """sections/ 폴더의 모든 섹션 이미지에 한글 오버레이 적용."""
    section_keys = [
        "01_hero", "02_pain", "03_problem", "04_story", "05_solution",
        "06_how_it_works", "07_social_proof", "08_authority", "09_benefits",
        "10_risk_removal", "11_comparison", "12_target_filter", "13_final_cta",
    ]
    out_dir = output_dir or sections_dir
    os.makedirs(out_dir, exist_ok=True)

    results = []
    for key in section_keys:
        src = os.path.join(sections_dir, f"{key}.png")
        if not os.path.exists(src):
            print(f"Skipping (not found): {src}")
            continue
        dst = os.path.join(out_dir, f"{key}.png")
        result = overlay_section(key, src, brief, dst)
        results.append(result)

    print(f"\nOverlay complete: {len(results)} sections processed")
    return results


if __name__ == "__main__":
    # 테스트: 01_hero 단독 오버레이
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from scripts.runvision_brief import create_runvision_brief

    brief = create_runvision_brief()
    src = "output/runvision-wadiz/sections/01_hero.png"
    if os.path.exists(src):
        overlay_section("01_hero", src, brief, "output/runvision-wadiz/sections/01_hero_text.png")
        print("Done: output/runvision-wadiz/sections/01_hero_text.png")
    else:
        print(f"File not found: {src}")
