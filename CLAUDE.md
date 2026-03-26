# CLAUDE.md — Đọc đầu tiên mỗi session

## Project: Tử Vi AI Luận Giải MVP

**One-liner:** User nhập ngày giờ sinh → Hệ thống tính lá số + scores → AI sinh luận giải cá nhân hóa cho 7 lĩnh vực → User đọc trên web.

**Phase:** MVP (2-4 tuần)
**Test group:** ~20-50 khách cũ của expert partner
**Tên app:** TBD (dùng placeholder "TuVi AI" trong code, dễ đổi sau)

---

## Quick Reference

| Doc | Đọc khi nào |
|-----|-------------|
| `docs/SPEC.md` | Hiểu product: features, user flow, business rules |
| `docs/ARCHITECTURE.md` | Hiểu tech stack, data flow, API contracts |
| `docs/DECISIONS.md` | Hiểu TẠI SAO chọn approach này (không debate lại) |
| `tasks/01_scraper.md` | Build data pipeline (scrape + parse lá số) |
| `tasks/02_scoring_engine.md` | Port scoring logic từ Google Sheet → Python |
| `tasks/03_ai_pipeline.md` | Build AI luận giải engine (prompt + KB + streaming) |
| `tasks/04_frontend.md` | Build web app (landing page + input + results + charts) |
| `tests/EXPECTED_OUTPUTS.md` | Validate outputs match expected behavior |

---

## Tech Stack (đã quyết định)

- **Frontend:** Next.js (App Router, TypeScript)
- **Backend:** Python FastAPI
- **Scraper:** Playwright (async, headless)
- **AI:** Claude Sonnet API (structured prompt, no RAG)
- **DB:** SQLite (MVP cache only)
- **Charts:** Recharts
- **Deploy:** Vercel (frontend) + Railway (backend)

---

## Coding Conventions

- Python: snake_case, type hints, async where possible
- TypeScript: camelCase, strict mode
- API responses: camelCase JSON
- Vietnamese text in KB/prompts: UTF-8, no escaping
- File names: kebab-case
- Commits: conventional commits (feat:, fix:, docs:, chore:)

---

## Critical Rules

1. **KHÔNG bịa data** — AI chỉ luận giải dựa trên scoring data + KB context được cung cấp
2. **Tone tích cực** — Mỗi cảnh báo 🔻 PHẢI kèm lời khuyên. Dùng "cần thận trọng", KHÔNG dùng "sẽ gặp họa"
3. **Giờ sinh bắt buộc** — Nếu user không biết giờ sinh → từ chối, hiện message giải thích tại sao
4. **8 dimensions** — van_menh + 7 lĩnh vực (su_nghiep, tien_bac, hon_nhan, suc_khoe, dat_dai, hoc_tap, con_cai). van_menh có charts nhưng KHÔNG có alerts
5. **2 scrapers** — tuvi.cohoc.net (lifetime + 10yr) + tuvi.vn (monthly). Cả 2 phải scrape cho 1 profile
6. **Pre-generate all dimensions** — Khi user submit, generate tất cả luận giải + overview. Không lazy-load
7. **Star matching dùng python-slugify** — `slugify(name.lower())` cho cả 2 phía (laso_points + scraper output). KHÔNG thay đổi matching logic
8. **Empty weight = 1** — Trong laso_points, nếu dimension weight trống → dùng 1 (không skip star)
9. **Anchor từ LIFETIME data** — House weighting anchor luôn tính từ cung lifetime, kể cả khi scoring 10yr/monthly
10. **Cache by birth data** — Cùng ngày/giờ/giới tính/năm xem = cùng kết quả. Cache scrape + scores
11. **Mobile-first** — Design responsive, test trên mobile trước desktop

---

## Project Structure (target)

```
/
├── frontend/                  # Next.js app
│   ├── app/
│   │   ├── page.tsx           # Landing page
│   │   ├── form/page.tsx      # Input form
│   │   ├── processing/[id]/   # Processing screen
│   │   └── result/[id]/       # Result + dimension detail
│   ├── components/
│   └── lib/
│
├── backend/                   # Python FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── services/
│   │   │   ├── scraper_cohoc.py  # Playwright (lifetime + 10yr)
│   │   │   ├── scraper_tuvivn.py # Playwright (monthly)
│   │   │   ├── scoring.py        # Scoring engine
│   │   │   └── ai_engine.py      # Claude API + prompt builder
│   │   ├── models/
│   │   └── knowledge_base/    # KB markdown files
│   └── tests/
│
├── docs/                      # Specs & decisions
├── tasks/                     # Task definitions
└── tests/                     # Integration test fixtures
```

---

## How to Work

1. Đọc task file trước khi code (`tasks/0X_*.md`)
2. Check acceptance criteria trong task file
3. Run tests sau mỗi milestone
4. Không thay đổi architecture decisions mà không update `docs/DECISIONS.md`
5. Khi gặp edge case không có trong spec → comment `// TODO: clarify` và tiếp tục