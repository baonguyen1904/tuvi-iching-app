# MVP Scope & AI Agent Plan
## "Lean MVP — 2-4 tuần, chạy được, test được"

**Date:** 23/03/2026  
**Goal:** MVP web app luận giải tử vi per dimension, powered by AI + existing scoring engine  
**Test group:** Khách cũ của expert  
**Timeline:** 2-4 tuần

---

## 1. WHAT WE'RE BUILDING (AND NOT BUILDING)

### MVP = "Score-to-Narrative" Engine

User nhập ngày giờ sinh → Hệ thống scrape lá số + tính score → AI sinh luận giải cho từng lĩnh vực → User đọc trên web.

**Khác gì so với hiện tại:**
- Hiện tại: Score → Chart → PPTX (user phải tự đọc chart, chỉ có cảnh báo ngắn)
- MVP: Score + Lá số data → AI generate text luận giải đầy đủ, cá nhân hóa → Web view

### IN SCOPE (MVP)

| Feature | Mô tả |
|---------|--------|
| Input form | Nhập ngày sinh, giờ sinh, giới tính → web form đơn giản |
| Data pipeline | Scrape cohoc.net → parse lá số → run scoring sheet logic |
| AI luận giải per dimension | Chọn 1 lĩnh vực (sự nghiệp / tiền bạc / ...) → AI sinh 1-2 trang text |
| Chart display | Hiện chart score (Dương/Âm/TB) cho lĩnh vực đó |
| Cảnh báo 🔺🔻 | Giữ nguyên logic hiện tại, nhưng AI expand thành advice |
| Web view | Responsive, đọc được trên mobile |
| Shareable link | Mỗi bản luận giải có URL riêng |

### OUT OF SCOPE (Phase 2+)

- Chatbot hỏi đáp
- Tổng hợp multi-dimension advice
- Kinh Dịch gieo quẻ
- User accounts / login
- Payment / premium
- Push notification
- PDF/PPTX export (dùng web view thay thế)
- So sánh biểu đồ (sự nghiệp vs tiền bạc)

---

## 2. USER FLOW (MVP)

```
[Landing page]
  "Xem luận giải vận mệnh cá nhân"
  
     ↓ CTA: "Bắt đầu"
  
[Input form]
  • Họ tên (optional)
  • Ngày sinh (dương lịch date picker)  
  • Giờ sinh (dropdown 12 canh hoặc "không rõ")
  • Giới tính (Nam/Nữ)
  
     ↓ Submit
  
[Processing] (5-10 giây)
  • Đang lấy lá số...
  • Đang phân tích...
  • Đang tạo luận giải...
  
     ↓
  
[Result page]
  ┌─────────────────────────────────────┐
  │ Chánh Ngã Đồ — [Tên user]          │
  │ Sinh: 20/04/1968, 17h45, Nữ        │
  ├─────────────────────────────────────┤
  │                                     │
  │ [Biểu đồ tổng] ← chart embed      │
  │                                     │
  │ Tổng quan vận mệnh                 │
  │ [AI generated summary — 3-5 câu]   │
  │                                     │
  ├─────────────────────────────────────┤
  │ Chọn lĩnh vực xem chi tiết:        │
  │                                     │
  │ [Sự nghiệp] [Tiền bạc] [Hôn nhân] │
  │ [Sức khỏe]  [Đất đai]  [Học tập]  │
  │ [Con cái]                           │
  │                                     │
  │ → Click 1 lĩnh vực                 │
  └─────────────────────────────────────┘
  
     ↓ Click "Sự nghiệp"
  
[Dimension detail page]
  ┌─────────────────────────────────────┐
  │ Luận giải Sự nghiệp — [Tên]        │
  ├─────────────────────────────────────┤
  │                                     │
  │ [Chart sự nghiệp cả đời]           │
  │ [Chart sự nghiệp 10 năm]           │
  │                                     │
  │ ── AI Luận giải ──                  │
  │                                     │
  │ ## Tổng quan sự nghiệp             │
  │ [AI text — bức tranh lớn]           │
  │                                     │
  │ ## Giai đoạn hiện tại (2023-2032)   │
  │ [AI text — phân tích 10 năm]       │
  │                                     │
  │ ## Các mốc cần chú ý               │
  │ 🔺 2025: có cơ hội thăng tiến...   │
  │ → [AI expand: tại sao, nên làm gì] │
  │                                     │
  │ 🔻 2027: dễ gặp kiện cáo...        │
  │ → [AI expand: phòng tránh thế nào] │
  │                                     │
  │ ## Lời khuyên                       │
  │ [AI text — actionable advice]       │
  │                                     │
  └─────────────────────────────────────┘
```

