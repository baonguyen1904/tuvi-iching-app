# Kinh Dịch × Tử Vi — AI Risk Management App
## Research Notes & Strategic Plan

**Version:** 0.1 — Brainstorm Phase  
**Date:** 22/03/2026  
**Status:** Research & Discovery

---

## 1. EXECUTIVE SUMMARY

**Concept:** Ứng dụng kết hợp Kinh Dịch (I Ching) và Tử Vi Việt Nam với LLM + Knowledge Base chuyên sâu để cung cấp **lời khuyên quản lý rủi ro cá nhân** qua nhiều khía cạnh cuộc sống (sự nghiệp, tài chính, sức khỏe, tình cảm, gia đình).

**Unique Edge:** Knowledge base từ chuyên gia Kinh Dịch thực chiến — không phải kiến thức generic trên internet, mà là hệ thống diễn giải đã được kiểm chứng qua thực tế xem quẻ.

**Core Positioning:** Không phải "xem bói" → Mà là **"risk intelligence cá nhân"** dựa trên Eastern wisdom + AI.

---

## 2. MARKET LANDSCAPE RESEARCH

### 2.1 Thị trường toàn cầu — Astrology App Market

| Metric | Data |
|--------|------|
| Market size 2025 | ~$3-5 tỷ USD |
| Dự báo 2030 | ~$9-12 tỷ USD |
| CAGR | 19-20% |
| Monthly active users toàn cầu | 120M+ |
| Top demographic | 18-34 tuổi (58-64% users) |
| Freemium model chiếm | ~45% thị phần |
| AI personalization tăng retention | 10-18% |
| Session duration trung bình | 7 phút/session |

**Key Insight:** Asia-Pacific được dự báo là vùng tăng trưởng mạnh nhất do smartphone penetration tăng + văn hóa tâm linh sẵn có.

### 2.2 Competitive Landscape — Vietnamese Market

**Đối thủ trực tiếp (Tử Vi apps Việt Nam):**

| App | Users | Đặc điểm | Điểm yếu |
|-----|-------|-----------|-----------|
| Thái Âm - Tử Vi 2026 | 211K+ | Lá số 12 cung, daily score, leaderboard | Generic, giải trí, không actionable |
| AI Tử Vi - Vận Hạn 2026 | 34K+ | AI-powered, data-driven charts, Rise/Fall charts | Thiếu depth về Kinh Dịch, chưa có risk framework |
| Tử Vi Huyền Các | N/A | Quẻ Kinh Dịch + Tarot + nhiều loại bói | Quá nhiều feature, mê tín, UX kém |
| Tử Vi Việt Nam (tuvi.vn) | N/A | AI tạo lá số, lịch âm dương | Thin content, basic AI |
| Tử vi 12 con giáp | N/A | Tử vi năm, tử vi trọn đời | Static content, không AI |

**Đối thủ quốc tế (I Ching + AI):**

| App | Đặc điểm | Điểm yếu |
|-----|-----------|-----------|
| I Ching AI (ichingai.info) | ChatGPT + 200K chars I Ching texts, actionable advice | Không có Tử Vi, không Vietnamese |
| DivinaAI | Tarot + I Ching + Zodiac combo, 3 AI oracles | Generic fusion, không depth |
| Co-Star | Western astrology, social features | Không có Eastern philosophy |
| The Pattern | Personality-based, relationship matching | Purely Western framework |

### 2.3 Gap Analysis — Cơ hội thị trường

**Không ai đang làm tốt cả 3 điều này cùng lúc:**

1. **Vietnamese Kinh Dịch + Tử Vi kết hợp** — Hầu hết app tách biệt hoặc chỉ có 1 trong 2
2. **Risk Management framing** — Tất cả đối thủ frame là "fortune telling" hoặc "giải trí tâm linh", KHÔNG AI frame là "risk intelligence"
3. **Deep knowledge base + LLM** — Đối thủ dùng generic AI (ChatGPT wrapper) hoặc static content. Không ai có knowledge base từ expert thực chiến

**→ Đây chính là blue ocean: "Personal Risk Intelligence powered by Vietnamese Eastern Wisdom"**

---

## 3. USER INSIGHT RESEARCH PLAN

### 3.1 Persona Hypotheses (cần validate)

