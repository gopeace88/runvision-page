"""
HTML/CSS 섹션 생성 모듈
실제 제품 이미지 + 한글 텍스트를 HTML/CSS로 합성합니다.
Playwright로 스크린샷하여 픽셀 퍼펙트 PNG 생성.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from playwright.sync_api import sync_playwright

CHROME_PATH = "/usr/bin/google-chrome"

# 실제 제품 이미지 경로
_PICS = "/home/jhkim/00.Projects/00.RunVision/Docs/product pictures"
_PROD = "/home/jhkim/00.Projects/00.RunVision/Docs/marketing/shorts-remotion/public/product"
_VFRAMES = "/home/jhkim/00.Projects/00.RunVision/Docs/product pictures/video_frames"

PRODUCT_IMAGES = {
    # ── 동영상 프레임 (Video Frames — 실제 러닝 역동적 장면) ────
    "runner_han_river_hud":   f"{_VFRAMES}/runner_han_river_hud.jpg",       # ★Hero: 한강변 러너 + AR HUD (181BPM)
    "runner_intense_closeup": f"{_VFRAMES}/runner_intense_closeup.jpg",     # ★CTA: 얼굴 클로즈업, RunVision 안경 착용
    "runner_bridge_cityscape":f"{_VFRAMES}/runner_bridge_cityscape.jpg",    # 한강 다리 배경 러너
    "runner_ar_overlay":      f"{_VFRAMES}/runner_ar_overlay.jpg",          # 러너 + AR HUD 오버레이
    "runner_checking_wrist":  f"{_VFRAMES}/runner_checking_wrist.jpg",      # ★Story BEFORE: 달리며 손목 워치 확인 장면
    "runner_with_hud_bpm":    f"{_VFRAMES}/runner_with_hud_bpm.jpg",        # ★Story AFTER: 러너 전면 + 159BPM HUD
    "runner_fullbody_free":   f"{_VFRAMES}/runner_fullbody_free.jpg",       # 전신 러닝샷 (한강, 텍스트있음)
    "runner_product_halfbody":f"{_VFRAMES}/runner_product_halfbody.jpg",    # ★Benefits: 한국러너 반신+RunVision착용+한강
    "product_ar_module_closeup": f"{_VFRAMES}/product_ar_module_closeup.jpg", # AR모듈 클로즈업, 파란빛

    # ── 신규 고화질 사진 (New high-quality photos) ────────
    "runner_wristcheck_marathon": f"{_PICS}/chrome_dTRpr1fA1a.png",          # ★Story BEFORE: 전신 한국 마라톤 선수 + 손목확인 (레이스)
    "runner_wristcheck_asics":    f"{_PICS}/chrome_RnpfBhWGBs.png",          # ★Pain BG: ASICS 전신 러너 + 손목확인
    "runner_ar_hud_fullbody":     f"{_PICS}/chrome_vkUhDoogXX.png",          # (저화질 160px — 사용 지양)
    "runner_ar_hud_race":         f"{_PICS}/chrome_1X4p64KGpY.png",          # 레이스 AR HUD 오버레이 725×560
    "runner_ar_hud_race_hq":      f"{_PICS}/hero_runner-5.png",              # ★Story AFTER: 4:15/km·180spm·02:30:45 HUD 531×744 고화질

    # ── 실제 사진 (Real photos) ─────────────────────────
    "hud_closeup":      f"{_PICS}/02_hero_hud-display-closeup.png",         # ★Benefits: 실착용 측면, AR 디스플레이 표시
    "runner_hud":       f"{_PICS}/01_hero_runner-with-hud-149bpm.png",      # 러너 + HUD 149bpm
    "runner_hud_159bpm":f"{_PICS}/hero_runner-2.png",                        # 159BPM HUD + 핑크 AR안경 얼굴샷
    "runner_ar_product": f"{_PICS}/hero_runner-8.png",                       # ★Hero: 1120×928 AR모듈 장착+HUD 고화질
    "runner_split":     f"{_PICS}/hero_runner-4.jpeg",                      # Story: Before/After 비교 실사진
    "runner_close":     f"{_PICS}/hero_runner-3.png",                       # 러너 클로즈업

    # ── 제품 렌더 / 스튜디오샷 ──────────────────────────
    "module_glow_3d":   f"{_PICS}/03_product_module-on-glasses-hud-glow.png", # ★Benefits: 글로우 효과 3D
    "module_white":     f"{_PICS}/04_product_module-on-glasses-white-bg.png",  # 화이트 배경 전체샷
    "module_side":      f"{_PICS}/05_product_module-on-glasses-side.png",      # 측면 3D
    "module_dark_side": f"{_PICS}/05_product_module-on-glasses-side.png",        # ★Solution: 라이트 그레이 측면 클린샷 (아티팩트 없음)
    "module_standalone":f"{_PICS}/07_product_module-standalone.png",           # ★Authority: 단독 제품
    "mount_detail":     f"{_PICS}/06_product_module-mount-detail.png",         # 장착 디테일

    # ── 충전 케이스 ─────────────────────────────────────
    "charging_dark":    f"{_PICS}/11_product_charging-case-dark.png",          # 케이스 다크
    "charging_module":  f"{_PICS}/12_product_charging-case-module.png",        # ★Final CTA: 케이스+모듈

    # ── 다이어그램 / 스케치 ─────────────────────────────
    "mount_diagram":    f"{_PICS}/18_diagram_4panel-mounting-steps.png",       # 4단계 장착 다이어그램
    "mount_sketch":     f"{_PICS}/22_sketch_cap-and-glasses-mounting.png",     # 모자+안경 장착 스케치

    # ── 레거시 (일부 섹션 유지) ─────────────────────────
    "module_glass":     f"{_PROD}/module_on_glasses.png",
    "product_flat":     f"{_PROD}/scene6_cta_product.png",
}

GOOGLE_FONTS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
"""

