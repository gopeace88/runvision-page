"""
피그마 디자인 기반 HTML/CSS 섹션 생성기
디자이너 피그마(런비전 상세페이지)를 로컬에서 실제 제품 이미지로 재현합니다.

너비: 860px (와디즈 상세페이지 표준)
색상: #FFFFFF 배경 / #000000 텍스트 / #00C4C4 포인트
폰트: Noto Sans KR (피그마 Inter 대체)
"""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright

CHROME_PATH = "/usr/bin/google-chrome"

# ── 이미지 경로 ──────────────────────────────────────────
_PICS   = "/home/jhkim/00.Projects/00.RunVision/Docs/product pictures"
_VFRAMES = f"{_PICS}/video_frames"

IMGS = {
    # 러너 + HUD
    "runner_hud_hero":    f"{_PICS}/hero_runner-6.png",
    "runner_hud_bpm":     f"{_VFRAMES}/runner_with_hud_bpm.jpg",
    "runner_ar_race":     f"{_PICS}/hero_runner-5.png",           # 4:15/km HUD
    "runner_closeup":     f"{_PICS}/hero_runner-8.png",
    "runner_product":     f"{_PICS}/hero_runner-8.png",
    "runner_hud_159":     f"{_PICS}/hero_runner-2.png",

    # 손목 확인 (BEFORE)
    "runner_wrist_race":  f"{_PICS}/chrome_dTRpr1fA1a.png",
    "runner_wrist_asics": f"{_PICS}/chrome_dTRpr1fA1a.png",

    # 제품샷
    "module_side":        f"{_PICS}/05_product_module-on-glasses-side.png",
    "module_white":       f"{_PICS}/04_product_module-on-glasses-white-bg.png",
    "module_glow":        f"{_PICS}/03_product_module-on-glasses-hud-glow.png",
    "module_standalone":  f"{_PICS}/07_product_module-standalone.png",
    "hud_closeup":        f"{_PICS}/02_hero_hud-display-closeup.png",
    "mount_detail":       f"{_PICS}/06_product_module-mount-detail.png",
    "mount_diagram":      f"{_PICS}/18_diagram_4panel-mounting-steps.png",

    # 충전케이스
    "charging_case":      f"{_PICS}/11_product_charging-case-dark.png",
    "charging_module":    f"{_PICS}/12_product_charging-case-module.png",

    # 스펙
    "spec_overview":      f"{_PICS}/14_spec_full-product-overview.png",

    # 마운팅
    "mount_cap":          "/home/jhkim/00.Projects/00.RunVision/Docs/사용자 메뉴얼/docx_images/08.png",
    "mount_both":         f"{_PICS}/22_sketch_cap-and-glasses-mounting.png",
    "glasses_glow":       f"{_PICS}/03_product_module-on-glasses-hud-glow.png",

    # 라이프스타일
    "cap_lifestyle":      f"{_PICS}/cap_female_strap.png",
    "glasses_lifestyle":  f"{_PICS}/glasses_lifestyle_female.png",
    "garmin_watch":       f"{_PICS}/garmin watch fr165-01.webp",

    # 장착 스케치
    "mount_sketch_glasses": f"{_PICS}/mount_sketch_glasses.jpg",
    "mount_sketch_cap":     f"{_PICS}/mount_sketch_cap.png",
}

def img(key): return f"file://{IMGS[key]}"

# ── 공통 CSS ─────────────────────────────────────────────
FONTS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
"""
RESET = """
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Noto Sans KR', sans-serif; }
.wrap { width:860px; overflow:hidden; }
"""

TEAL   = "#00C4C4"
DARK   = "#0A1628"
WHITE  = "#FFFFFF"
BLACK  = "#000000"
GRAY   = "#F5F5F5"


# ─────────────────────────────────────────────────────────
# SECTION 1: 인트로(1) — AR HUD Hero
# ─────────────────────────────────────────────────────────
def section_intro1():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}
<style>{RESET}
.wrap {{ background:{DARK}; }}

/* 상단 어두운 배너 영역 */
.hero-top {{
  position:relative; width:860px; height:520px; overflow:hidden;
}}
.hero-bg {{
  position:absolute; inset:0; width:100%; height:100%;
  object-fit:cover; object-position:center 20%;
  filter:brightness(0.55);
}}
.hero-overlay {{
  position:absolute; inset:0;
  background:linear-gradient(to bottom, rgba(10,22,40,0.3) 0%, rgba(10,22,40,0.85) 100%);
}}
.hero-text {{
  position:absolute; bottom:60px; left:60px; right:60px;
}}
.hero-badge {{
  display:inline-block; background:{TEAL}; color:{DARK};
  font-size:12px; font-weight:700; letter-spacing:2px;
  padding:6px 18px; border-radius:30px; margin-bottom:20px;
}}
.hero-title {{
  color:{WHITE}; font-size:48px; font-weight:900;
  line-height:1.25; letter-spacing:-2px; word-break:keep-all;
  margin-bottom:14px;
}}
.hero-sub {{
  color:rgba(255,255,255,0.65); font-size:18px; font-weight:300;
  letter-spacing:-0.3px;
}}

/* HUD 디스플레이 영역 */
.hud-zone {{
  background:{DARK}; padding:40px 60px 0;
}}
.hud-label {{
  color:{TEAL}; font-size:12px; font-weight:700;
  letter-spacing:3px; margin-bottom:24px; text-align:center;
}}
.hud-frame {{
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(0,196,196,0.25);
  border-radius:16px; padding:32px 40px;
  display:flex; justify-content:space-between; align-items:center;
  margin-bottom:24px;
}}
.hud-metric {{
  text-align:center; flex:1;
}}
.hud-value {{
  color:{WHITE}; font-size:42px; font-weight:900;
  letter-spacing:-2px; line-height:1;
}}
.hud-unit {{
  color:rgba(255,255,255,0.45); font-size:13px;
  font-weight:300; letter-spacing:1px; margin-top:6px;
}}
.hud-divider {{
  width:1px; height:60px;
  background:rgba(255,255,255,0.12); flex-shrink:0;
}}

/* 하단 그라디언트 바 */
.gradient-bar {{
  width:860px; height:280px; position:relative; overflow:hidden;
  background:linear-gradient(180deg, {TEAL} 0%, #0086E0 100%);
  display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:16px;
}}
.gradient-bar-title {{
  color:{WHITE}; font-size:32px; font-weight:700;
  letter-spacing:-0.5px; word-break:keep-all; text-align:center;
}}
.gradient-bar-sub {{
  color:rgba(255,255,255,0.8); font-size:16px; font-weight:300;
  text-align:center;
}}

/* 네비 도트 */
.dots {{
  display:flex; gap:10px; justify-content:center;
  padding:24px 0 40px;
}}
.dot {{
  width:10px; height:10px; border-radius:50%;
  background:rgba(255,255,255,0.2);
}}
.dot.active {{ background:{TEAL}; }}
</style></head>
<body><div class="wrap">

  <!-- 히어로 이미지 -->
  <div class="hero-top">
    <img class="hero-bg" src="{img('runner_product')}" alt="RunVision runner">
    <div class="hero-overlay"></div>
    <div class="hero-text">
      <div class="hero-badge">RUNVISION SMARTGLASSES</div>
      <div class="hero-title">스마트 글래스로<br>달리는 방법</div>
      <div class="hero-sub">가민 워치 데이터를 — 시야 위에</div>
    </div>
  </div>

  <!-- HUD 메트릭 디스플레이 -->
  <div class="hud-zone">
    <div class="hud-label">REAL-TIME SMART DISPLAY</div>
    <div class="hud-frame">
      <div class="hud-metric">
        <div class="hud-value">11:31</div>
        <div class="hud-unit">min/km</div>
      </div>
      <div class="hud-divider"></div>
      <div class="hud-metric">
        <div class="hud-value">180</div>
        <div class="hud-unit">spm</div>
      </div>
      <div class="hud-divider"></div>
      <div class="hud-metric">
        <div class="hud-value">41.1</div>
        <div class="hud-unit">km</div>
      </div>
      <div class="hud-divider"></div>
      <div class="hud-metric">
        <div class="hud-value">120</div>
        <div class="hud-unit">bpm</div>
      </div>
    </div>
    <div class="dots">
      <div class="dot active"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>
  </div>

  <!-- 그라디언트 바 -->
  <div class="gradient-bar">
    <div class="gradient-bar-title">달리면서, 시야에서 바로 확인</div>
    <div class="gradient-bar-sub">손목을 들지 않아도 — 페이스, 심박수, 거리, 케이던스</div>
  </div>

</div></body></html>""", 860, 1120


# ─────────────────────────────────────────────────────────
# SECTION 2: 인트로(2) — Q&A 스토리텔링
# ─────────────────────────────────────────────────────────
def section_intro2():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}
<style>{RESET}
.wrap {{ background:{WHITE}; }}

