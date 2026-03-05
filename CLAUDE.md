# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

**RunVision Wadiz 상세페이지 생성기**

HTML → Playwright → PNG 섹션 생성 후 스티칭하여 와디즈 크라우드펀딩 상세페이지를 만드는 파이프라인.

## Pipeline

```
html_sections_figma.py → 섹션별 PNG (figma-sections/) → stitch_images.py → final_runvision_wadiz.png
```

## Commands

```bash
pip install -r requirements.txt

# 모든 섹션 생성
python3 figma/html_sections_figma.py

# 최종 스티칭
python3 shared/stitch_images.py releases/figma/wadiz/figma-sections releases/figma/wadiz/final_runvision_wadiz.png
```

## Key Files

| 파일 | 설명 |
|------|------|
| `scripts/html_sections_figma.py` | 9개 섹션 HTML→PNG 생성 (메인) |
| `scripts/stitch_images.py` | 섹션 PNG 세로 스티칭 |
| `scripts/generate_cap_photos.py` | Gemini 이미지 생성 (캡 라이프스타일) |
| `scripts/gen_glasses_lifestyle.py` | Gemini 이미지 생성 (글래스 라이프스타일) |

## Environment Variables

```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Section Structure

| 번호 | 섹션 | 높이 |
|------|------|------|
| 01 | Intro 1 (Hero) | ~1550px |
| 02 | Intro 2 (Features) | ~6800px |
| 03 | Core | ~4400px |
| 04 | Special | ~4200px |
| 05 | HOW TO USE + HOW TO WEAR | ~2460px |
| 05c | Before/After | ~1350px |
| 05d | Real User Review | ~1420px |
| 06 | Maker | ~3130px |
| 07 | FAQ | ~4260px |