BASE_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif; }
.section { width: 1200px; overflow: hidden; position: relative; }
"""

def img_url(key: str) -> str:
    return f"file://{PRODUCT_IMAGES[key]}"


def screenshot_html(html: str, output_path: str, width: int = 1200, height: int = 800):
    """HTML을 Chrome으로 스크린샷합니다."""
    tmp = f"/tmp/rv_{os.path.basename(output_path)}.html"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
        )
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(f"file://{tmp}")
        page.wait_for_timeout(2500)
        page.screenshot(path=output_path, full_page=False,
                        clip={"x": 0, "y": 0, "width": width, "height": height})
        browser.close()

    os.remove(tmp)
    size = os.path.getsize(output_path)
    print(f"  ✓ {output_path} ({size:,} bytes)")
    return output_path


def make_section_html(section_key: str, brief: Dict[str, Any]) -> tuple:
    """섹션별 HTML/CSS와 (width, height)를 반환합니다."""
    copy = brief.get("copy", {})
    c = brief.get("brand_colors", {})
    P = c.get("primary", "#0066FF")
    A = c.get("accent", "#00E5FF")
    D = c.get("secondary", "#001A3D")

    if section_key == "01_hero":
        hl  = copy.get("hero_headline", "가민워치 이제 보지마세요,\n시야에 띄우세요").replace("\n","<br>")
        sub = copy.get("hero_sub", "RunVision — 러닝 전용 스마트글래스")
        urg = brief.get("urgency", {}).get("value", "얼리버드 100명 한정")
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
/* 분할 레이아웃: 좌 텍스트 + 우 이미지 */
.section {{
  width:1200px; height:800px; background:{D};
  display:flex; overflow:hidden;
}}
/* 왼쪽: 텍스트 영역 */
.left {{
  width:560px; flex-shrink:0;
  display:flex; flex-direction:column; justify-content:center;
  padding:0 60px 0 80px; position:relative; z-index:2;
}}
/* 오른쪽: 이미지 패널 */
.right {{
  flex:1; position:relative; overflow:hidden;
}}
.hero-img {{
  width:100%; height:100%;
  object-fit:cover; object-position:center 30%;
}}
/* 이미지 좌측 블렌딩 — 배경색과 자연스럽게 연결 */
.img-fade {{
  position:absolute; top:0; left:0; bottom:0; width:80px;
  background:linear-gradient(to right, {D} 0%, transparent 100%);
  z-index:1;
}}
/* 하단 바닥 암막 */
.img-bottom {{
  position:absolute; bottom:0; left:0; right:0; height:120px;
  background:linear-gradient(to top, rgba(0,10,30,0.5) 0%, transparent 100%);
  z-index:1;
}}
.badge {{
  display:inline-flex; align-items:center;
  background:{A}; color:{D};
  font-size:13px; font-weight:700; letter-spacing:1px;
  padding:8px 20px; border-radius:40px;
  margin-bottom:32px; width:fit-content;
}}
h1 {{
  color:#fff; font-size:64px; font-weight:900;
  line-height:1.18; letter-spacing:-3px;
  margin-bottom:20px; word-break:keep-all;
}}
.sub {{
  color:rgba(255,255,255,0.72); font-size:19px; font-weight:400;
  letter-spacing:-0.3px; margin-bottom:44px;
}}
.cta {{
  display:inline-flex; align-items:center; gap:10px;
  background:{P}; color:#fff;
  font-size:19px; font-weight:700; letter-spacing:-0.3px;
  padding:17px 40px; border-radius:50px;
  box-shadow:0 8px 40px rgba(0,102,255,0.55);
  width:fit-content; margin-bottom:18px;
}}
.sub-note {{
  color:rgba(255,255,255,0.38); font-size:12px; letter-spacing:0.3px;
}}
</style></head>
<body><div class="section">
  <!-- 왼쪽: 텍스트 -->
  <div class="left">
    <div class="badge">🏃 {urg}</div>
    <h1>{hl}</h1>
    <div class="sub">{sub}</div>
    <div class="cta">와디즈에서 후원하기 →</div>
    <div class="sub-note">Garmin · Galaxy Watch 앱 평생 무료 · 마이크로 OLED 모듈</div>
  </div>
  <!-- 오른쪽: 이미지 그대로 -->
  <div class="right">
    <img class="hero-img" src="{img_url('runner_ar_product')}" alt="RunVision 스마트글래스">
    <div class="img-fade"></div>
    <div class="img-bottom"></div>
  </div>
</div></body></html>""", 1200, 800

    elif section_key == "02_pain":
        pts = copy.get("pain_points", [
            "달리다가 손목을 들어 워치를 확인하는 순간\n시선이 흔들리고 리듬이 끊깁니다",
            "페이스가 떨어져도 다시 올리기가 너무 힘들고\n집중력도 흐트러집니다",
            "달리면서 손목을 보는 것이 불편하고\n안전하지 않다고 느낀 적 있습니다",
        ])
        cards = "".join([f"""<div class="card">
          <div class="num">{i+1}</div>
          <div class="txt">{p.replace(chr(10),'<br>')}</div>
        </div>""" for i, p in enumerate(pts)])
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
.section {{ width:1200px; height:620px; background:{D};
  display:flex; overflow:hidden; }}