---

## 3. AI AGENT ARCHITECTURE

### 3.1 Approach: "Structured Prompt + KB Context"

KHÔNG build RAG phức tạp cho MVP. Thay vào đó, dùng **structured prompt engineering** với context đầy đủ.

```
INPUT cho AI Agent:
┌──────────────────────────────────────────┐
│ 1. User birth data (tên, ngày giờ sinh) │
│ 2. Lá số gốc data (12 cung × sao)      │
│ 3. Score data per dimension              │
│    (Dương/Âm/TB scores qua các mốc)     │
│ 4. Alert triggers (🔺🔻 + tag text)     │
│ 5. KB context cho dimension đó           │
│    (template luận giải + rules)          │
└──────────────────────────────────────────┘
           ↓
    [LLM — Claude Sonnet]
           ↓
    Structured luận giải text
```

### 3.2 Why NOT RAG for MVP

| Approach | Pros | Cons | MVP fit? |
|----------|------|------|----------|
| Structured prompt + inline KB | Simple, fast, predictable | Limited KB size (~100K tokens) | ✅ YES |
| RAG (vector DB + retrieval) | Scalable KB, flexible | Complex setup, retrieval quality issues | ❌ Overkill |
| Fine-tuned model | Best quality | Expensive, slow iteration, needs data | ❌ Way too much |

**Rationale:** Tử vi knowledge cho 1 dimension fit trong ~5-10K tokens context. Với Claude Sonnet 200K context window, chúng ta có thể đưa cả scoring data + KB rules + prompt trong 1 call. Không cần RAG.

**Khi nào chuyển sang RAG:** Khi KB grow > 100K tokens (Phase 2, khi thêm Kinh Dịch + cross-dimension + chatbot).

### 3.3 Prompt Structure

```markdown
# System Prompt Template — Per Dimension

## Role
Bạn là tư vấn viên luận giải tử vi chuyên nghiệp. Bạn luận giải 
dựa trên DỮ LIỆU CỤ THỂ từ lá số và biểu đồ score, KHÔNG bịa đặt.

## Rules
1. Chỉ nói về những gì data cho thấy — không thêm thông tin ngoài data
2. Ngôn ngữ tích cực, empowering — không gieo sợ hãi
3. Mỗi cảnh báo PHẢI đi kèm lời khuyên cụ thể
4. Dùng "cần thận trọng" thay vì "sẽ gặp họa"
5. Kết thúc bằng disclaimer

## Knowledge Base — {dimension_name}
{kb_content — xem section 4}

## User Data
- Tên: {name}
- Sinh: {birth_date}, {birth_time}, {gender}
- Tuổi hiện tại: {current_age}
- Âm lịch: {lunar_info}
- Cung Mệnh: {menh_cung} — Sao: {menh_stars}
- Cung {relevant_cung}: {stars_in_cung}

## Score Data — {dimension_name}
### Cả đời (mốc 10 năm):
{lifetime_scores — format: age_range | duong | am | tb}

### 10 năm (mốc từng năm):
{decade_scores — format: year | duong | am | tb}

### 12 tháng:
{monthly_scores — format: month | duong | am | tb}

## Alerts
{alerts — format: 🔺/🔻 | time_period | tag_text}

## Output Format
Viết luận giải tiếng Việt, chia thành các phần:

### 1. Tổng quan {dimension} (3-5 câu)
Nhận xét tổng thể dựa trên pattern score cả đời.

### 2. Phân tích giai đoạn hiện tại
Nhìn vào 10 năm gần nhất, đường Dương và Âm đang thế nào.

### 3. Các mốc cần chú ý
Với mỗi alert, giải thích:
- Tại sao mốc này quan trọng (link với sao/cung)
- Nên làm gì / tránh gì
- Đây là xác suất, không phải chắc chắn

### 4. Lời khuyên tổng thể
2-3 điều cụ thể, actionable.

### Disclaimer
"Đây là luận giải tham khảo dựa trên Tử Vi Đẩu Số. 
 Mọi quyết định cuối cùng là của bạn."
```

---

## 4. KNOWLEDGE BASE STRUCTURE

### 4.1 Philosophy: "Expert-in-a-prompt"

KB cho MVP KHÔNG phải database khổng lồ. Nó là **tập hợp các rules + templates** mà expert dùng khi luận giải, được viết dưới dạng LLM có thể hiểu.

### 4.2 KB Files Structure