/* ── 1부: 기존 가정 도전 ── */
.part1 {{ padding:80px 90px 60px; }}
.section-label {{
  color:{TEAL}; font-size:12px; font-weight:700;
  letter-spacing:3px; margin-bottom:32px;
}}
.assumption-strip {{
  background:{DARK}; border-radius:12px;
  padding:20px 32px; margin-bottom:12px;
  display:flex; align-items:center; gap:16px;
}}
.strip-num {{
  color:{TEAL}; font-size:18px; font-weight:900;
  width:28px; flex-shrink:0;
}}
.strip-text {{
  color:rgba(255,255,255,0.75); font-size:26px;
  font-weight:300; letter-spacing:-0.5px;
  text-decoration:line-through;
  text-decoration-color:rgba(0,196,196,0.6);
}}

/* ── 이미지 블록 ── */
.img-block {{
  width:860px; height:460px; position:relative; overflow:hidden;
}}
.img-block img {{
  width:100%; height:100%; object-fit:cover; object-position:center 40%;
  filter:brightness(0.8);
}}
.img-block-overlay {{
  position:absolute; inset:0;
  background:linear-gradient(to bottom, transparent 40%, rgba(10,22,40,0.7) 100%);
}}

/* ── 인용구 블록 ── */
.quote-block {{
  background:#F8F9FA; border-left:4px solid {TEAL};
  margin:0 90px; padding:48px 52px;
  position:relative;
}}
.quote-mark {{
  color:{TEAL}; font-size:80px; font-weight:900;
  line-height:0.8; position:absolute; top:28px; left:32px;
  opacity:0.4;
}}
.quote-text {{
  color:{DARK}; font-size:34px; font-weight:300;
  line-height:1.6; letter-spacing:-0.5px;
  word-break:keep-all; text-align:center;
  padding-top:20px;
}}
.quote-end {{
  text-align:right;
}}

/* ── 포인트 섹션 (TEAL 배경) ── */
.point-section {{
  background:{TEAL}; padding:64px 90px; margin-top:60px;
}}
.point-label {{
  color:{DARK}; font-size:13px; font-weight:700;
  letter-spacing:3px; margin-bottom:16px;
}}
.point-brand {{
  color:{DARK}; font-size:22px; font-weight:900;
  letter-spacing:-0.5px; margin-bottom:20px;
}}
.point-title {{
  color:{WHITE}; font-size:44px; font-weight:300;
  line-height:1.4; letter-spacing:-1px; word-break:keep-all;
  margin-bottom:8px;
}}
.point-title strong {{ font-weight:900; }}
.point-divider {{
  width:680px; height:1px; background:rgba(255,255,255,0.3);
  margin:32px 0;
}}

/* ── Q&A 섹션 ── */
.qa-block {{
  padding:80px 90px; background:{WHITE};
}}
.qa-item {{
  margin-bottom:64px;
}}
.qa-q {{
  font-size:42px; font-weight:700; color:{DARK};
  line-height:1.35; letter-spacing:-1.5px;
  word-break:keep-all; margin-bottom:24px;
}}
.qa-a {{
  font-size:28px; font-weight:300; color:#333;
  line-height:1.8; letter-spacing:-0.3px;
  word-break:keep-all; padding-left:24px;
  border-left:3px solid {TEAL};
}}

/* ── HUD 정보 원형 그래픽 ── */
.hud-circles {{
  padding:60px 90px; background:#F8FEFF;
  display:flex; flex-direction:column; align-items:center;
}}
.hud-circles-label {{
  color:{TEAL}; font-size:13px; font-weight:700;
  letter-spacing:3px; margin-bottom:32px;
}}
.circles-row {{
  display:flex; gap:20px; margin-bottom:16px;
  justify-content:center;
}}
.circle-item {{
  width:160px; height:160px; border-radius:50%;
  background:{TEAL}; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  color:{WHITE}; text-align:center;
}}
.circle-item.gray {{
  background:#E2E8F0; color:#718096;
}}
.circle-val {{
  font-size:18px; font-weight:900; line-height:1.2;
}}
.circle-unit {{
  font-size:12px; font-weight:300; margin-top:4px;
  opacity:0.8;
}}

/* ── 스마트 글래스 이유 ── */
.eyewear-reason {{
  padding:80px 90px; background:{WHITE};
  text-align:center;
}}
.er-q {{
  font-size:42px; font-weight:700; color:{DARK};
  line-height:1.35; letter-spacing:-1.5px;
  word-break:keep-all; margin-bottom:32px;
}}
.er-body {{
  font-size:28px; font-weight:300; color:#333;
  line-height:1.8; letter-spacing:-0.3px;
  word-break:keep-all; margin-bottom:16px;
}}
.er-emphasis {{
  font-size:30px; font-weight:700; color:{TEAL};
  margin-bottom:40px;
}}
</style></head>
<body><div class="wrap">

  <!-- 1부: 기존 가정 도전 -->
  <div class="part1">
    <div class="section-label">CHALLENGE</div>
    <div style="font-size:44px; font-weight:300; color:{DARK}; line-height:1.5; letter-spacing:-1px; word-break:keep-all; margin-bottom:40px;">
      우리는 그동안<br>이렇게 생각했어요.
    </div>
    <div class="assumption-strip">
      <div class="strip-num">01</div>
      <div class="strip-text">워치는 손목에 있어야 하고,</div>
    </div>
    <div class="assumption-strip">
      <div class="strip-num">02</div>
      <div class="strip-text">정보는 확인해야 하며,</div>
    </div>
    <div class="assumption-strip">
      <div class="strip-num">03</div>
      <div class="strip-text">러닝 중 불편함은 당연하다</div>
    </div>
  </div>

  <!-- 이미지 블록 -->
  <div class="img-block">
    <img src="{img('runner_wrist_asics')}" alt="손목 확인 러너">
    <div class="img-block-overlay"></div>
  </div>

  <!-- 그런데, 왜? -->
  <div class="qa-block" style="padding-bottom:40px;">
    <div class="qa-item">
      <div class="qa-q">그런데, 왜?<br>아무도 이 불.편.함을<br>바꾸지 않았을까요?</div>
    </div>
  </div>

  <!-- 인용구 -->
  <div class="quote-block">
    <div class="quote-mark">"</div>
    <div class="quote-text">
      러닝 중 정보는<br>확인하는 것이 아니라,<br>함께 달려야 한다고!
    </div>
    <div class="quote-end" style="color:{TEAL}; font-size:80px; font-weight:900; line-height:0.5;">"</div>
  </div>

  <!-- 포인트 섹션 -->
  <div class="point-section">
    <div class="point-label">RUNVISION은</div>
    <div class="point-title">러닝 중 정보를<br>'보는 방식'이 아니라<br><strong>'존재하는 위치'를 바꿉니다.</strong></div>
    <div class="point-divider"></div>
    <div style="color:{WHITE}; font-size:26px; font-weight:300; line-height:1.8; word-break:keep-all;">
      그래서 우리는 이렇게 생각했습니다.
    </div>
    <div style="color:{WHITE}; font-size:30px; font-weight:700; margin-top:16px; line-height:1.6; word-break:keep-all;">
      손목이 아닌 시야에서,<br>멈추지 않고 이어지는 러닝을 위해.
    </div>
  </div>

  <!-- Q&A 섹션 -->
  <div class="qa-block">
    <div class="qa-item">
      <div class="qa-q">Q. 달리는 중에,<br>굳이 손목을 들어야 할까요?</div>
      <div class="qa-a">
        A. 아닙니다!<br><br>
        달리는 동안 리듬을 깨지 않고,<br>
        시야를 흐트러뜨리지 않고,<br>
        내 페이스를 확인할 수 있다면?
      </div>
    </div>
    <div class="qa-item">
      <div class="qa-q">그래서 RUNVISION은<br>'확인하는 방식'을 바꿨습니다.</div>
      <div class="qa-a">
        내 눈앞, 시야 안에<br>정보를 띄우는 방식으로!!<br><br>
        달리는 중에도 내가 지금 어떻게 달리고 있는지,<br>
        눈을 떼지 않고 바로 알 수 있습니다.
      </div>
    </div>
  </div>

  <!-- HUD 정보 원형 그래픽 -->
  <div class="hud-circles">
    <div class="hud-circles-label">시야에 표시되는 정보</div>
    <div class="circles-row">
      <div class="circle-item">
        <div class="circle-val">현재<br>페이스</div>
      </div>
      <div class="circle-item">
        <div class="circle-val">심박수</div>
      </div>
      <div class="circle-item">
        <div class="circle-val">거리</div>
      </div>
    </div>
    <div class="circles-row">
      <div class="circle-item">
        <div class="circle-val">케이던스</div>
      </div>
      <div class="circle-item">
        <div class="circle-val">시간</div>
      </div>
    </div>
    <div style="margin-top:32px; color:#718096; font-size:15px; font-weight:300; text-align:center;">
      vs 기존방식 — <span style="text-decoration:line-through;">손목</span> · <span style="text-decoration:line-through;">휴대폰</span> · <span style="text-decoration:line-through;">멈춤</span>
    </div>
  </div>

  <!-- 왜 스마트 글래스인가 -->
  <div class="eyewear-reason">
    <div class="er-q">그럼 왜,<br>스마트 글래스일까요?</div>
    <div class="er-body">
      러닝 중<br>가장 안정적으로 유지되는 위치는<br>손도 고개도 아닌<br>시야이기 때문입니다.
    </div>
    <div class="er-emphasis">손은 계속 흔들리고,<br>고개는 자연스럽게 움직이지만,<br>시야는 항상 전방을 향합니다.</div>
    <div class="er-body" style="color:{TEAL}; font-weight:700;">
      RUNVISION은<br>그 가장 안정적인 위치에<br>정보를 올렸습니다.
    </div>
  </div>