/* 왼쪽: 텍스트 + 카드 */
.left {{ width:640px; flex-shrink:0; display:flex; flex-direction:column;
  justify-content:center; padding:52px 56px; }}
.eyebrow {{ color:{A}; font-size:12px; font-weight:700;
  letter-spacing:3px; text-transform:uppercase; margin-bottom:16px; }}
h2 {{ color:#fff; font-size:40px; font-weight:900;
  letter-spacing:-1.5px; margin-bottom:10px; }}
.div {{ width:48px; height:4px; background:{P}; border-radius:2px; margin-bottom:36px; }}
.cards {{ display:flex; flex-direction:column; gap:16px; }}
.card {{ background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);
  border-left:4px solid {P}; border-radius:12px;
  padding:20px 24px; display:flex; align-items:flex-start; gap:16px; }}
.num {{ width:36px; height:36px; background:{P}; color:#fff;
  border-radius:50%; display:flex; align-items:center;
  justify-content:center; font-size:16px; font-weight:900; flex-shrink:0; margin-top:2px; }}
.txt {{ color:rgba(255,255,255,0.82); font-size:16px; font-weight:500;
  line-height:1.7; letter-spacing:-0.3px; }}
/* 오른쪽: 사진 */
.right {{ flex:1; position:relative; overflow:hidden; }}
.right img {{ width:100%; height:100%; object-fit:cover; object-position:center 30%; }}
.right-fade {{ position:absolute; inset:0;
  background:linear-gradient(to right, {D} 0%, transparent 40%); }}
.label {{ position:absolute; bottom:32px; right:28px;
  background:rgba(0,0,0,0.55); border:1px solid rgba(255,255,255,0.15);
  border-radius:10px; padding:12px 20px; text-align:right; }}