```
/knowledge-base/
│
├── core/
│   ├── scoring_rules.md          # Giải thích hệ thống Dương/Âm/TB
│   ├── alert_interpretation.md   # Cách đọc 🔺🔻 alerts
│   └── tone_guidelines.md        # Nguyên tắc ngôn ngữ, ethics
│
├── dimensions/
│   ├── su_nghiep.md              # KB cho luận giải sự nghiệp
│   ├── tien_bac.md               # KB cho luận giải tiền bạc
│   ├── hon_nhan.md               # KB cho luận giải hôn nhân
│   ├── suc_khoe.md               # KB cho luận giải sức khỏe
│   ├── dat_dai.md                # KB cho luận giải đất đai
│   ├── hoc_tap.md                # KB cho luận giải học tập
│   └── con_cai.md                # KB cho luận giải con cái
│
├── stars/
│   ├── chinh_tinh.md             # 14 chính tinh — ý nghĩa + điểm
│   └── phu_tinh.md               # Phụ tinh — ý nghĩa khi trigger alert
│
└── templates/
    ├── tong_quan.md              # Template cho phần tổng quan
    └── example_outputs/
        ├── su_nghiep_example.md  # Example output tốt (expert approved)
        └── tien_bac_example.md   # Example output tốt
```

### 4.3 Content Format — Per Dimension KB

**Ví dụ: `/dimensions/su_nghiep.md`**

```markdown
# Knowledge Base — Sự Nghiệp

## Cung liên quan chính
- **Quan Lộc** (cung chính về sự nghiệp)
- **Mệnh** (ảnh hưởng tính cách → cách làm việc)
- **Thiên Di** (ảnh hưởng quan hệ xã hội, đi xa)

## Cách đọc score sự nghiệp

### Khi đường Dương cao (>15)
- Sự nghiệp đang thuận lợi, có cơ hội thăng tiến
- Gặp quý nhân trong công việc
- Được công nhận năng lực

### Khi đường Dương thấp (<5)
- Giai đoạn ổn định, chưa có đột phá
- Nên tập trung tích lũy, học hỏi

### Khi đường Âm sâu (<-5)
- Có áp lực hoặc thử thách trong công việc
- Có thể gặp thị phi, tiểu nhân
- Cần thận trọng trong giao tiếp, quyết định

### Khi Dương và Âm giao nhau
- Giai đoạn chuyển tiếp — có thay đổi lớn
- Nếu Dương vượt lên: đổi mới tích cực
- Nếu Âm vượt lên: cần phòng bị

## Ý nghĩa alerts thường gặp

### 🔺 "có bước thăng tiến hoặc đạt được sự công nhận"
Context: Sao tốt (như Tả Phù, Hữu Bật, Thiên Khôi) 
đang chiếu vào Quan Lộc tại mốc hạn đó.
Advice: Đây là thời điểm tốt để chủ động đề xuất, 
nhận dự án mới, hoặc thể hiện năng lực.

### 🔻 "cẩn thận tiểu nhân, bất công trong công việc"
Context: Sao xấu (Đà La, Kình Dương, Thị Phi) 
đang ảnh hưởng Quan Lộc.
Advice: Cẩn thận lời nói, document mọi thứ, 
tránh conflict không cần thiết. Thời điểm này 
nên giữ thế thủ, không nên mạo hiểm.

### 🔺 "dễ nổi danh / được công nhận"
Context: Sao Khoa, Quyền hoặc Lộc chiếu Quan Lộc.
Advice: Tận dụng cơ hội truyền thông, networking.
Năng lực của bạn dễ được người khác nhìn thấy.

### 🔻 "dễ gặp kiện cáo, thị phi"  
Context: Quan Phù, Bạch Hổ ảnh hưởng Quan Lộc.
Advice: Kiểm tra kỹ hợp đồng, giấy tờ pháp lý.
Tránh tranh chấp, ưu tiên hòa giải.

[...thêm các alert patterns khác]

## Cách luận giải theo giai đoạn tuổi

### Tuổi 20-30
Focus: Xây dựng nền tảng, học nghề, tìm hướng đi
Tone: Khuyến khích thử, chấp nhận sai lầm

### Tuổi 30-45
Focus: Phát triển sự nghiệp, leadership, thu nhập
Tone: Chiến lược, cân bằng risk/reward

### Tuổi 45-60
Focus: Đỉnh cao, truyền đạt, chuẩn bị kế thừa
Tone: Ổn định, bảo vệ thành quả

### Tuổi 60+
Focus: Hưởng thụ, cố vấn, legacy
Tone: An nhiên, nhìn lại hành trình
```

