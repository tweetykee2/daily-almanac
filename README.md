# 오늘의 역 (daily.almanac12)

매일 아침 인스타그램 @daily.almanac12 에 올라가는 동양 책력 카드.

- `renderer/` — 카드 HTML(index.html), 수묵 일러스트(img/), lunar.js, 렌더러(render.py)
- `posts/YYYY-MM-DD.jpg` — 날짜별 카드 이미지 (Buffer가 raw 주소로 가져감)

렌더: `python3 renderer/render.py 2026-11-26 posts/2026-11-26.jpg` → 이미지 저장 + 캡션 JSON 출력
