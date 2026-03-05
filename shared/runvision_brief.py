"""
RunVision 와디즈 상세페이지 Brief
엑셀 '상세페이지_기획_1.0 와디즈ver.' 기반 — 와디즈 스타일 카피 우선
"""

from typing import Dict, Any


def create_runvision_brief() -> Dict[str, Any]:
    return {
        "product_name": "RunVision",
        "one_liner": "달리는 시야 안에서 바로 보이는 러닝 전용 스마트글래스",
        "target_audience": "Garmin · Galaxy Watch 사용자 중 달리면서 손목을 드는 습관이 있는 러너",
        "main_problem": "달리는 중 손목을 들어 워치를 확인하는 순간 시선이 흔들리고 리듬이 끊기고 페이스가 떨어진다",
        "key_benefit": "시야 안에서 바로 확인 — 멈추지 않고, 흐름을 유지한 채로",
        "price": {
            "original": "299,000원",
            "discounted": "199,000원",
            "period": "와디즈 얼리버드"
        },
        "urgency": {
            "type": "quantity",
            "value": "얼리버드 100명 한정",
            "bonus": "Garmin · Galaxy Watch 앱 평생 무료"
        },
        "style_preset": "sport-tech",
        "brand_colors": {
            "primary": "#0066FF",
            "secondary": "#001A3D",
            "accent": "#00E5FF"
        },

        # ── 섹션별 카피 (엑셀 와디즈 스타일 기준) ──────────────────
        "copy": {

            # 1.0 인트로 → Hero
            "hero_headline": "가민워치 이제 보지마세요,\n시야에 띄우세요",
            "hero_sub": "RunVision — 러닝 전용 스마트글래스",
            "hero_brand_copy": "우리는 행동하는 순간, 이미 시야 안에 있다.",

            # 2.0 공감&니즈 자극 → Pain
            "pain_intro": "이런 경험 있으신가요?",
            "pain_points": [
                "달리다가 손목을 들어 워치를 확인하는 순간\n시선이 흔들리고 리듬이 끊깁니다",
                "페이스가 떨어져도 다시 올리기가 너무 힘들고\n집중력도 흐트러집니다",
                "달리면서 손목을 보는 것이 불편하고\n안전하지 않다고 느낀 적 있습니다",
            ],
            "pain_hook": "겪어보신 적 있으신가요?",

            # 2.0 전환 → Problem
            "problem_transition": "멈추지 않고, 흐름을 유지한 채로 본다면?",
            "problem_body": (
                "손목을 들지 않아도\n"
                "휴대폰을 열지 않아도\n"
                "달리는 시야 안에서\n"
                "필요한 정보가 바로 보인다면 어떨까요?"
            ),
            "problem_root": "문제는 러닝이 아니라, '확인하는 방식'이었습니다",

            # 2.0 제품 정의 → Solution
            "solution_define": (
                "RunVision은 달리는 중에도 시야를 흐트러뜨리지 않기 위해 설계된\n"
                "러닝 전용 스마트글래스입니다."
            ),
            "solution_tagline": "RunVision은 러닝의 흐름을 지키는 시야입니다",
            "solution_icons": ["휴대폰 ✕", "워치 ✕", "멈춤 ✕"],

            # 4.0 핵심 기능 → How It Works / Benefits
            "feature_headline": "필요한 정보는, 시야 안에 그대로 나타납니다",
            "features": [
                "현재 페이스 (min/km)",
                "러닝 시간",
                "총 거리 (km)",
                "심박수 (bpm)",
                "케이던스 (spm)",
            ],
            "feature_sub": "달리는 동안 고개를 돌리지 않고\n시선을 떼지 않고\n그냥 보면 됩니다.",

            # 4.0 설계 철학 → Authority
            "design_philosophy": "러닝의 흐름을 끊지 않기 위한 설계",
            "design_points": [
                "가벼운 착용감 — 장거리 러닝을 고려한 밸런스",
                "흔들림 최소화 — 안정적인 착용 구조",
                "Garmin · Galaxy Watch 자동 연동 — BLE 원터치 페어링",
            ],

            # How It Works
            "how_it_works": [
                "Garmin · Galaxy Watch\nBLE 자동 연결",
                "마이크로 OLED에 러닝 데이터\n실시간 표시",
                "러닝 종료 후\n데이터 자동 저장",
            ],

            # 7.0 사용감·후기 → Social Proof
            "social_proof_stat": "베타 테스터 27명 · 평균 만족도 4.8/5.0 · 페이스 유지율 +12%",
            "testimonials": [
                {
                    "quote": "달리면서 워치 안 봐도 되니까 너무 편해요. 페이스도 훨씬 잘 유지되고 집중력이 높아졌습니다.",
                    "name": "김○○ · 하프마라톤 러너"
                },
                {
                    "quote": "Garmin 워치랑 연동이 정말 자연스러워요. HUD가 선명하게 잘 보이고, 처음 착용하는데도 불편하지 않았어요.",
                    "name": "이○○ · 마라톤 완주자"
                },
                {
                    "quote": "고개를 내릴 필요가 없으니까 러닝 폼이 훨씬 안정됐어요. 기록도 개선됐고 달리는 게 더 즐거워졌습니다.",
                    "name": "박○○ · 10km 생활체육 러너"
                },
            ],

            # Authority
            "authority": (
                "실제 마라톤 러너가 '달리면서 워치를 보지 않아도 되면 어떨까?' 라는 질문에서 시작된 프로젝트입니다.\n"
                "Garmin · Galaxy Watch 연동 앱과 스마트글래스를 직접 개발하며 수백 시간의 테스트를 거쳤습니다."
            ),

            # Final CTA
            "cta_final": "지금 후원하고, 첫 번째 런비전 러너가 되세요",
        }
    }


if __name__ == "__main__":
    import json
    print(json.dumps(create_runvision_brief(), ensure_ascii=False, indent=2))