**Persona A — "Người tìm hướng" (Primary)**
- 25-40 tuổi, urban Vietnam
- Có quyết định lớn cần đưa ra (đổi việc, đầu tư, kết hôn, mua nhà)
- Không muốn "xem bói" theo kiểu mê tín, nhưng muốn thêm một góc nhìn để ra quyết định
- Pain point: Không biết nên tin ai, thầy bói thì không đáng tin, nhưng vẫn muốn tham khảo
- Willingness to pay: Trung bình đến cao cho advice chất lượng

**Persona B — "Entrepreneur / Business Owner"**
- 30-50 tuổi, đang điều hành business
- Quen sử dụng Kinh Dịch/Tử Vi để hỗ trợ quyết định kinh doanh (timing, đối tác, hướng phát triển)
- Pain point: Muốn có tool nhanh, đáng tin, có thể dùng daily mà không cần gặp thầy
- Willingness to pay: Cao — sẵn sàng trả cho value rõ ràng

**Persona C — "Việt Kiều tò mò"**
- 20-45 tuổi, sống ở nước ngoài
- Muốn kết nối văn hóa Việt nhưng rào cản ngôn ngữ
- Pain point: Không có thầy uy tín ở nước ngoài, thông tin online thì generic
- Willingness to pay: Cao (thu nhập USD)

**Persona D — "Gen Z spiritual"**
- 18-28 tuổi
- Thích tâm linh, tarot, astrology — coi như lifestyle/self-discovery
- Pain point: Thấy Tử Vi cool nhưng khó hiểu, cần ai giải thích dễ hiểu
- Willingness to pay: Thấp nhưng volume lớn, good for acquisition

### 3.2 Research Methods cần thực hiện

**Phase 1: Qualitative (Tuần 1-3)**

| Method | Target | Mục tiêu |
|--------|--------|----------|
| In-depth interviews (1:1) | 5-8 người mỗi persona | Hiểu decision-making process, khi nào/tại sao họ tìm đến Kinh Dịch/Tử Vi |
| Expert interview | Người bạn chuyên gia + 2-3 thầy khác | Map hệ thống knowledge, understand edge cases |
| Competitor user testing | 5 người dùng app đối thủ | Pain points hiện tại, what's missing |
| Social listening | Facebook groups, TikTok, Reddit | Ngôn ngữ user dùng, questions they ask |

**Câu hỏi research quan trọng:**
- Lần cuối bạn xem quẻ/tử vi là khi nào? Vì sao?
- Bạn đã làm gì với thông tin sau khi xem? Có thay đổi quyết định không?
- Điều gì khiến bạn tin/không tin kết quả?
- Nếu có 1 app cho bạn "lời khuyên quản lý rủi ro" dựa trên Kinh Dịch, bạn nghĩ gì?
- Bạn sẵn sàng trả bao nhiêu cho 1 lần tư vấn chuyên sâu?

**Phase 2: Quantitative (Tuần 3-5)**

| Method | Target | Mục tiêu |
|--------|--------|----------|
| Survey (Google Forms / Typeform) | 200-500 người | Validate persona priorities, pricing sensitivity |
| App store review mining | Top 10 competitors | Aggregate pain points, feature requests |
| Google Trends analysis | Keywords liên quan | Seasonal patterns, search demand |

### 3.3 Key Hypotheses cần Validate

| # | Hypothesis | Validation Method |
|---|-----------|-------------------|
| H1 | Users muốn "risk advice" hơn "fortune telling" | A/B test messaging trong survey |
| H2 | Kinh Dịch + Tử Vi combo có value cao hơn đơn lẻ | Conjoint analysis trong survey |
| H3 | Expert-backed knowledge tạo trust hơn generic AI | Interview + willingness to pay test |
| H4 | Bảng chart visual tăng engagement đáng kể | Prototype testing |
| H5 | Business owners willing to pay premium | Interview + pricing test |

---

## 4. PRODUCT CONCEPT FRAMEWORK

### 4.1 Core Product Vision

**Tagline concept:** *"Đừng đoán — Hãy quản lý rủi ro"*

**Positioning Matrix:**