</div></body></html>""", 860, 2600


# ─────────────────────────────────────────────────────────
# SECTION 3: 핵심키워드 — 달라짐의 증거
# ─────────────────────────────────────────────────────────
def section_core():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}
<style>{RESET}
.wrap {{ background:{WHITE}; }}

/* 섹션 헤더 */
.sec-header {{ padding:80px 90px 48px; }}
.sec-tag {{
  color:{TEAL}; font-size:12px; font-weight:700;
  letter-spacing:3px; margin-bottom:20px;
}}
.sec-title {{
  font-size:48px; font-weight:700; color:{DARK};
  line-height:1.3; letter-spacing:-1.5px; word-break:keep-all;
  margin-bottom:20px;
}}
.sec-body {{
  font-size:26px; font-weight:300; color:#555;
  line-height:1.8; letter-spacing:-0.3px; word-break:keep-all;
}}

/* 이미지 분할 비교 */
.split-compare {{
  display:flex; width:860px; height:500px;
}}
.split-panel {{
  flex:1; position:relative; overflow:hidden;
}}
.split-panel img {{
  width:100%; height:100%; object-fit:cover;
}}
.split-caption {{
  position:absolute; bottom:0; left:0; right:0;
  padding:28px 28px 24px;
  background:linear-gradient(to top, rgba(0,0,0,0.85) 0%, transparent 100%);
}}
.split-tag {{
  font-size:11px; font-weight:700; letter-spacing:3px; margin-bottom:8px;
}}
.before-tag {{ color:#FC8181; }}
.after-tag {{ color:{TEAL}; }}
.split-title {{
  color:{WHITE}; font-size:20px; font-weight:700;
  letter-spacing:-0.5px; line-height:1.4; word-break:keep-all;
}}
.split-sub {{
  color:rgba(255,255,255,0.6); font-size:13px; margin-top:4px;
}}
.vs-badge {{
  position:absolute; top:50%; left:50%;
  transform:translate(-50%, -50%);
  width:52px; height:52px;
  background:{TEAL}; border-radius:50%;
  border:3px solid {WHITE};
  display:flex; align-items:center; justify-content:center;
  color:{WHITE}; font-size:14px; font-weight:900;
  box-shadow:0 4px 20px rgba(0,196,196,0.5);
  z-index:10;
}}

/* 텍스트 설명 */
.core-desc {{
  padding:64px 90px;
}}
.desc-title {{
  font-size:42px; font-weight:700; color:{DARK};
  line-height:1.35; letter-spacing:-1.5px;
  word-break:keep-all; margin-bottom:28px;
}}
.desc-body {{
  font-size:26px; font-weight:300; color:#555;
  line-height:1.9; letter-spacing:-0.3px; word-break:keep-all;
}}

/* 가민 연동 섹션 */
.garmin-block {{
  background:#F0FFFE; padding:64px 90px;
  border-top:2px solid {TEAL};
}}
.garmin-title {{
  font-size:42px; font-weight:700; color:{DARK};
  line-height:1.35; letter-spacing:-1.5px;
  word-break:keep-all; margin-bottom:24px;
}}
.garmin-body {{
  font-size:26px; font-weight:300; color:#555;
  line-height:1.9; letter-spacing:-0.3px; word-break:keep-all;
  margin-bottom:32px;
}}
.garmin-img {{
  width:100%; height:300px; object-fit:cover;
  border-radius:16px; margin-top:8px;
}}

/* VS 비교 테이블 */
.compare-table {{
  display:flex; gap:20px; padding:64px 90px;
  background:{WHITE};
}}
.compare-col {{
  flex:1; border-radius:20px; padding:36px 32px;
}}
.col-before {{
  background:#F7FAFC; border:2px solid #E2E8F0;
}}
.col-after {{
  background:{DARK}; border:2px solid {TEAL};
}}
.col-head {{
  font-size:18px; font-weight:900; padding-bottom:20px;
  margin-bottom:20px; border-bottom:2px solid;
}}
.col-before .col-head {{ color:#A0AEC0; border-color:#E2E8F0; }}
.col-after .col-head  {{ color:{WHITE}; border-color:rgba(0,196,196,0.4); }}
.col-row {{
  font-size:16px; font-weight:500;
  padding:12px 0; border-bottom:1px solid rgba(0,0,0,0.06);
  display:flex; align-items:center; gap:12px;
}}
.col-after .col-row {{ border-color:rgba(255,255,255,0.08); color:rgba(255,255,255,0.9); }}
.col-before .col-row {{ color:#A0AEC0; }}
.col-row:last-child {{ border:none; }}
.x {{ color:#E53E3E; font-weight:900; }}
.ck {{ color:{TEAL}; font-weight:900; }}

/* 핵심 강조 텍스트 */
.emphasis-text {{
  padding:60px 90px; text-align:center;
}}
.emph-line {{
  font-size:28px; font-weight:300; color:{DARK};
  line-height:1.9; word-break:keep-all; margin-bottom:8px;
}}
.emph-bold {{
  font-size:36px; font-weight:900; color:{TEAL};
  margin-top:8px;
}}
</style></head>
<body><div class="wrap">

  <!-- 섹션 헤더 -->
  <div class="sec-header">
    <div class="sec-tag">CORE DIFFERENCE</div>
    <div class="sec-title">실제 러닝에서는,<br>이렇게 달라집니다</div>
    <div class="sec-body">
      RUNVISION을 착용하면<br>
      러닝 중 정보를 확인하는 방식 자체가 달라집니다.
    </div>
  </div>

  <!-- Before/After 이미지 비교 -->
  <div style="position:relative;">
    <div class="split-compare">
      <div class="split-panel">
        <img src="{img('runner_wrist_race')}" alt="Before">
        <div class="split-caption">
          <div class="split-tag before-tag">✕ BEFORE — 기존 방식</div>
          <div class="split-title">손목을 드는 순간<br>페이스가 끊긴다</div>
          <div class="split-sub">리듬이 깨지면 다시 올리기가 힘듭니다</div>
        </div>
      </div>
      <div class="split-panel">
        <img src="{img('runner_ar_race')}" alt="After">
        <div class="split-caption">
          <div class="split-tag after-tag">✓ AFTER — RunVision</div>
          <div class="split-title">시야 안에서 바로 확인<br>흐름을 유지한다</div>
          <div class="split-sub">고개를 돌리지 않아도, 멈추지 않아도</div>
        </div>
      </div>
    </div>
    <div class="vs-badge">VS</div>
  </div>

  <!-- 확인 방법 비교 -->
  <div class="compare-table">
    <div class="compare-col col-before">
      <div class="col-head">기존 방식</div>
      <div class="col-row"><span class="x">✕</span> 확인방법: 손목을 내려다봄</div>
      <div class="col-row"><span class="x">✕</span> 리듬이 끊김</div>
      <div class="col-row"><span class="x">✕</span> '확인' 중심</div>
    </div>
    <div class="compare-col col-after">
      <div class="col-head">✦ RunVision</div>
      <div class="col-row"><span class="ck">✓</span> 확인방법: 시야에서 바로 확인</div>
      <div class="col-row"><span class="ck">✓</span> 흐름 유지</div>
      <div class="col-row"><span class="ck">✓</span> '몰입' 중심</div>
    </div>
  </div>

  <!-- 설명 텍스트 -->
  <div class="core-desc">
    <div class="desc-title">가민 워치를 바꿀 필요도,<br>새로운 생태계에 적응할 필요도 없습니다.</div>
    <div class="desc-body">
      Runvision은 지금의 러닝 위에 얹어지는 시야입니다.<br><br>
      내 페이스와 컨디션을<br>자연스럽게 인지하며 달릴 수 있습니다.
    </div>
  </div>

  <!-- 가민 연동 -->
  <div class="garmin-block">
    <div class="garmin-title">러너들이 가장 많이 쓰는<br>가민 워치와 연동됩니다</div>
    <div class="garmin-body">
      Runvision은 러너들이 이미 가장 신뢰해 온<br>
      Garmin워치와 연동되는 스마트 글래스입니다.<br><br>
      새로운 데이터를 만들지 않습니다.<br>
      지금 쓰고 있는 가민의 러닝 데이터를,<br>
      그대로 '시야'로 옮겼을 뿐입니다.
    </div>
    <img class="garmin-img" src="{img('hud_closeup')}" alt="RunVision HUD">
  </div>

  <!-- 강조 텍스트 -->
  <div class="emphasis-text">
    <div class="emph-line">시선 이동 없이,</div>
    <div class="emph-line">손목을 들지 않고,</div>
    <div class="emph-line">리듬을 끊지 않은 채,</div>
    <div class="emph-bold">특히 숨이 차오르고,<br>몸이 무거워질수록,<br>이 차이는 더 크게 느껴집니다.</div>
  </div>

</div></body></html>""", 860, 2200