### 4.4 KB Fill Process — Cần expert

**CRITICAL:** Phần quan trọng nhất là expert ngồi review + bổ sung từng dimension KB file. Cách làm hiệu quả nhất:

```
Bước 1: Tech team viết skeleton (framework + alert meanings từ code)
         → 2-3 ngày

Bước 2: Expert review + bổ sung insight vào từng dimension
         → Record session, mỗi dimension ~30 phút = ~4 giờ total
         
         Câu hỏi cho expert mỗi dimension:
         a) "Khi anh nhìn biểu đồ sự nghiệp và thấy đường Dương 
            rất cao ở mốc 60-70, anh nói gì với khách?"
         b) "Khi alert 'cẩn thận tiểu nhân' hiện ra, anh giải thích 
            thêm gì ngoài text đó?"
         c) "Có case nào anh nhớ mà score sự nghiệp tốt nhưng thực 
            tế không tốt? Tại sao?"
         d) "Điều gì quan trọng nhất khi luận sự nghiệp mà sheet 
            scoring KHÔNG capture được?"

Bước 3: Tech team format lại thành KB markdown
         → 1-2 ngày

Bước 4: Test generate luận giải → Expert review output
         → Iterate cho đến khi expert approve
         → 3-5 ngày
```

### 4.5 Expert Session Cần Làm Trước MVP

| Session | Duration | Mục tiêu | Output |
|---------|----------|----------|--------|
| Session 1 | 2h | Expert demo luận giải 2-3 lá số mẫu (record) | Video/audio + notes |
| Session 2 | 2h | Review 7 dimension KBs, bổ sung insight | Annotated KB files |
| Session 3 | 1h | Review AI output mẫu, feedback | Approved examples |

**Total expert time: ~5 giờ** — rất reasonable cho MVP.

---

## 5. TECH ARCHITECTURE (MVP — Simple)

### 5.1 Stack

```
Frontend:     Next.js (hoặc simple HTML + HTMX nếu muốn nhanh hơn)
Backend:      Python FastAPI (1 service)
AI:           Claude Sonnet API (direct call, no RAG)
Data:         SQLite (MVP) hoặc Supabase
Scraper:      Python requests + BeautifulSoup (scrape cohoc.net)
Scoring:      Python (port logic từ Google Sheet)  
Charts:       Chart.js hoặc Recharts (render từ score data)
Deploy:       Vercel (frontend) + Railway (backend)
```

### 5.2 Data Flow

```
[User Input]  ngày sinh, giờ sinh, giới tính
     ↓
[Scraper]     GET tuvi.cohoc.net/lap-la-so-tu-vi.html
              Parse HTML → extract 12 cung × sao list
     ↓
[Scoring]     For each sao in each cung:
                lookup laso_points → get scores + alerts
              Aggregate per dimension per time period
     ↓
[Store]       Save raw lá số + scores to DB (cache)
     ↓
[Chart Gen]   From scores → generate chart data (JSON)
     ↓
[AI Call]     Build prompt:
                system_prompt (role + rules)
                + kb_content (dimension-specific)
                + user_data (birth info + lá số)
                + score_data (Dương/Âm/TB per period)
                + alerts (🔺🔻 + tag text)
              
              Call Claude Sonnet API
              Stream response
     ↓
[Render]      Chart (client-side) + AI text (streamed)
              → Web page
```

### 5.3 API Endpoints (MVP — chỉ cần 3)

```
POST /api/generate
  Body: { birthDate, birthTime, gender, name? }
  Response: { 
    profileId, 
    lasoData,           // 12 cung raw data
    scores,             // all dimensions, all timeframes
    alerts,             // all triggered alerts
    overviewChart       // chart data JSON
  }

GET /api/interpret/{profileId}/{dimension}
  Response: {
    dimension,
    chartData,          // scores for this dimension
    alerts,             // alerts for this dimension  
    interpretation,     // AI generated text (streamed)
  }
  
GET /api/profile/{profileId}
  Response: full cached profile data
```

---

## 6. DEVELOPMENT PLAN — 2-4 WEEKS

### Week 1: Data Pipeline + Scoring

| Day | Task | Output |
|-----|------|--------|
| D1-2 | Port scraper: cohoc.net → parsed lá số | Python script, tested |
| D2-3 | Port scoring logic: Google Sheet → Python | Scoring module, tested |
| D3-4 | Validate: run 5 test cases, compare with Sheet output | Test report |
| D4-5 | API endpoint: POST /generate | Working endpoint |
| D5 | **Expert Session 1:** Demo + record luận giải | Video + notes |