```
                    ENTERTAINMENT ←————→ ACTIONABLE
                         |
    Thái Âm, Huyền Các  |  
    (generic, fun)       |
                         |              ★ OUR APP
         SHALLOW ————————+———————————— DEEP
                         |
    Daily horoscope apps |   AI Tử Vi
    (surface level)      |   (deeper but still fortune-telling)
                         |
```

**App không bảo user "bạn sẽ gặp may mắn tháng 5" → App nói: "Tháng 5 có biến động tài chính, đây là 3 rủi ro cần chú ý và cách phòng tránh"**

### 4.2 Core Feature Set (MVP Hypothesis)

**Module 1: Lá Số Cá Nhân (Tử Vi Engine)**
- Input: Ngày giờ sinh (âm lịch hoặc dương lịch auto convert)
- Output: Bảng chart tử vi visual (dựa trên bản chart đã phát triển)
- AI interpretation: LLM + Knowledge base giải thích từng cung, từng vận
- Risk radar: Highlight các vùng rủi ro theo thời gian

**Module 2: Xem Quẻ Kinh Dịch (On-demand Divination)**
- User đặt câu hỏi cụ thể
- Gieo quẻ (animated, authentic ritual feel)
- AI giải quẻ: Không chỉ nghĩa quẻ mà còn actionable advice
- Follow-up Q&A: User hỏi sâu hơn, AI trả lời based on context

**Module 3: Risk Dashboard**
- Timeline view: Biến động rủi ro theo tháng/quý/năm
- Multi-dimension: Sự nghiệp, Tài chính, Sức khỏe, Tình cảm, Gia đình
- Alert system: Push notification khi vào vùng rủi ro cao
- Action items: Lời khuyên cụ thể cho mỗi giai đoạn

**Module 4: Family Profiles**
- Quản lý lá số cả gia đình
- Compatibility analysis (hợp tuổi, hợp mệnh)
- Family risk calendar: Ai cần chú ý gì, khi nào

### 4.3 Knowledge Base Architecture (The Moat)

```
┌─────────────────────────────────────┐
│          LLM Layer (GPT/Claude)     │
│   Ngôn ngữ tự nhiên + Reasoning    │
├─────────────────────────────────────┤
│     RAG / Retrieval Layer           │
│   Vector DB + Semantic Search       │
├─────────────────────────────────────┤
│     KNOWLEDGE BASE (The Edge)       │
│                                     │
│  ┌───────────┐ ┌────────────────┐   │
│  │ Kinh Dịch │ │ Tử Vi Đẩu Số  │   │
│  │ 64 quẻ    │ │ 12 cung        │   │
│  │ Hào từ    │ │ Sao chính/phụ  │   │
│  │ Biến quẻ  │ │ Đại/Tiểu vận   │   │
│  │ Expert    │ │ Expert          │   │
│  │ interpret │ │ interpret       │   │
│  └───────────┘ └────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │
│  │ Case Studies & Patterns      │   │
│  │ (Curated by expert team)     │   │
│  │ Anonymized real readings     │   │
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │
│  │ Risk Framework Mapping       │   │
│  │ Quẻ/Cung → Risk categories   │   │
│  │ Time-based risk patterns     │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Knowledge base cần digitize:**
- Hệ thống 64 quẻ Kinh Dịch + biến quẻ + expert interpretation cho mỗi quẻ
- Hệ thống 12 cung Tử Vi + Sao + Vận hạn + expert interpretation
- Cross-reference rules: Khi nào dùng Kinh Dịch, khi nào dùng Tử Vi, khi nào kết hợp
- Risk mapping: Mỗi quẻ/cung tương ứng với risk categories nào
- Case patterns: Các pattern thường gặp (anonymized)

---

## 5. MONETIZATION STRATEGY OPTIONS

### 5.1 Revenue Model Analysis

| Model | Pros | Cons | Fit |
|-------|------|------|-----|
| **Freemium** | Acquisition dễ, viral potential | Conversion thấp (2-5%), cần volume | ★★★★ |
| **Subscription** | Recurring revenue, predictable | Churn risk cao, cần daily value | ★★★ |
| **Pay-per-reading** | High intent = high conversion | Inconsistent revenue, no habit | ★★ |
| **B2B for advisors** | High ARPU, niche defensible | Small TAM, sales-heavy | ★★ |
| **Hybrid: Freemium + Credits** | Best of both worlds | Complex to manage | ★★★★★ |

### 5.2 Recommended: Hybrid Freemium + Credit System

**Free Tier:**
- Lá số tử vi cơ bản (overview)
- 1 lần xem quẻ Kinh Dịch/tuần
- Daily risk score (simple)
- Community features

**Premium Tier (~$4.99-9.99/tháng hoặc ~99K-199K VNĐ/tháng):**
- Lá số tử vi chuyên sâu (full 12 cung + vận hạn)
- Unlimited Kinh Dịch readings
- Risk Dashboard đầy đủ
- Family profiles (lên đến 5 người)
- Priority AI response quality

**Credit System (bổ sung):**
- Deep consultation (1 reading = 3-5 credits)
- Expert-level analysis
- Personalized reports (PDF export)

### 5.3 Pricing Benchmark

- Thái Âm: Free + In-app purchases
- AI Tử Vi: Subscription model
- Co-Star: Free + Premium ($2.99/tháng)
- I Ching AI: Free trial + Monthly subscription
- AstroTalk (Ấn Độ): Pay-per-minute consultation ($1-5/phút)

---

## 6. TECHNICAL ARCHITECTURE (HIGH LEVEL)

### 6.1 Tech Stack Recommendation

```
Frontend:     React Native (iOS + Android) hoặc Flutter
Backend:      Node.js / Python FastAPI
AI Engine:    Claude API / OpenAI API + RAG pipeline
Vector DB:    Pinecone / Weaviate / ChromaDB
Database:     PostgreSQL + Redis
Hosting:      AWS / GCP
Knowledge:    Markdown + structured JSON → embedded vào vector DB
```

### 6.2 AI Pipeline

```
User Query
    ↓