.label-main {{ color:#fff; font-size:14px; font-weight:700; }}
.label-sub {{ color:rgba(255,255,255,0.5); font-size:12px; margin-top:4px; }}
</style></head>
<body><div class="section">
  <div class="left">
    <div class="eyebrow">Pain Point</div>
    <h2>{copy.get("pain_intro","이런 경험 있으신가요?")}</h2>
    <div class="div"></div>
    <div class="cards">{cards}</div>
  </div>
  <div class="right">
    <img src="{img_url('runner_wristcheck_asics')}" alt="손목 확인 러너">
    <div class="right-fade"></div>
    <div class="label">
      <div class="label-main">달리면서 손목을 확인하는 순간</div>
      <div class="label-sub">시선이 흔들리고 페이스가 끊깁니다</div>
    </div>
  </div>
</div></body></html>""", 1200, 620

    elif section_key == "03_problem":
        lines = copy.get("problem_body","손목을 들지 않아도\n휴대폰을 열지 않아도\n달리는 시야 안에서\n필요한 정보가 바로 보인다면?").split("\n")
        line_els = "".join([f'<div class="line">{l}</div>' for l in lines if l.strip()])
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
.section {{ width:1200px; height:520px; background:#fff;
  display:flex; align-items:center; padding:0 120px; gap:80px; }}
.left {{ flex:1; }}
.eyebrow {{ color:{P}; font-size:13px; font-weight:700;
  letter-spacing:3px; text-transform:uppercase; margin-bottom:20px; }}
h2 {{ color:#0D1B2A; font-size:48px; font-weight:900;
  letter-spacing:-1.8px; line-height:1.3; margin-bottom:20px; }}
h2 span {{ color:{P}; }}
.div {{ width:64px; height:4px; background:{A}; border-radius:2px; }}
.right {{ flex:1; display:flex; flex-direction:column; gap:0;
  border-left:3px solid {A}; padding-left:40px; }}
.line {{ color:#2D3748; font-size:26px; font-weight:700;
  letter-spacing:-0.5px; padding:14px 0;
  border-bottom:1px solid #EDF2F7; }}
.line:last-child {{ border:none; }}
</style></head>
<body><div class="section">
  <div class="left">
    <div class="eyebrow">Root Cause</div>
    <h2>문제는 러닝이 아니라,<br><span>'확인하는 방식'</span>이었습니다</h2>
    <div class="div"></div>
  </div>
  <div class="right">{line_els}</div>
</div></body></html>""", 1200, 520

    elif section_key == "04_story":
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
.section {{ width:1200px; height:680px; background:{D};
  display:flex; flex-direction:column; overflow:hidden; }}
/* 상단 타이틀 영역 */
.title-bar {{ padding:44px 72px 32px; display:flex; flex-direction:column; align-items:center; flex-shrink:0; }}
.eyebrow {{ color:{A}; font-size:13px; font-weight:700;
  letter-spacing:3px; margin-bottom:12px; }}
h2 {{ color:#fff; font-size:38px; font-weight:900;
  letter-spacing:-1.5px; word-break:keep-all; text-align:center; }}
/* 사진 스플릿 비교 영역 */
.split {{ display:flex; flex:1; min-height:0; }}
.panel {{ flex:1; position:relative; overflow:hidden; }}
/* BEFORE 패널 — 흑백 필터, 아래로 내려서 손목/워치 영역 강조 */
.before-img {{
  position:absolute; inset:0; width:100%; height:100%;
  object-fit:cover; object-position:center 68%;
  filter:grayscale(40%) brightness(0.75);
}}
/* AFTER 패널 */
.after-img {{
  position:absolute; inset:0; width:100%; height:100%;
  object-fit:cover; object-position:center top;
  filter:brightness(0.9);
}}
/* 하단 레이블 오버레이 */
.panel-caption {{
  position:absolute; bottom:0; left:0; right:0;
  padding:40px 36px 32px;
  background:linear-gradient(to top, rgba(0,0,0,0.82) 0%, transparent 100%);
  display:flex; flex-direction:column;
}}
.panel-tag {{ font-size:11px; font-weight:700; letter-spacing:3px; margin-bottom:10px; }}
.before-panel .panel-tag {{ color:#FC8181; }}
.after-panel .panel-tag {{ color:{A}; }}
.panel-title {{ font-size:22px; font-weight:900; color:#fff;
  letter-spacing:-0.5px; line-height:1.4; word-break:keep-all; }}
.panel-sub {{ font-size:14px; color:rgba(255,255,255,0.65);
  margin-top:6px; letter-spacing:-0.2px; }}
/* 가운데 구분선 + VS 배지 */
.divider {{
  width:4px; background:rgba(255,255,255,0.15); flex-shrink:0;
  position:relative; z-index:10;
}}
.vs {{
  position:absolute; top:50%; left:50%;
  transform:translate(-50%,-50%);
  width:52px; height:52px; background:{P};
  border-radius:50%; border:3px solid #fff;
  display:flex; align-items:center; justify-content:center;
  color:#fff; font-size:14px; font-weight:900;
  box-shadow:0 4px 20px rgba(0,102,255,0.5);
}}
</style></head>
<body><div class="section">
  <div class="title-bar">
    <div class="eyebrow">BEFORE / AFTER</div>
    <h2>RunVision이 바꾸는 러닝의 순간</h2>
  </div>
  <div class="split">
    <!-- BEFORE: 손목 확인 장면 -->
    <div class="panel before-panel">
      <img class="before-img" src="{img_url('runner_wristcheck_marathon')}" alt="" style="object-position:center 38%;">
      <div class="panel-caption">
        <div class="panel-tag">✕  BEFORE — 기존 방식</div>
        <div class="panel-title">손목을 드는 순간<br>페이스가 끊긴다</div>
        <div class="panel-sub">리듬이 깨지면 다시 올리기가 힘듭니다</div>
      </div>
    </div>
    <!-- 구분선 -->
    <div class="divider"><div class="vs">VS</div></div>
    <!-- AFTER: 자유롭게 달리는 장면 -->
    <div class="panel after-panel">
      <img class="after-img" src="{img_url('runner_ar_hud_race_hq')}" alt="" style="object-position:center 45%;">
      <div class="panel-caption">
        <div class="panel-tag">✓  AFTER — RunVision</div>
        <div class="panel-title">시야 안에서 바로 확인<br>흐름을 유지한다</div>
        <div class="panel-sub">고개를 돌리지 않아도, 멈추지 않아도</div>
      </div>
    </div>
  </div>
</div></body></html>""", 1200, 680

    elif section_key == "05_solution":
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
.section {{ width:1200px; height:500px; background:{D};
  display:flex; align-items:center; padding:0 80px; gap:80px; overflow:hidden; }}
/* 실제 제품 이미지 — 전체 제품 표시, 라이트 배경으로 클린 렌더링 */
.img-wrap {{ flex-shrink:0; width:440px; height:340px; border-radius:24px;
  overflow:hidden; box-shadow:0 32px 80px rgba(0,0,0,0.5);
  background:#EEF2F7; display:flex; align-items:center; justify-content:center; }}
.img-wrap img {{ width:100%; height:100%; object-fit:contain; padding:16px; }}
.text {{ flex:1; display:flex; flex-direction:column; }}
.tags {{ display:flex; gap:10px; margin-bottom:20px; flex-wrap:wrap; }}
.tag {{ font-size:12px; font-weight:700; letter-spacing:2px;
  padding:6px 14px; border-radius:40px; }}
.tag-blue {{ color:{A}; border:1px solid {A}; }}
.tag-white {{ color:rgba(255,255,255,0.5); border:1px solid rgba(255,255,255,0.2); }}
h2 {{ color:#fff; font-size:58px; font-weight:900;
  letter-spacing:-3px; margin-bottom:16px; }}
.div {{ width:80px; height:4px; background:{A}; border-radius:2px; margin-bottom:24px; }}
p {{ color:rgba(255,255,255,0.7); font-size:18px; line-height:1.8;
  letter-spacing:-0.3px; max-width:480px; margin-bottom:28px; }}
.icons {{ display:flex; gap:16px; flex-wrap:wrap; }}
.icon-badge {{ display:flex; align-items:center; gap:8px;
  background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.12);
  border-radius:40px; padding:10px 20px;
  color:rgba(255,255,255,0.6); font-size:15px; font-weight:500; }}
.icon-badge span {{ color:{A}; font-weight:900; }}
</style></head>
<body><div class="section">
  <div class="img-wrap">
    <img src="{img_url('module_dark_side')}" alt="RunVision AR module">
  </div>
  <div class="text">
    <div class="tags">
      <div class="tag tag-blue">INTRODUCING</div>
      <div class="tag tag-white">오른쪽 눈 전용 스마트 글래스</div>
    </div>
    <h2>RunVision</h2>
    <div class="div"></div>
    <p>{copy.get("solution_define","달리는 중에도 시야를 흐트러뜨리지 않기 위해 설계된 러닝 전용 스마트글래스입니다.").replace(chr(10),' ')}</p>
    <div class="icons">
      <div class="icon-badge"><span>✕</span> 휴대폰</div>
      <div class="icon-badge"><span>✕</span> 손목 확인</div>
      <div class="icon-badge"><span>✓</span> 시야 안에서 바로</div>
    </div>
  </div>
</div></body></html>""", 1200, 500

    elif section_key == "06_how_it_works":
        steps = copy.get("how_it_works", [
            "Garmin · Galaxy Watch\nBLE 자동 연결",
            "마이크로 OLED에 러닝 데이터\n실시간 표시",
            "러닝 종료 후\n데이터 자동 저장",
        ])
        step_els = ""
        for i, s in enumerate(steps):
            arrow = '<div class="arr">→</div>' if i < len(steps)-1 else ''
            step_els += f"""<div class="step">
              <div class="circle">{i+1}</div>
              <div class="stxt">{s.replace(chr(10),'<br>')}</div>
            </div>{arrow}"""
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
.section {{ width:1200px; height:700px; background:#F2F5FA;
  display:flex; flex-direction:column; align-items:center;
  justify-content:center; padding:56px 80px; gap:0; }}
.eyebrow {{ color:{P}; font-size:13px; font-weight:700;
  letter-spacing:3px; margin-bottom:14px; }}
h2 {{ color:#0D1B2A; font-size:46px; font-weight:900;
  letter-spacing:-1.5px; margin-bottom:12px; }}
.div {{ width:56px; height:4px; background:{A}; border-radius:2px;
  margin-bottom:48px; }}
.row {{ display:flex; align-items:center; gap:0; width:100%;
  margin-bottom:48px; }}
.step {{ flex:1; display:flex; flex-direction:column;
  align-items:center; gap:20px; }}
.circle {{ width:80px; height:80px; background:{P}; color:#fff;
  border-radius:50%; display:flex; align-items:center;
  justify-content:center; font-size:36px; font-weight:900;
  box-shadow:0 8px 28px rgba(0,102,255,0.35); }}
.stxt {{ color:#2D3748; font-size:18px; font-weight:700;
  text-align:center; line-height:1.6; letter-spacing:-0.3px; }}
.arr {{ color:{A}; font-size:36px; font-weight:700;
  flex-shrink:0; padding:0 8px; margin-bottom:32px; }}
/* 장착 방식 안내 */
.mount-row {{ display:flex; gap:24px; width:100%; }}
.mount-card {{ flex:1; background:#fff; border-radius:20px;
  overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08);
  display:flex; align-items:center; gap:0; }}
.mount-img {{ width:160px; height:100px; object-fit:cover;
  object-position:center; flex-shrink:0; }}
.mount-txt {{ padding:20px 28px; }}
.mount-label {{ color:{P}; font-size:12px; font-weight:700;
  letter-spacing:2px; margin-bottom:6px; }}
.mount-title {{ color:#0D1B2A; font-size:18px; font-weight:900;
  letter-spacing:-0.5px; margin-bottom:4px; }}
.mount-desc {{ color:#718096; font-size:14px; line-height:1.5; }}
</style></head>
<body><div class="section">
  <div class="eyebrow">HOW IT WORKS</div>
  <h2>이렇게 작동합니다</h2>
  <div class="div"></div>
  <div class="row">{step_els}</div>
  <div class="mount-row">
    <div class="mount-card">
      <img class="mount-img" src="{img_url('module_white')}" alt="안경 장착">
      <div class="mount-txt">
        <div class="mount-label">MOUNTING TYPE A</div>
        <div class="mount-title">안경 장착형</div>
        <div class="mount-desc">기존 안경 프레임에 바로 장착<br>렌즈 교체 없이 착용 가능</div>
      </div>
    </div>
    <div class="mount-card">
      <img class="mount-img" src="{img_url('mount_sketch')}" alt="모자 장착">
      <div class="mount-txt">
        <div class="mount-label">MOUNTING TYPE B</div>
        <div class="mount-title">러닝 캡 장착형</div>
        <div class="mount-desc">모자 챙에 클립으로 장착<br>안경 없이도 착용 가능</div>
      </div>
    </div>
  </div>
</div></body></html>""", 1200, 700

    elif section_key == "07_social_proof":
        tms = copy.get("testimonials", [
            {"quote":"달리면서 워치 안 봐도 되니까 너무 편해요. 페이스도 훨씬 잘 유지됩니다.","name":"김○○ · 하프마라톤 러너"},
            {"quote":"Garmin 워치랑 연동이 정말 자연스러워요. 디스플레이가 선명하고 착용감도 좋습니다.","name":"이○○ · 마라톤 완주자"},
            {"quote":"고개를 내릴 필요가 없어서 러닝 폼이 안정됐어요. 기록도 개선됐습니다.","name":"박○○ · 10km 생활체육"},
        ])
        cards = "".join([f"""<div class="card">
          <div class="stars">★★★★★</div>
          <p class="qt">"{t['quote']}"</p>
          <div class="who">— {t['name']}</div>
        </div>""" for t in tms])
        stat_txt = copy.get("social_proof_stat","베타 테스터 27명 · 만족도 4.8/5.0 · 페이스 유지율 +12%")
        stats = [s.strip() for s in stat_txt.split("·")]
        stat_els = "".join([f'<div class="stat"><div class="sn">{s.split()[0]}</div><div class="sl">{" ".join(s.split()[1:])}</div></div>' for s in stats if s])
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
.section {{ width:1200px; height:800px; background:#fff;
  display:flex; flex-direction:column; align-items:center;
  padding:56px 72px; }}
.eyebrow {{ color:{P}; font-size:13px; font-weight:700;
  letter-spacing:3px; margin-bottom:14px; }}
h2 {{ color:#0D1B2A; font-size:46px; font-weight:900;
  letter-spacing:-1.5px; margin-bottom:12px; }}
.div {{ width:56px; height:4px; background:{A}; border-radius:2px; margin-bottom:40px; }}
.stats {{ display:flex; width:100%; background:{D}; border-radius:20px;
  padding:36px 0; margin-bottom:40px; }}
.stat {{ flex:1; text-align:center;
  border-right:1px solid rgba(255,255,255,0.1); }}
.stat:last-child {{ border:none; }}
.sn {{ color:{A}; font-size:46px; font-weight:900; letter-spacing:-2px; }}
.sl {{ color:rgba(255,255,255,0.55); font-size:15px; margin-top:6px; }}
.cards {{ display:flex; gap:20px; width:100%; }}
.card {{ flex:1; background:#F8FAFF; border-radius:16px; padding:32px;
  border:1px solid #E2E8F0; display:flex; flex-direction:column; gap:16px; }}
.stars {{ color:#FFB800; font-size:18px; letter-spacing:2px; }}
.qt {{ color:#2D3748; font-size:16px; line-height:1.8;
  letter-spacing:-0.3px; font-style:italic; flex:1; }}
.who {{ color:#A0AEC0; font-size:13px; font-weight:700; }}
</style></head>
<body><div class="section">
  <div class="eyebrow">SOCIAL PROOF</div>
  <h2>베타 테스터의 실제 후기</h2>
  <div class="div"></div>
  <div class="stats">{stat_els}</div>
  <div class="cards">{cards}</div>
</div></body></html>""", 1200, 800

    elif section_key == "08_authority":
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
.section {{ width:1200px; height:480px; background:#F2F5FA;
  display:flex; align-items:center; padding:0 100px; gap:80px; }}
.img-wrap {{ flex-shrink:0; width:220px; height:220px; border-radius:50%;
  overflow:hidden; box-shadow:0 16px 48px rgba(0,102,255,0.25);
  border:4px solid {P}; }}
.img-wrap img {{ width:100%; height:100%; object-fit:cover; object-position:top; }}
.info {{ flex:1; }}
.eyebrow {{ color:{P}; font-size:13px; font-weight:700;
  letter-spacing:3px; margin-bottom:16px; }}
h3 {{ color:#0D1B2A; font-size:40px; font-weight:900;
  letter-spacing:-1.5px; margin-bottom:8px; }}
.title {{ color:{P}; font-size:18px; font-weight:700; margin-bottom:24px; }}
.div {{ width:48px; height:3px; background:{A}; border-radius:2px; margin-bottom:20px; }}
p {{ color:#4A5568; font-size:17px; line-height:1.8; letter-spacing:-0.3px; }}
</style></head>
<body><div class="section">
  <div class="img-wrap">
    <img src="{img_url('module_standalone')}" alt="RunVision product">
  </div>
  <div class="info">
    <div class="eyebrow">ABOUT MAKER</div>
    <h3>RunVision Labs</h3>
    <div class="title">러너를 위해, 러너가 만든 제품</div>
    <div class="div"></div>
    <p>{copy.get("authority","실제 마라톤 러너가 만든 프로젝트입니다. Garmin · Galaxy Watch 연동 앱과 스마트글래스를 직접 개발하며 수백 시간의 테스트를 거쳤습니다.").replace(chr(10),'<br>')}</p>
  </div>
</div></body></html>""", 1200, 480

    elif section_key == "09_benefits":
        feats = copy.get("features", ["현재 페이스","총 거리","심박수","케이던스","러닝 타임"])
        feat_els = "".join([f'<div class="feat"><span class="ck">✓</span><span>{f}</span></div>' for f in feats])
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
/* Split panel: 왼쪽 dark, 오른쪽 light — 배경색 다른 제품 이미지 자연스럽게 처리 */
.section {{ width:1200px; height:680px; display:flex; overflow:hidden; }}
.left {{
  flex:1; background:{D};
  display:flex; flex-direction:column; justify-content:center;
  padding:60px 60px 60px 80px;
}}
.eyebrow {{ color:{A}; font-size:13px; font-weight:700;
  letter-spacing:3px; margin-bottom:16px; }}
h2 {{ color:#fff; font-size:42px; font-weight:900;
  letter-spacing:-1.5px; margin-bottom:14px; line-height:1.3;
  word-break:keep-all; }}
.div {{ width:56px; height:4px; background:{A}; border-radius:2px; margin-bottom:32px; }}
.feats {{ display:flex; flex-direction:column; gap:14px; }}
.feat {{ display:flex; align-items:center; gap:16px;
  background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.1);
  border-radius:12px; padding:16px 22px;
  color:#fff; font-size:17px; font-weight:500; letter-spacing:-0.3px; }}
.ck {{ color:{A}; font-size:18px; font-weight:900; flex-shrink:0; }}
.bonus {{ margin-top:18px; background:rgba(0,229,255,0.1);
  border:1px solid rgba(0,229,255,0.3); border-radius:12px;
  padding:16px 22px; color:{A}; font-size:15px; font-weight:700;
  text-align:center; }}
/* 오른쪽 패널 — 실제 러닝 중 착용 장면 풀블리드 */
.right {{
  flex-shrink:0; width:440px; position:relative; overflow:hidden;
}}
.right-img {{
  position:absolute; inset:0; width:100%; height:100%;
  object-fit:contain; object-position:center center;
  background:{D};
}}
/* 왼쪽 경계 — dark에서 이미지로 자연스럽게 */
.right-fade {{
  position:absolute; inset:0;
  background:linear-gradient(to right, {D} 0%, transparent 30%);
}}
/* 우측 하단 제품 레이블 */
.prod-label {{
  position:absolute; bottom:24px; right:24px; text-align:right; z-index:2;
  background:rgba(0,10,30,0.65); padding:12px 18px; border-radius:12px;
  backdrop-filter:blur(6px);
}}
.prod-name {{ color:#fff; font-size:14px; font-weight:900;
  letter-spacing:-0.3px; margin-bottom:2px; }}
.prod-tag {{ color:{A}; font-size:11px; font-weight:700;
  letter-spacing:1px; }}
</style></head>
<body><div class="section">
  <div class="left">
    <div class="eyebrow">BENEFITS</div>
    <h2>{copy.get("feature_headline","필요한 정보는, 시야 안에 그대로 나타납니다")}</h2>
    <div class="div"></div>
    <div class="feats">{feat_els}</div>
    <div class="bonus">🎁 얼리버드: Garmin · Galaxy Watch 앱 평생 무료 제공</div>
  </div>
  <div class="right">
    <img class="right-img" src="{img_url('hud_closeup')}" alt="RunVision 스마트글래스">
    <div class="right-fade"></div>
    <div class="prod-label">
      <div class="prod-name">RunVision 스마트글래스</div>
      <div class="prod-tag">실착용 · 마이크로 OLED 실시간 표시</div>
    </div>
  </div>
</div></body></html>""", 1200, 680

    elif section_key == "10_risk_removal":
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
.section {{ width:1200px; height:480px; background:#fff;
  display:flex; flex-direction:column; align-items:center;
  justify-content:center; padding:60px 120px; }}
.badge-wrap {{ display:flex; align-items:center; gap:16px; margin-bottom:32px; }}
.shield {{ font-size:52px; }}
.badge-txt {{ color:{P}; font-size:20px; font-weight:900;
  letter-spacing:-0.5px; }}
h2 {{ color:#0D1B2A; font-size:48px; font-weight:900;
  letter-spacing:-1.5px; margin-bottom:14px; text-align:center; }}
.div {{ width:56px; height:4px; background:{A}; border-radius:2px;
  margin:0 auto 28px; }}
p {{ color:#4A5568; font-size:18px; line-height:1.8;
  text-align:center; max-width:680px; letter-spacing:-0.3px; margin-bottom:24px; }}
.contact {{ color:{P}; font-size:17px; font-weight:700; }}
</style></head>
<body><div class="section">
  <div class="badge-wrap"><span class="shield">🛡</span>
    <span class="badge-txt">메이커 직접 대응 보장</span></div>
  <h2>100% 만족 보장</h2>
  <div class="div"></div>
  <p>와디즈 펀딩 특성상 제품 수령 후 불만족 시 메이커에게 직접 문의해 주세요.<br>성실하게 대응하겠습니다.</p>
  <div class="contact">📧 support@runvision.ai</div>
</div></body></html>""", 1200, 480

    elif section_key == "11_comparison":
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
.section {{ width:1200px; height:420px; background:#F2F5FA;
  display:flex; align-items:center; justify-content:center;
  padding:48px 72px; gap:20px; }}
.col {{ flex:1; border-radius:20px; padding:36px 40px; }}
.before {{ background:#fff; border:2px solid #E2E8F0; }}
.after {{ background:{D}; border:2px solid {P}; }}
.col-h {{ font-size:20px; font-weight:900; letter-spacing:-0.5px;
  margin-bottom:24px; padding-bottom:18px; border-bottom:2px solid; }}
.before .col-h {{ color:#A0AEC0; border-color:#E2E8F0; }}
.after .col-h {{ color:#fff; border-color:rgba(0,102,255,0.4); }}
.row {{ display:flex; align-items:center; gap:14px;
  font-size:17px; font-weight:500; padding:12px 0;
  border-bottom:1px solid rgba(0,0,0,0.06); }}
.after .row {{ border-color:rgba(255,255,255,0.08); }}
.before .row {{ color:#A0AEC0; }}
.after .row {{ color:rgba(255,255,255,0.9); }}
.before .row:last-child {{ border:none; }}
.after .row:last-child {{ border:none; }}
.x {{ color:#E53E3E; font-weight:900; }}
.ck {{ color:{A}; font-weight:900; }}
.vs {{ color:{A}; font-size:32px; font-weight:900;
  flex-shrink:0; padding:0 8px; }}
</style></head>
<body><div class="section">
  <div class="col before">
    <div class="col-h">기존 방식 (워치/폰)</div>
    <div class="row"><span class="x">✕</span> 손목 들어서 확인 → 속도 감소</div>
    <div class="row"><span class="x">✕</span> 리듬이 끊기고 집중력 저하</div>
    <div class="row"><span class="x">✕</span> 시선 분산 → 안전 위험</div>
  </div>
  <div class="vs">VS</div>
  <div class="col after">
    <div class="col-h">✦ RunVision 스마트글래스</div>
    <div class="row"><span class="ck">✓</span> 시야에서 바로 확인 → 속도 유지</div>
    <div class="row"><span class="ck">✓</span> 흐름 유지, 집중력 극대화</div>
    <div class="row"><span class="ck">✓</span> 전방 주시 → 안전한 러닝</div>
  </div>
</div></body></html>""", 1200, 420

    elif section_key == "12_target_filter":
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
.section {{ width:1200px; height:400px; background:#fff;
  display:flex; align-items:center; justify-content:center;
  padding:40px 72px; gap:24px; }}
.col {{ flex:1; border-radius:20px; padding:36px 40px; height:100%; }}
.for {{ background:#EBF8FF; border:2px solid #BEE3F8; }}
.not {{ background:#F7FAFC; border:2px solid #E2E8F0; }}
.col-h {{ font-size:18px; font-weight:900; letter-spacing:-0.3px;
  margin-bottom:24px; padding-bottom:14px; border-bottom:2px solid; }}
.for .col-h {{ color:{P}; border-color:#BEE3F8; }}
.not .col-h {{ color:#A0AEC0; border-color:#E2E8F0; }}
.item {{ font-size:16px; font-weight:500; padding:10px 0;
  border-bottom:1px solid rgba(0,0,0,0.05); display:flex; gap:10px; }}
.item:last-child {{ border:none; }}
.for .item {{ color:#2C5282; }}
.not .item {{ color:#718096; }}
</style></head>
<body><div class="section">
  <div class="col for">
    <div class="col-h">✓ 이런 분께 추천합니다</div>
    <div class="item">🏃 페이스 관리가 중요한 러너</div>
    <div class="item">⌚ Garmin · Galaxy Watch 사용자</div>
    <div class="item">🎯 마라톤·하프 도전 예정인 분</div>
  </div>
  <div class="col not">
    <div class="col-h">— 이런 분은 맞지 않을 수 있어요</div>
    <div class="item">📱 GPS 워치 없이 스마트폰만 사용</div>
    <div class="item">🏠 실내 트레드밀 전용 러너</div>
    <div class="item">🚶 걷기 위주, 러닝 비중 낮은 분</div>
  </div>
</div></body></html>""", 1200, 400

    elif section_key == "13_final_cta":
        price = brief.get("price", {})
        urg   = brief.get("urgency", {})
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{GOOGLE_FONTS}
<style>
{BASE_CSS}
.section {{ width:1200px; height:620px; background:{D}; overflow:hidden; }}
/* 제품 플랫레이 배경 */
.bg {{ position:absolute; right:0; top:0; width:560px; height:100%;
  object-fit:cover; object-position:center; opacity:0.7; }}
.fade {{ position:absolute; inset:0;
  background:linear-gradient(to right,
    {D} 0%, {D} 40%, rgba(0,26,61,0.8) 65%, transparent 100%); }}
.content {{ position:absolute; inset:0; display:flex;
  flex-direction:column; justify-content:center;
  padding:0 580px 0 80px; }}
h2 {{ color:#fff; font-size:46px; font-weight:900; letter-spacing:-1.5px;
  line-height:1.3; margin-bottom:10px; word-break:keep-all; }}
.sub {{ color:rgba(255,255,255,0.55); font-size:17px;
  margin-bottom:44px; letter-spacing:-0.3px; }}
.price-row {{ display:flex; align-items:baseline; gap:20px; margin-bottom:8px; }}
.orig {{ color:rgba(255,255,255,0.3); font-size:26px;
  text-decoration:line-through; }}
.sale {{ color:{A}; font-size:64px; font-weight:900; letter-spacing:-2px; }}
.period {{ color:rgba(255,255,255,0.45); font-size:15px;
  margin-bottom:32px; }}
.cta {{ display:inline-flex; align-items:center; gap:10px;
  background:{P}; color:#fff; font-size:22px; font-weight:900;
  padding:20px 56px; border-radius:50px; letter-spacing:-0.5px;
  box-shadow:0 0 40px rgba(0,102,255,0.55); width:fit-content;
  margin-bottom:20px; }}
.urgency {{ color:{A}; font-size:15px; font-weight:700; }}
</style></head>
<body><div class="section">
  <img class="bg" src="{img_url('runner_intense_closeup')}" alt="">
  <div class="fade"></div>
  <div class="content">
    <h2>지금 후원하고,<br>첫번째 런비전 러너가 되세요</h2>
    <p class="sub">RunVision 와디즈 얼리버드 · 한정 수량</p>
    <div class="price-row">
      <span class="orig">{price.get("original","299,000원")}</span>
      <span class="sale">{price.get("discounted","199,000원")}</span>
    </div>
    <p class="period">{price.get("period","와디즈 얼리버드 특가")}</p>
    <div class="cta">와디즈에서 후원하기 →</div>
    <div class="urgency">🔥 {urg.get("value","얼리버드 100명 한정")} · {urg.get("bonus","Garmin · Galaxy Watch 앱 무료 제공")}</div>
    <div style="margin-top:16px;color:rgba(255,255,255,0.3);font-size:13px;">문의: support@runvision.ai</div>
  </div>
</div></body></html>""", 1200, 620

    return None, 0, 0


SECTION_LIST = [
    "01_hero", "02_pain", "03_problem", "04_story", "05_solution",
    "06_how_it_works", "07_social_proof", "08_authority", "09_benefits",
    "10_risk_removal", "11_comparison", "12_target_filter", "13_final_cta",
]


def generate_all_sections(brief: Dict[str, Any], output_dir: str) -> list:
    """모든 섹션을 HTML→PNG로 생성합니다."""
    os.makedirs(output_dir, exist_ok=True)
    results = []
    for key in SECTION_LIST:
        result = make_section_html(key, brief)
        if result[0] is None:
            continue
        html, w, h = result
        out = os.path.join(output_dir, f"{key}.png")
        print(f"\n[{key}] {w}x{h}...")
        screenshot_html(html, out, w, h)
        results.append(out)
    return results


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from scripts.runvision_brief import create_runvision_brief

    brief = create_runvision_brief()
    out_dir = "output/runvision-wadiz/sections"

    # 전체 13개 섹션 생성
    results = generate_all_sections(brief, out_dir)
    print(f"\nDone: {len(results)}/13 sections generated → {out_dir}/")