### Week 2: AI Agent + KB

| Day | Task | Output |
|-----|------|--------|
| D1-2 | Write KB skeleton (7 dimensions + core rules) | Markdown files |
| D2 | **Expert Session 2:** Review + annotate KBs | Annotated files |
| D3-4 | Build prompt template + AI call pipeline | Working AI generation |
| D4-5 | Test + iterate prompt quality (5+ test cases) | Tuned prompts |
| D5 | **Expert Session 3:** Review AI output | Approved examples |

### Week 3: Frontend + Integration

| Day | Task | Output |
|-----|------|--------|
| D1-2 | Input form + processing page | Web form working |
| D2-3 | Result page: overview + chart display | Charts rendering |
| D3-4 | Dimension detail page: chart + AI text (streamed) | Full flow working |
| D4-5 | Mobile responsive + polish | Looks good on phone |

### Week 4: Test + Launch (buffer week)

| Day | Task | Output |
|-----|------|--------|
| D1-2 | End-to-end testing (10+ test cases) | Bug fixes |
| D3 | Deploy to production | Live URL |
| D4-5 | Send to test group (khách cũ) + collect feedback | Feedback |

---

## 7. SUCCESS METRICS (MVP Test)

| Metric | Cách đo | Target |
|--------|---------|--------|
| Completion rate | % users hoàn thành input → xem result | > 80% |
| Dimension click-through | % users click xem chi tiết ít nhất 1 dimension | > 60% |
| Time on page | Average time trên dimension detail page | > 2 phút |
| Expert accuracy rating | Expert review 10 outputs, rate 1-10 | > 7/10 |
| User feedback | NPS hoặc simple "có ích không?" survey | > 50% positive |
| Share rate | % users share link | > 10% |

---

## 8. RISKS & MITIGATIONS

| Risk | Impact | Mitigation |
|------|--------|------------|
| Scraper break (cohoc.net thay đổi) | High | Cache results, monitor, có fallback manual input |
| AI hallucinate thông tin sai | High | Constrained prompt, only use provided data, expert review |
| Scoring port sai so với Sheet | High | Test 20+ cases, automated comparison |
| Expert không có time | Medium | Minimize to 5h total, pre-prepare materials |
| cohoc.net block scraping | Medium | Rate limit, cache, consider alternative source |
| AI text quá generic | Medium | Better KB + few-shot examples in prompt |

---

## 9. PHẦN CẦN HỎI EXPERT (Ưu tiên cho Session 1)

### Câu hỏi bắt buộc:

1. **"Khi anh nhìn lá số, anh đọc theo thứ tự nào?"**
   → Capture luận giải flow

2. **"Ngoài score sheet, anh nhìn thêm gì từ lá số gốc?"**  
   → Tổ hợp sao? Tam hợp? Ngũ hành?
   → Đây quyết định KB cần sâu đến đâu

3. **"Cho mỗi lĩnh vực, điều quan trọng nhất anh nói với khách là gì?"**
   → Core message per dimension

4. **"Có điều gì sheet scoring KHÔNG capture được mà anh phải bổ sung?"**
   → KB gap analysis

5. **"Anh có thể luận giải 2-3 lá số mẫu và mình record lại?"**
   → Gold standard examples cho AI to learn from

### Câu hỏi tùy chọn (nếu có thời gian):

6. Khi 2 lĩnh vực mâu thuẫn (sự nghiệp tốt + sức khỏe xấu), anh nói thế nào?
7. Với người trẻ vs người lớn tuổi, cách luận giải có khác không?
8. Alert nào khách quan tâm nhất? Alert nào hay gây hoang mang?

---

## 10. DECISION LOG

| Decision | Rationale | Có thể thay đổi khi |
|----------|-----------|---------------------|
| Web view thay PPTX | Iterate nhanh, mobile-friendly | Nếu user muốn download |
| Luận giải per dimension (not all) | Lean, test quality trước | Khi quality đạt, thêm tổng hợp |
| Claude Sonnet (not GPT) | Vietnamese quality tốt, 200K context | Nếu cost issue |
| Structured prompt (not RAG) | Simple, đủ cho MVP KB size | Khi KB grow > 100K tokens |
| No login cho MVP | Reduce friction, faster test | Khi cần save/return |
| Scrape cohoc.net | Already working pipeline | Khi self-host tử vi engine |
| 2-4 week timeline | Test hypothesis nhanh | Nếu expert cần thêm time |

---

*Next step: Schedule Expert Session 1 → Start Week 1 development parallel*s