# ─────────────────────────────────────────────────────────
# SECTION 4: 특별성 — $100대 유일한 가민 호환 스마트 글래스
# ─────────────────────────────────────────────────────────
def section_special():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}
<style>{RESET}
.wrap {{ background:{WHITE}; }}

/* 메인 헤더 */
.spec-header {{ padding:80px 90px 48px; }}
.spec-tag {{
  color:{TEAL}; font-size:12px; font-weight:700;
  letter-spacing:3px; margin-bottom:20px;
}}
.spec-title {{
  font-size:48px; font-weight:700; color:{DARK};
  line-height:1.3; letter-spacing:-1.5px; word-break:keep-all;
  margin-bottom:24px;
}}
.spec-body {{
  font-size:26px; font-weight:300; color:#555;
  line-height:1.9; letter-spacing:-0.3px; word-break:keep-all;
}}
.spec-body strong {{
  font-weight:700; color:{DARK};
}}

/* 메인 제품 이미지 */
.main-product-img {{
  width:860px; height:400px; object-fit:cover;
  object-position:center 40%;
  display:block;
}}

/* 강조 문구 */
.highlight-text {{
  padding:64px 90px;
  text-align:center;
  background:#F8FEFF;
}}
.hl-title {{
  font-size:34px; font-weight:300; color:{DARK};
  line-height:1.6; letter-spacing:-0.5px; word-break:keep-all;
  margin-bottom:24px;
}}
.hl-title strong {{ font-weight:900; color:{TEAL}; }}
.hl-body {{
  font-size:26px; font-weight:300; color:#555;
  line-height:1.9; word-break:keep-all;
}}

/* 3개 특징 스트립 */
.feature-strips {{ padding:60px 90px; }}
.strip-title {{
  font-size:13px; font-weight:700; color:{TEAL};
  letter-spacing:3px; margin-bottom:32px; text-align:center;
}}
.feature-strip {{
  display:flex; align-items:center;
  background:{DARK}; border-radius:12px;
  padding:0; margin-bottom:12px; overflow:hidden; height:100px;
}}
.strip-img {{
  width:120px; height:100px; object-fit:cover; flex-shrink:0;
}}
.strip-content {{
  flex:1; padding:0 32px;
  display:flex; flex-direction:column; justify-content:center;
}}
.strip-feature-text {{
  color:{WHITE}; font-size:24px; font-weight:300;
  letter-spacing:-0.3px;
}}
.strip-feature-text strong {{ font-weight:700; color:{TEAL}; }}
.strip-num-badge {{
  width:40px; height:40px; background:rgba(255,255,255,0.1);
  border-radius:50%; display:flex; align-items:center; justify-content:center;
  color:{TEAL}; font-size:16px; font-weight:900; flex-shrink:0;
  margin-right:20px; margin-left:20px;
}}

/* 감성 카피 */
.emotional-copy {{
  padding:80px 90px; text-align:center; background:{WHITE};
}}
.ec-quote {{
  font-size:30px; font-weight:300; color:{DARK};
  line-height:1.8; letter-spacing:-0.5px; word-break:keep-all;
  margin-bottom:32px;
}}
.ec-quote em {{
  font-style:normal; font-weight:900;
  color:{TEAL};
}}
.ec-divider {{
  width:48px; height:3px; background:{TEAL};
  border-radius:2px; margin:0 auto 32px;
}}
.ec-body {{
  font-size:24px; font-weight:300; color:#666;
  line-height:1.9; word-break:keep-all;
}}

/* 가격 가치 제안 */
.price-value {{
  background:{DARK}; padding:64px 90px; text-align:center;
}}
.pv-label {{
  color:{TEAL}; font-size:12px; font-weight:700;
  letter-spacing:3px; margin-bottom:20px;
}}
.pv-title {{
  color:{WHITE}; font-size:44px; font-weight:900;
  line-height:1.3; letter-spacing:-1.5px; word-break:keep-all;
  margin-bottom:16px;
}}
.pv-sub {{
  color:rgba(255,255,255,0.6); font-size:20px; font-weight:300;
  line-height:1.6; word-break:keep-all; margin-bottom:40px;
}}
.pv-body {{
  color:rgba(255,255,255,0.75); font-size:22px; font-weight:300;
  line-height:1.9; word-break:keep-all;
}}
</style></head>
<body><div class="wrap">

  <!-- 메인 헤더 -->
  <div class="spec-header">
    <div class="spec-tag">UNIQUENESS</div>
    <div class="spec-title">가민 워치와 호환되는,<br>유.일.한 $100대<br>러닝 스마트 글래스</div>
    <div class="spec-body">
      많은 러너들이 선택한 가민 워치.<br>
      하지만 그 가민과 연동되는 러닝 스마트 글래스는<br>
      대부분 <strong>$300 이상입니다.</strong><br><br>
      가민 워치에서 제공하는<br>
      페이스, 거리, 시간, 심박수, 케이던스까지<br>
      러닝에 필요한 모든 정보를
    </div>
  </div>

  <!-- 핵심 카피 강조 -->
  <div class="highlight-text">
    <div class="hl-title">
      <strong>달리는 그대로,<br>시야 위에 보여줍니다.</strong>
    </div>
  </div>

  <!-- 메인 제품 이미지 -->
  <img class="main-product-img" src="{img('runner_hud_hero')}" alt="RunVision in action">

  <!-- 3개 특징 스트립 -->
  <div class="feature-strips">
    <div class="strip-title">RunVision 핵심 차별점</div>
    <div class="feature-strip">
      <div class="strip-num-badge">1</div>
      <img class="strip-img" src="{img('module_side')}" alt="">
      <div class="strip-content">
        <div class="strip-feature-text"><strong>손목을 들지 않고</strong> — 시야에서 바로</div>
      </div>
    </div>
    <div class="feature-strip">
      <div class="strip-num-badge">2</div>
      <img class="strip-img" src="{img('hud_closeup')}" alt="">
      <div class="strip-content">
        <div class="strip-feature-text"><strong>고개를 숙이지 않고</strong> — 전방 주시 유지</div>
      </div>
    </div>
    <div class="feature-strip">
      <div class="strip-num-badge">3</div>
      <img class="strip-img" src="{img('runner_hud_bpm')}" alt="">
      <div class="strip-content">
        <div class="strip-feature-text"><strong>흐름을 끊지 않은 채</strong> — 몰입 유지</div>
      </div>
    </div>
  </div>

  <!-- 감성 카피 -->
  <div class="emotional-copy">
    <div class="ec-divider"></div>
    <div class="ec-quote">
      러닝이 가장 힘들어지는 순간,<br>
      이미 숨은 차오르고<br>
      팔을 들 힘조차 없을 때,<br><br>
      그때 필요한 건<br>
      <em>"한 번 더 확인"이 아니라<br>놓치지 않는 흐름입니다.</em>
    </div>
    <div class="ec-body">
      Runvision은 그 순간을 위해 만들어졌습니다.
    </div>
  </div>

  <!-- 가격 가치 제안 -->
  <div class="price-value">
    <div class="pv-label">VALUE PROPOSITION</div>
    <div class="pv-title">가민은 러닝을 '기록'이 아니라<br>훈련으로 보는 러너들이 선택합니다.</div>
    <div class="pv-sub">그래서 많은 러너들이 궁금해합니다.<br>"이 정도 경험이면, 과연 얼마일까?"</div>
    <div class="pv-body">
      이제, Runvision이 러닝을 어떻게 바꾸는지<br>하나씩 살펴볼 차례입니다.
    </div>
  </div>