Context Builder → Thu thập: birth data, lá số, quẻ hiện tại, lịch sử
    ↓
RAG Retrieval → Tìm relevant knowledge từ vector DB
    ↓
Prompt Engineering → System prompt + Expert persona + Retrieved context + User query
    ↓
LLM Generation → Claude/GPT generate response
    ↓
Post-processing → Format, risk scoring, action item extraction
    ↓
Response to User
```

### 6.3 Key Technical Challenges

| Challenge | Approach |
|-----------|----------|
| Tính toán Tử Vi chính xác (âm lịch, giờ sinh, etc.) | Cần algorithm engine riêng, validate với expert |
| Knowledge base quality & consistency | Expert review cycle, A/B test interpretations |
| LLM hallucination trong lĩnh vực chuyên sâu | Heavy RAG, constrained generation, fact-checking layer |
| Vietnamese language quality | Fine-tune hoặc few-shot prompting, expert review |
| Gieo quẻ Kinh Dịch authentic | Implement đúng thuật toán cổ truyền (yarrow stalk / coin) |

---

## 7. GO-TO-MARKET STRATEGY

### 7.1 Launch Phases

**Phase 0: Pre-launch (Tháng 1-2)**
- Landing page + waitlist
- Content marketing: TikTok/YouTube shorts về Kinh Dịch cho người mới
- Build email list: Target 5,000 signups
- Expert credibility: Giới thiệu chuyên gia, showcase methodology

**Phase 1: Soft Launch / Beta (Tháng 3-4)**
- Invite-only beta: 500-1000 users
- Core features: Lá số + Xem quẻ + Basic AI interpretation
- Feedback loop: In-app surveys, 1:1 interviews với beta users
- Iterate nhanh dựa trên data

**Phase 2: Public Launch (Tháng 5)**
- App Store + Play Store
- PR push: Tech blogs, lifestyle media
- Influencer partnerships: Tâm linh + Lifestyle creators
- Tết Marketing prep (nếu timing phù hợp — Tử Vi theo năm là seasonal peak)

**Phase 3: Growth (Tháng 6-12)**
- Referral program (invite bạn bè xem lá số)
- Seasonal campaigns (Tết, ngày lễ, mùa cưới)
- B2B pilot: Offer tool cho consultants/coaches
- Content flywheel: User-generated questions → AI answers → Content

### 7.2 Marketing Channels

| Channel | Strategy | Budget Priority |
|---------|----------|-----------------|
| TikTok/Reels | Short-form: "Kinh Dịch giải thích [topic]" | ★★★★★ |
| Facebook Groups | Join existing tâm linh groups, provide value | ★★★★ |
| YouTube | Long-form: Expert giải thích methodology | ★★★ |
| App Store Optimization | Keywords: tử vi, kinh dịch, xem quẻ, rủi ro | ★★★★ |
| Referral/Viral | "Xem lá số → Share với bạn bè" | ★★★★★ |
| Paid Ads (FB/Google) | Retargeting, lookalike audiences | ★★ (sau khi có PMF) |

### 7.3 Key Messaging Framework

**KHÔNG nói:** "Xem bói online", "Dự đoán tương lai", "Biết trước số phận"

**NÊN nói:**
- "Hiểu rõ bản thân để ra quyết định tốt hơn"
- "Quản lý rủi ro cuộc sống bằng trí tuệ phương Đông"
- "Không phải xem bói — là chiến lược cá nhân"
- "3000 năm Kinh Dịch + AI = Risk Intelligence cho bạn"

---

## 8. RISK ASSESSMENT (Cho chính project này)

### 8.1 Risks & Mitigations

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Expert knowledge chưa digitize được | Cao | Trung bình | Phân chia thành phases, start small |
| LLM hallucination gây mất trust | Cao | Cao | RAG heavy, disclaimer, expert review layer |
| Market coi là "app xem bói" generic | Trung bình | Cao | Strong branding, differentiated positioning |
| Regulatory risk (Vietnam có thể siết app tâm linh) | Trung bình | Thấp | Frame là "self-development", không claim predict |
| Knowledge base bị copy/leak | Cao | Trung bình | Server-side only, không expose raw knowledge |
| Expert dependency (single point of failure) | Cao | Trung bình | Document hóa mọi thứ sớm, train thêm người |

### 8.2 Critical Success Factors

1. **Knowledge Base Quality** — Đây là moat duy nhất, phải invest nặng
2. **UX/UI Excellence** — Phải đẹp và modern, tránh aesthetic "mê tín"
3. **Trust Building** — Expert credibility, transparency về methodology
4. **Daily Habit** — Nếu user không mở app daily, sẽ churn
5. **Community** — Users talking to each other tạo network effect

---

## 9. NEXT STEPS — ACTION ITEMS

### Immediate (Tuần này)

- [ ] Confirm target persona priorities (đang chờ input từ founder)
- [ ] Schedule expert interview: Map toàn bộ knowledge cần digitize
- [ ] Audit bản chart tử vi hiện có → đánh giá mức độ sẵn sàng
- [ ] Set up research: Recruit 15-20 people cho in-depth interviews

### Short-term (2-4 tuần)

- [ ] Complete qualitative research (interviews)
- [ ] Launch quantitative survey (200+ responses)
- [ ] Begin knowledge base documentation (Phase 1: Kinh Dịch 64 quẻ)
- [ ] Wireframe MVP (low-fi prototypes)
- [ ] Test positioning: "Risk Management" vs "Life Advisor" vs "Wisdom Guide"

### Medium-term (1-2 tháng)

- [ ] Validate MVP features qua prototype testing
- [ ] Build AI pipeline prototype (RAG + LLM)
- [ ] Expert review cycle cho AI outputs
- [ ] Technical architecture finalization
- [ ] Beta user recruitment (target: 500 signups)

---

## 10. OPEN QUESTIONS — Cần thảo luận thêm

1. **Bản chart tử vi hiện tại** ở dạng gì? Cần bao nhiêu effort để digitize thành structured data?
2. **Expert bandwidth:** Người bạn chuyên gia có thể dành bao nhiêu giờ/tuần để build knowledge base?
3. **Ngôn ngữ:** MVP tiếng Việt trước hay bilingual (Việt + English) từ đầu?
4. **Platform:** Mobile-first hay web-first? (Mobile thường tốt hơn cho habit, web tốt hơn cho SEO/content)
5. **Tên app:** Cần brainstorm — nên mang tính "modern wisdom" hơn là "tâm linh truyền thống"
6. **Legal:** Cần disclaimer gì để tránh bị classify là "hành nghề mê tín dị đoan"?
7. **AI model:** Self-host (cost control, privacy) hay API (nhanh, ít invest infra)?

---

*Document này sẽ được update liên tục khi có thêm research data và decisions từ team.*s