</div></body></html>""", 860, 2000


# ─────────────────────────────────────────────────────────
# SECTION 5: 사용법 — 단 3단계 + Before/After
# ─────────────────────────────────────────────────────────
def section_usage():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}
<style>{RESET}
.wrap {{ background:{WHITE}; }}

/* 헤더 */
.usage-header {{ padding:80px 90px 60px; }}
.usage-tag {{
  color:{TEAL}; font-size:12px; font-weight:700;
  letter-spacing:3px; margin-bottom:20px;
}}
.usage-title {{
  font-size:48px; font-weight:700; color:{DARK};
  line-height:1.3; letter-spacing:-1.5px; word-break:keep-all;
  margin-bottom:24px;
}}
.usage-body {{
  font-size:26px; font-weight:300; color:#555;
  line-height:1.9; letter-spacing:-0.3px; word-break:keep-all;
}}

/* 착용 방법 */
.how-label {{
  font-size:28px; font-weight:700; color:{DARK};
  text-align:center; margin-bottom:8px;
}}

/* 3단계 */
.steps-section {{
  padding:40px 60px 60px;
}}
.steps-subtitle {{
  font-size:22px; font-weight:700; color:{DARK};
  text-align:center; margin-bottom:32px;
}}
/* Step 1 — 풀 와이드 카드 */
.step1-card {{
  border-radius:16px; overflow:hidden;
  box-shadow:0 4px 20px rgba(0,0,0,0.08);
  margin-bottom:20px;
}}
.step1-images {{
  display:flex; height:200px; background:#F7F7F7;
}}
.step1-images img {{
  flex:1; object-fit:contain; padding:20px;
}}
.step1-images img:first-child {{
  border-right:1px solid #E0E0E0;
}}
.step1-body {{
  padding:16px 28px; background:{WHITE};
  display:flex; align-items:center; gap:16px;
}}
/* 아래 화살표 */
.step-down-arrow {{
  text-align:center; color:{TEAL};
  font-size:26px; font-weight:900; margin-bottom:16px;
}}
/* Step 2, 3 — 2열 */
.steps-row {{
  display:flex; gap:20px; align-items:stretch;
}}
.step-card {{
  flex:1; border-radius:16px; overflow:hidden;
  box-shadow:0 4px 20px rgba(0,0,0,0.08);
  display:flex; flex-direction:column;
}}
.step-img {{
  width:100%; height:220px;
  object-fit:contain; background:#F5F5F5;
}}
.step-body {{
  padding:20px; background:{WHITE}; flex:1;
  display:flex; flex-direction:column; align-items:center;
}}
.step-num {{
  width:44px; height:44px; background:{TEAL};
  border-radius:50%; color:{WHITE}; font-size:20px; font-weight:900;
  display:flex; align-items:center; justify-content:center;
  flex-shrink:0;
}}
.step-text {{
  font-size:18px; font-weight:700; color:{DARK};
  text-align:center; letter-spacing:-0.3px; margin-top:12px;
}}
.step-arrow {{
  color:{TEAL}; font-size:28px; font-weight:900;
  flex-shrink:0; align-self:center; padding:0 8px;
}}

/* 연결 설명 */
.connect-desc {{
  padding:0 90px 60px;
  font-size:24px; font-weight:300; color:#555;
  line-height:1.9; word-break:keep-all;
  text-align:center;
}}

/* ── HOW TO WEAR (통합) ──────────────────────────── */
.mount-header {{
  padding:56px 60px 44px; text-align:center;
}}
.mount-tag {{
  display:inline-block; background:{TEAL}; color:{WHITE};
  font-size:11px; font-weight:700; letter-spacing:3px;
  padding:6px 18px; border-radius:30px; margin-bottom:24px;
}}
.mount-title {{
  font-size:38px; font-weight:900; color:{DARK};
  line-height:1.25; letter-spacing:-2px; word-break:keep-all;
  margin-bottom:16px;
}}
.mount-sub {{
  font-size:17px; font-weight:300; color:#666;
  letter-spacing:-0.3px;
}}
.mount-grid {{
  display:flex; gap:0; padding:0 40px 52px; align-items:stretch;
}}
.mount-card {{
  flex:1; background:#F8FAFB;
  border:2px solid #E8EEF2; border-radius:20px;
  margin:0 10px; overflow:hidden;
  display:flex; flex-direction:column;
}}
.mount-card:last-child {{
  background:{DARK}; border-color:{TEAL};
}}
.card-header {{
  padding:28px 32px 20px;
  display:flex; flex-direction:column; align-items:center;
}}
.card-badge {{
  font-size:11px; font-weight:700; letter-spacing:2px;
  padding:5px 16px; border-radius:20px;
  margin-bottom:20px;
}}
.mount-card:first-child .card-badge {{
  background:rgba(0,196,196,0.12); color:{TEAL};
}}
.mount-card:last-child .card-badge {{
  background:{TEAL}; color:{DARK};
}}
.card-img-wrap {{
  width:200px; height:200px; display:flex;
  align-items:center; justify-content:center;
  margin-bottom:16px;
}}
.card-img-wrap img {{
  max-width:100%; max-height:100%;
  object-fit:contain;
}}
.card-photo {{
  width:100%; height:260px; overflow:hidden;
}}
.card-photo img {{
  width:100%; height:100%;
  object-fit:cover; object-position:center 20%;
}}
.card-body {{
  padding:24px 32px 28px;
  display:flex; flex-direction:column; align-items:center;
  flex:1;
}}
.card-type {{
  font-size:13px; font-weight:700; letter-spacing:2px;
  color:{TEAL}; margin-bottom:10px;
}}
.card-title {{
  font-size:20px; font-weight:900; color:{DARK};
  margin-bottom:10px; text-align:center; word-break:keep-all;
}}
.mount-card:last-child .card-title {{
  color:{WHITE};
}}
.card-desc {{
  font-size:15px; font-weight:300; color:#666;
  line-height:1.8; text-align:center; word-break:keep-all;
  margin-bottom:16px;
}}
.mount-card:last-child .card-desc {{
  color:rgba(255,255,255,0.65);
}}
.card-tag {{
  font-size:13px; font-weight:700;
  padding:7px 18px; border-radius:30px;
  margin-top:auto;
}}
.mount-card:first-child .card-tag {{
  background:rgba(0,196,196,0.1); color:{TEAL};
  border:1px solid rgba(0,196,196,0.3);
}}
.mount-card:last-child .card-tag {{
  background:rgba(0,196,196,0.2); color:{TEAL};
  border:1px solid rgba(0,196,196,0.4);
}}
.mount-footer {{
  background:#F0FAFA;
  border-top:3px solid {TEAL};
  padding:40px 60px; text-align:center;
}}
.mount-footer-text {{
  font-size:19px; font-weight:300; color:{DARK};
  line-height:2; letter-spacing:-0.3px; word-break:keep-all;
}}
.mount-footer-text strong {{
  font-weight:900; color:{TEAL};
}}

</style></head>
<body><div class="wrap">

  <!-- 헤더 -->
  <div class="usage-header">
    <div class="usage-tag">HOW TO USE</div>
    <div class="usage-title">러닝 중엔,<br>생각할 여유가 없습니다.<br>그래서 Runvision은<br>'어떻게 쓰느냐'부터<br>단순하게 만들었습니다.</div>
  </div>

  <!-- 착용 방법 -->
  <div style="padding:0 90px 20px; text-align:center;">
    <div class="how-label">어떻게 착용하나요?<br>모자 또는 고글에 붙이면, 준비 끝!</div>
  </div>

  <!-- 3단계 -->
  <div class="steps-section">
    <div class="steps-subtitle">단 3단계로 바로 러닝</div>

    <!-- Step 1: 풀 와이드 -->
    <div class="step1-card">
      <div class="step1-images">
        <img src="{img('mount_sketch_glasses')}" alt="고글 장착">
        <img src="{img('mount_sketch_cap')}" alt="모자 장착">
      </div>
      <div class="step1-body">
        <div class="step-num">1</div>
        <div class="step-text">고글 및 모자에 부착</div>
      </div>
    </div>

    <!-- 아래 방향 화살표 -->
    <div class="step-down-arrow">↓</div>

    <!-- Step 2, 3: 2열 -->
    <div class="steps-row">
      <div class="step-card">
        <img class="step-img" src="{img('garmin_watch')}" alt="Step 2">
        <div class="step-body">
          <div class="step-num">2</div>
          <div class="step-text">가민 워치 연동</div>
        </div>
      </div>
      <div class="step-arrow">→</div>
      <div class="step-card">
        <img class="step-img" src="{img('glasses_lifestyle')}" alt="Step 3">
        <div class="step-body">
          <div class="step-num">3</div>
          <div class="step-text">러닝 시작</div>
        </div>
      </div>
    </div>
  </div>

  <!-- 연결 설명 -->
  <div class="connect-desc">
    Runvision은 별도의 복잡한 설정 없이<br>
    러너의 모자 및 고글에 부착하는 방식으로 사용합니다.<br><br>
    장착하고, 이미 사용 중인 가민 워치와 연결하면<br>
    러닝 준비는 이미 끝났습니다.
  </div>

</div></body></html>""", 860, 1400


# ─────────────────────────────────────────────────────────
# SECTION 6: 메이커소개 + 리워드
# ─────────────────────────────────────────────────────────
def section_maker():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}
<style>{RESET}
.wrap {{ background:{WHITE}; }}

/* 메이커 소개 */
.maker-header {{ padding:80px 90px 48px; }}
.maker-tag {{
  color:{TEAL}; font-size:12px; font-weight:700;
  letter-spacing:3px; margin-bottom:20px;
}}
.maker-title {{
  font-size:52px; font-weight:700; color:{DARK};
  line-height:1.2; letter-spacing:-1.5px; margin-bottom:32px;
}}

/* 메이커 프로필 */
.maker-profile {{
  display:flex; align-items:center; gap:40px;
  margin-bottom:40px;
}}
.maker-img-wrap {{
  width:180px; height:180px; border-radius:50%;
  overflow:hidden; border:4px solid {TEAL};
  flex-shrink:0; background:#EEF2F7;
  display:flex; align-items:center; justify-content:center;
}}
.maker-img {{
  width:100%; height:100%; object-fit:cover; object-position:center;
}}
.maker-info {{ flex:1; }}
.maker-name {{
  font-size:28px; font-weight:900; color:{DARK};
  letter-spacing:-0.5px; margin-bottom:6px;
}}
.maker-role {{
  font-size:18px; font-weight:700; color:{TEAL}; margin-bottom:16px;
}}
.maker-desc {{
  font-size:22px; font-weight:300; color:#555;
  line-height:1.9; letter-spacing:-0.3px; word-break:keep-all;
}}

/* 메이커 이미지 */
.maker-banner {{
  width:860px; height:712px; object-fit:cover;
  object-position:center; display:block;
}}

/* 리워드 섹션 */
.reward-section {{
  padding:80px 90px;
}}
.reward-title {{
  font-size:42px; font-weight:700; color:{DARK};
  line-height:1.3; letter-spacing:-1.5px; word-break:keep-all;
  margin-bottom:40px;
}}
.reward-card {{
  border:2px solid #E2E8F0; border-radius:16px;
  overflow:hidden; margin-bottom:20px;
}}
.reward-card-header {{
  background:{DARK}; padding:20px 28px;
  display:flex; align-items:center; justify-content:space-between;
}}
.reward-card-name {{
  color:{WHITE}; font-size:20px; font-weight:700;
  letter-spacing:-0.3px;
}}
.reward-card-badge {{
  background:{TEAL}; color:{DARK}; font-size:13px;
  font-weight:700; padding:6px 16px; border-radius:20px;
  letter-spacing:0.5px;
}}
.reward-card-body {{
  padding:24px 28px; background:{WHITE};
}}
.reward-item {{
  display:flex; align-items:center; gap:12px;
  font-size:18px; font-weight:400; color:#444;
  padding:10px 0; border-bottom:1px solid #F0F0F0;
}}
.reward-item:last-child {{ border:none; }}
.reward-ck {{ color:{TEAL}; font-weight:900; font-size:16px; }}
.reward-price {{
  font-size:26px; font-weight:900; color:{TEAL};
  text-align:right; padding-top:16px;
}}
.reward-orig {{
  font-size:18px; color:#A0AEC0;
  text-decoration:line-through; margin-right:12px;
}}
</style></head>
<body><div class="wrap">

  <!-- 메이커 소개 -->
  <div class="maker-header">
    <div class="maker-tag">ABOUT MAKER</div>
    <div class="maker-title">메이커소개</div>
    <div class="maker-profile">
      <div class="maker-img-wrap">
        <img class="maker-img" src="{img('module_standalone')}" alt="RunVision">
      </div>
      <div class="maker-info">
        <div class="maker-name">RunVision Labs</div>
        <div class="maker-role">러너를 위해, 러너가 만든 제품</div>
        <div class="maker-desc">
          실제 마라톤 러너가 만든 프로젝트입니다.<br>
          Garmin 워치 연동 앱과 스마트글래스를 직접 개발하며<br>
          수백 시간의 테스트를 거쳤습니다.
        </div>
      </div>
    </div>
  </div>

  <!-- 메이커 배너 이미지 -->
  <img class="maker-banner" src="{img('runner_closeup')}" alt="RunVision maker">

  <!-- 리워드 구성 안내 -->
  <div class="reward-section">
    <div class="reward-title">리워드 구성 안내</div>

    <div class="reward-card">
      <div class="reward-card-header">
        <div class="reward-card-name">🥇 얼리버드 Special</div>
        <div class="reward-card-badge">한정 100명</div>
      </div>
      <div class="reward-card-body">
        <div class="reward-item"><span class="reward-ck">✓</span> RunVision 스마트글래스 본체</div>
        <div class="reward-item"><span class="reward-ck">✓</span> 충전 케이스</div>
        <div class="reward-item"><span class="reward-ck">✓</span> Garmin 앱 평생 무료 이용권</div>
        <div class="reward-item"><span class="reward-ck">✓</span> Galaxy Watch 앱 평생 무료 이용권</div>
        <div class="reward-price">
          <span class="reward-orig">299,000원</span>
          <span>199,000원</span>
        </div>
      </div>
    </div>

    <div class="reward-card">
      <div class="reward-card-header">
        <div class="reward-card-name">🥈 일반 후원</div>
        <div class="reward-card-badge">Standard</div>
      </div>
      <div class="reward-card-body">
        <div class="reward-item"><span class="reward-ck">✓</span> RunVision 스마트글래스 본체</div>
        <div class="reward-item"><span class="reward-ck">✓</span> 충전 케이스</div>
        <div class="reward-item"><span class="reward-ck">✓</span> Garmin 앱 1년 이용권</div>
        <div class="reward-price">
          <span class="reward-orig">299,000원</span>
          <span>249,000원</span>
        </div>
      </div>
    </div>

  </div>

</div></body></html>""", 860, 1400


# ─────────────────────────────────────────────────────────
# SECTION 7: FAQ
# ─────────────────────────────────────────────────────────
def section_faq():
    faqs = [
        ("어떤 가민 워치와 호환되나요?",
         "Forerunner, Fenix, Epix, Enduro 시리즈 등 BLE 지원 가민 워치 대부분과 호환됩니다. Connect IQ 스토어에서 RunVision IQ 앱을 설치하시면 됩니다."),
        ("갤럭시 워치도 사용할 수 있나요?",
         "네, 갤럭시 워치도 지원합니다. Galaxy Watch 전용 앱을 설치하면 가민 워치와 동일하게 페이스, 심박수, 케이던스 등 러닝 데이터를 스마트렌즈로 확인할 수 있습니다."),
        ("배터리는 얼마나 가나요?",
         "연속 사용 기준 80분 사용 가능합니다. 화면 꺼짐/켜짐 시간을 조합하면 더 오래 사용할 수 있습니다. 충전 케이스로 8번 충전 가능합니다."),
        ("방수가 되나요?",
         "IPX4 등급 방수로 땀과 소나기 정도의 빗물은 문제없습니다. 수영이나 물에 완전히 잠기는 환경은 피해주세요."),
        ("안경을 착용하지 않아도 사용할 수 있나요?",
         "네, 가능합니다. 러닝 고글이나 선글라스에 부착하거나, 러닝 캡 챙에 클립으로 장착하는 방식도 지원합니다."),
        ("어떤 러닝 고글/안경에 장착 가능한가요?",
         "대부분의 표준 프레임 러닝 고글에 장착 가능합니다. 프레임 두께 2~8mm 범위의 안경에 호환되며, 상세 호환 목록은 출시 시 안내드립니다."),
        ("앱 설치가 필요한가요?",
         "Garmin 워치에 Connect IQ 앱(RunVision IQ)을 설치해야 합니다. 스마트폰 앱은 초기 설정 시에만 필요하며 러닝 중에는 불필요합니다."),
        ("배송은 언제 예정인가요?",
         "와디즈 펀딩 종료 후 3개월 내 순차 발송 예정입니다. 정확한 일정은 펀딩 달성 후 안내드립니다."),
        ("환불이 가능한가요?",
         "와디즈 펀딩 특성상 취소는 목표금액 미달성 시 자동 환불됩니다. 제품 수령 후 불만족 시 메이커에게 직접 문의해 주시면 성실히 대응하겠습니다."),
        ("디스플레이가 햇빛 아래에서도 잘 보이나요?",
         "마이크로 OLED 패널을 사용하여 밝은 환경에서도 가시성이 좋습니다. 밝기 자동 조절 기능이 내장되어 있습니다."),
        ("무게가 무거운가요?",
         "모듈 자체 무게는 약 18g으로 매우 가볍습니다. 장시간 착용해도 불편함이 없도록 설계되었습니다."),
        ("기기의 동작을 커스터마이징 할 수 있나요?",
         "Google Store에서 runvision 앱을 다운받아서 밝기, 화면 꺼짐/켜짐 시간 등을 설정할 수 있습니다."),
        ("A/S는 어떻게 받나요?",
         "카카오톡 채널(runvision 검색)로 문의주시면 빠르게 대응해 드립니다. 제조 결함의 경우 1년 무상 A/S를 제공합니다."),
    ]

    faq_items = ""
    for i, (q, a) in enumerate(faqs):
        faq_items += f"""
        <div class="faq-item">
          <div class="faq-q">Q. {q}</div>
          <div class="faq-a">{a}</div>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}
<style>{RESET}
.wrap {{ background:{WHITE}; }}

/* 헤더 */
.faq-header {{ padding:80px 90px 60px; }}
.faq-tag {{
  color:{TEAL}; font-size:12px; font-weight:700;
  letter-spacing:3px; margin-bottom:16px;
}}
.faq-title {{
  font-size:52px; font-weight:700; color:{DARK};
  line-height:1.2; letter-spacing:-1.5px;
}}
.faq-subtitle {{
  font-size:24px; font-weight:300; color:#888;
  margin-top:8px;
}}

/* FAQ 목록 */
.faq-list {{ padding:0 60px 80px; }}
.faq-item {{
  border-bottom:1px solid #E2E8F0; padding:36px 24px;
}}
.faq-item:first-child {{ border-top:1px solid #E2E8F0; }}
.faq-q {{
  font-size:20px; font-weight:700; color:{DARK};
  letter-spacing:-0.3px; line-height:1.5;
  margin-bottom:16px; word-break:keep-all;
}}
.faq-a {{
  font-size:18px; font-weight:300; color:#555;
  line-height:1.9; letter-spacing:-0.2px; word-break:keep-all;
  padding-left:20px; border-left:2px solid {TEAL};
}}

/* 문의 CTA */
.faq-cta {{
  padding:60px 90px 80px; text-align:center;
  background:#F8FEFF;
}}
.faq-cta-title {{
  font-size:28px; font-weight:700; color:{DARK};
  margin-bottom:16px;
}}
.faq-cta-email {{
  font-size:22px; font-weight:700; color:{TEAL};
}}
</style></head>
<body><div class="wrap">

  <div class="faq-header">
    <div class="faq-tag">FAQ</div>
    <div class="faq-title">자주묻는질문</div>
    <div class="faq-subtitle">궁금한 점이 있으시면 언제든지 문의해 주세요</div>
  </div>

  <div class="faq-list">
    {faq_items}
  </div>

  <div class="faq-cta">
    <div class="faq-cta-title">더 궁금한 점이 있으신가요?</div>
    <div class="faq-cta-email">💬 카카오톡 상담: <span style="text-decoration:none;">http://pf.kakao.com/_SMxnzX</span></div>
    <div style="font-size:15px; color:#888; margin-top:8px;">카카오톡 오픈채널에서 <strong>runvision</strong> 으로 검색하세요.</div>
  </div>

</div></body></html>""", 860, 1800


# ─────────────────────────────────────────────────────────
# 스크린샷 공통 함수
# ─────────────────────────────────────────────────────────
def screenshot_html(html: str, output_path: str, width: int, height: int):
    tmp = f"/tmp/figma_section_{os.path.basename(output_path)}.html"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
                  "--allow-file-access-from-files", "--disable-web-security"]
        )
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
        page.goto(f"file://{tmp}")
        page.wait_for_timeout(3000)
        actual_height = page.evaluate("document.body.scrollHeight")
        page.set_viewport_size({"width": width, "height": actual_height})
        page.wait_for_timeout(500)
        page.screenshot(path=output_path, full_page=True)
        browser.close()
    os.remove(tmp)
    size = os.path.getsize(output_path)
    print(f"  ✓ {output_path} ({size:,} bytes)")
    return output_path


# ─────────────────────────────────────────────────────────
# SECTION 5b: 착용 방식 — 고글 & 모자 두 가지 마운팅
# ─────────────────────────────────────────────────────────
def section_mount():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}
<style>{RESET}
.wrap {{ background:{WHITE}; }}

/* 섹션 헤더 */
.mount-header {{
  padding:72px 60px 52px; text-align:center;
}}
.mount-tag {{
  display:inline-block; background:{TEAL}; color:{WHITE};
  font-size:11px; font-weight:700; letter-spacing:3px;
  padding:6px 18px; border-radius:30px; margin-bottom:24px;
}}
.mount-title {{
  font-size:42px; font-weight:900; color:{DARK};
  line-height:1.25; letter-spacing:-2px; word-break:keep-all;
  margin-bottom:16px;
}}
.mount-sub {{
  font-size:18px; font-weight:300; color:#666;
  letter-spacing:-0.3px;
}}

/* 카드 그리드 */
.mount-grid {{
  display:flex; gap:0; padding:0 40px 60px; align-items:stretch;
}}
.mount-card {{
  flex:1; background:#F8FAFB;
  border:2px solid #E8EEF2; border-radius:20px;
  margin:0 10px; overflow:hidden;
  display:flex; flex-direction:column;
}}
.mount-card:last-child {{
  background:{DARK}; border-color:{TEAL};
}}

/* 카드 헤더 (배지 + 텍스트) */
.card-header {{
  padding:32px 32px 24px;
  display:flex; flex-direction:column; align-items:center;
}}
.card-badge {{
  font-size:11px; font-weight:700; letter-spacing:2px;
  padding:5px 16px; border-radius:20px;
  margin-bottom:20px;
}}
.mount-card:first-child .card-badge {{
  background:rgba(0,196,196,0.12); color:{TEAL};
}}
.mount-card:last-child .card-badge {{
  background:{TEAL}; color:{DARK};
}}

/* 카드 1 이미지 (기존 작은 square) */
.card-img-wrap {{
  width:220px; height:220px; display:flex;
  align-items:center; justify-content:center;
  margin-bottom:20px;
}}
.card-img-wrap img {{
  max-width:100%; max-height:100%;
  object-fit:contain;
}}

/* 카드 2 라이프스타일 사진 (풀 와이드) */
.card-photo {{
  width:100%; height:280px; overflow:hidden;
  margin-bottom:0;
}}
.card-photo img {{
  width:100%; height:100%;
  object-fit:cover; object-position:center 20%;
}}

/* 카드 하단 텍스트 */
.card-body {{
  padding:28px 32px 32px;
  display:flex; flex-direction:column; align-items:center;
  flex:1;
}}
.card-type {{
  font-size:13px; font-weight:700; letter-spacing:2px;
  color:{TEAL}; margin-bottom:10px;
}}
.card-title {{
  font-size:22px; font-weight:900; color:{DARK};
  margin-bottom:12px; text-align:center; word-break:keep-all;
}}
.mount-card:last-child .card-title {{
  color:{WHITE};
}}
.card-desc {{
  font-size:16px; font-weight:300; color:#666;
  line-height:1.8; text-align:center; word-break:keep-all;
  margin-bottom:20px;
}}
.mount-card:last-child .card-desc {{
  color:rgba(255,255,255,0.65);
}}
.card-tag {{
  font-size:14px; font-weight:700;
  padding:8px 20px; border-radius:30px;
  margin-top:auto;
}}
.mount-card:first-child .card-tag {{
  background:rgba(0,196,196,0.1); color:{TEAL};
  border:1px solid rgba(0,196,196,0.3);
}}
.mount-card:last-child .card-tag {{
  background:rgba(0,196,196,0.2); color:{TEAL};
  border:1px solid rgba(0,196,196,0.4);
}}

/* 하단 메시지 */
.mount-footer {{
  background:#F0FAFA;
  border-top:3px solid {TEAL};
  padding:44px 60px; text-align:center;
}}
.mount-footer-text {{
  font-size:20px; font-weight:300; color:{DARK};
  line-height:2; letter-spacing:-0.3px; word-break:keep-all;
}}
.mount-footer-text strong {{
  font-weight:900; color:{TEAL};
}}
</style></head>
<body><div class="wrap">

  <!-- 헤더 -->
  <div class="mount-header">
    <div class="mount-tag">HOW TO WEAR</div>
    <div class="mount-title">어떤 러너든,<br>바로 사용할 수 있습니다</div>
    <div class="mount-sub">고글 착용자도, 모자만 쓰는 러너도 — 두 가지 착용 방식 지원</div>
  </div>

  <!-- 카드 2개 -->
  <div class="mount-grid">

    <div class="mount-card">
      <div class="card-header">
        <div class="card-badge">방식 1</div>
        <div class="card-img-wrap">
          <img src="{img('glasses_glow')}" alt="고글 장착">
        </div>
      </div>
      <div class="card-body">
        <div class="card-type">GLASSES MOUNT</div>
        <div class="card-title">러닝 고글 / 선글라스</div>
        <div class="card-desc">
          기존 러닝 글래스 코다리에<br>
          클립 방식으로 간단히 장착.<br>
          대부분의 러닝 안경과 호환됩니다.
        </div>
        <div class="card-tag">✓ 대부분의 러닝 글래스 호환</div>
      </div>
    </div>

    <div class="mount-card">
      <div class="card-header">
        <div class="card-badge">방식 2</div>
      </div>
      <div class="card-photo">
        <img src="{img('cap_lifestyle')}" alt="모자 착용 라이프스타일">
      </div>
      <div class="card-body">
        <div class="card-type">CAP MOUNT</div>
        <div class="card-title">러닝캡 / 모자</div>
        <div class="card-desc">
          글래스 없이도 OK.<br>
          모자 차양에 직접 장착하여<br>
          동일한 스마트렌즈를 경험합니다.
        </div>
        <div class="card-tag">✓ 안경 없어도 사용 가능</div>
      </div>
    </div>

  </div>

  <!-- 하단 강조 -->
  <div class="mount-footer">
    <div class="mount-footer-text">
      평소 고글 없이 모자만 쓰고 달리시나요?<br>
      <strong>그래도 RunVision을 사용할 수 있습니다.</strong>
    </div>
  </div>

</div></body></html>""", 860, 1100


# ─────────────────────────────────────────────────────────
# SECTION 5c: 사용 전과 후 (Before/After)
# ─────────────────────────────────────────────────────────
def section_ba():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}
<style>{RESET}
.wrap {{ background:{WHITE}; }}

/* Before / After 비교 */
.ba-section {{ padding:0 0 0; }}
.ba-header {{
  padding:60px 90px 32px;
  font-size:42px; font-weight:700; color:{DARK};
  line-height:1.35; letter-spacing:-1.5px; word-break:keep-all;
}}
.ba-compare {{
  display:flex; width:860px;
}}
.ba-panel {{
  flex:1; position:relative;
}}
.ba-panel img {{
  width:100%; height:440px; object-fit:cover; display:block;
}}
.ba-overlay {{
  position:absolute; bottom:0; left:0; right:0;
  padding:32px 24px 28px;
  background:linear-gradient(to top, rgba(0,0,0,0.88) 0%, transparent 100%);
}}
.ba-tag {{
  font-size:11px; font-weight:700; letter-spacing:3px; margin-bottom:8px;
}}
.ba-before-tag {{ color:#FC8181; }}
.ba-after-tag {{ color:{TEAL}; }}
.ba-title {{
  color:{WHITE}; font-size:20px; font-weight:700;
  letter-spacing:-0.5px; line-height:1.45; word-break:keep-all;
}}
.ba-desc-col {{
  flex:1; padding:36px 28px;
  display:flex; flex-direction:column; justify-content:center;
}}
.ba-desc-col.before-col {{ background:#F7FAFC; }}
.ba-desc-col.after-col {{ background:#F0FFFE; }}
.ba-desc-text {{
  font-size:22px; font-weight:300; color:#555;
  line-height:1.9; letter-spacing:-0.3px; word-break:keep-all;
  text-align:center;
}}
.ba-desc-text strong {{ font-weight:700; color:{DARK}; }}
.ba-desc-text.after-text strong {{ color:{TEAL}; }}
.ba-vs-badge {{
  position:absolute; top:50%; left:50%;
  transform:translate(-50%, -50%);
  width:48px; height:48px; border-radius:50%;
  background:{TEAL}; border:3px solid {WHITE};
  display:flex; align-items:center; justify-content:center;
  color:{WHITE}; font-size:13px; font-weight:900;
  z-index:10; box-shadow:0 4px 16px rgba(0,0,0,0.3);
}}
</style></head>
<body><div class="wrap">

  <div class="ba-section">
    <div class="ba-header">
      Runvision 사용 전과 후,<br>러닝은 이렇게 달라집니다
    </div>
    <div style="position:relative;">
      <div class="ba-compare">
        <div class="ba-panel">
          <img src="{img('runner_wrist_race')}" alt="사용 전">
          <div class="ba-overlay">
            <div class="ba-tag ba-before-tag">사용 전</div>
            <div class="ba-title">페이스를 확인하는 순간,<br>자세가 흐트러지고 리듬이 끊겼습니다.</div>
          </div>
        </div>
        <div class="ba-panel">
          <img src="{img('runner_ar_race')}" alt="사용 후">
          <div class="ba-overlay">
            <div class="ba-tag ba-after-tag">사용 후</div>
            <div class="ba-title">손목을 들 필요도,<br>호흡을 깨트릴 필요도 없습니다.</div>
          </div>
        </div>
      </div>
      <div class="ba-vs-badge">VS</div>
    </div>
    <div class="ba-compare">
      <div class="ba-desc-col before-col">
        <div class="ba-desc-text">
          달릴수록 숨이 가빠질 때,<br>
          <strong>손목을 드는 것조차<br>부담이 되던 순간들.</strong><br><br>
          러닝에 집중하기보다<br>계속 '확인해야 했던' 러닝이었습니다.
        </div>
      </div>
      <div class="ba-desc-col after-col">
        <div class="ba-desc-text after-text">
          달리는 흐름은 그대로,<br>
          <strong>집중력은 더 깊게.</strong><br><br>
          러닝에 필요한 정보는 보되,<br>러닝은 방해하지 않는 것.<br>
          <strong>Runvision이 만든 변화입니다.</strong>
        </div>
      </div>
    </div>
  </div>

</div></body></html>""", 860, 900


# ─────────────────────────────────────────────────────────
# SECTION 5d: 실제 사용자 후기 (REAL USER REVIEW)
# ─────────────────────────────────────────────────────────
def section_review():
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{FONTS}
<style>{RESET}
.wrap {{ background:{WHITE}; }}

/* 베타 테스터 후기 */
.review-section {{
  padding:64px 90px; background:#F8FEFF;
}}
.review-label {{
  color:{TEAL}; font-size:12px; font-weight:700;
  letter-spacing:3px; margin-bottom:32px;
}}
.review-card {{
  background:{WHITE}; border-radius:20px;
  padding:40px 44px; border-left:4px solid {TEAL};
  box-shadow:0 4px 24px rgba(0,0,0,0.06);
}}
.review-text {{
  font-size:22px; font-weight:300; color:{DARK};
  line-height:1.9; letter-spacing:-0.3px; word-break:keep-all;
  margin-bottom:24px;
}}
.review-name {{
  font-size:16px; font-weight:700; color:{TEAL};
}}
.review-quotes {{
  display:flex; gap:16px; margin-top:24px;
}}
.review-mini-quote {{
  flex:1; background:#F8F9FA; border-radius:12px;
  padding:20px 24px;
  font-size:18px; font-weight:300; color:#555;
  line-height:1.7; letter-spacing:-0.3px;
  word-break:keep-all;
}}
</style></head>
<body><div class="wrap">

  <div class="review-section">
    <div class="review-label">REAL USER REVIEW</div>
    <div style="padding:20px 90px 40px; text-align:center;">
      <div style="font-size:32px; font-weight:700; color:{DARK}; line-height:1.4; letter-spacing:-1px; word-break:keep-all;">
        그래서 우리는,<br>실제 러너들에게 먼저<br>달려보게 했습니다.
      </div>
    </div>
    <div class="review-card">
      <div class="review-text">
        러닝 5년차 러너입니다. 가민워치로 갈아탄지 2년차인데,<br>
        사용하다보니 페이스 확인을 할때마다 조금씩 페이스가 주춤하는게 느껴지더라구요.<br><br>
        런비전은 그냥 내 시야위에 그대로 제 정보를 띄워주니<br>
        이거 참 <strong style="color:{TEAL};">속이 시원합니다!!</strong><br><br>
        왜 이런 생각을 그동안 못했을까요?
      </div>
      <div class="review-name">— 러너 김@영님</div>
    </div>
    <div class="review-quotes">
      <div class="review-mini-quote">처음엔 신기했는데, 한 번 써보니 다시 손목 보는 게 불편해졌어요.</div>
      <div class="review-mini-quote">훈련 중 리듬이 끊기지 않으니까, 러닝에 더 집중하게 돼요.</div>
      <div class="review-mini-quote">페이스 확인하려고 손목을 들 필요가 없어요. 그냥 달리기만 하면 됩니다.</div>
    </div>
  </div>

</div></body></html>""", 860, 720


SECTION_LIST = [
    ("01_figma_intro1",   section_intro1),
    ("02_figma_intro2",   section_intro2),
    ("03_figma_core",     section_core),
    ("04_figma_special",  section_special),
    ("05_figma_usage",    section_usage),
    ("05c_figma_ba",      section_ba),
    ("05d_figma_review",  section_review),
    ("06_figma_maker",    section_maker),
    ("07_figma_faq",      section_faq),
]


def generate_all(output_dir: str) -> list:
    os.makedirs(output_dir, exist_ok=True)
    results = []
    for key, fn in SECTION_LIST:
        result = fn()
        if result is None:
            continue
        html, w, h = result
        out = os.path.join(output_dir, f"{key}.png")
        print(f"\n[{key}] generating ({w}x~{h}px)...")
        screenshot_html(html, out, w, h)
        results.append(out)
    return results


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    out_dir = "output/runvision-wadiz/figma-sections"
    results = generate_all(out_dir)
    print(f"\n✅ Done: {len(results)}/{len(SECTION_LIST)} sections → {out_dir}/")
