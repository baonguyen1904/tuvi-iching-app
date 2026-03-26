# Discovery Framework
## "Hiểu trước, build sau"

**Mục đích:** Thu thập evidence từ thực tế để ra quyết định product, KHÔNG dựa trên assumption.  
**Thời gian:** 6-8 tuần  
**Output:** Evidence-based Product Brief — mọi quyết định product đều có data đi kèm

---

## TRIẾT LÝ

Chúng ta KHÔNG biết:
- Tại sao người ta thực sự đi xem bói (functional job? emotional job? social job?)
- Họ đã thử những gì trước khi tìm đến xem bói
- Điều gì khiến họ hài lòng hay thất vọng sau khi xem
- "Risk management" có phải framing mà họ muốn hay chỉ chúng ta thích
- Họ sẵn sàng trả bao nhiêu và cho cái gì
- App có phải dạng họ muốn hay không

Chúng ta CHỈ biết:
- Thị trường xem bói/tử vi online đang lớn (từ search data)
- Có nhiều scam và người dùng bị lừa (từ báo chí)
- Team có scoring engine đang hoạt động
- Team có expert Kinh Dịch

**Rule #1: Mọi insight phải đến từ user, không từ team.**
**Rule #2: Nếu 2 người trong team không đồng ý, đi hỏi user.**

---

## FRAMEWORK OVERVIEW

```
PHASE 1                PHASE 2              PHASE 3              PHASE 4
EXPLORE               PATTERN              TEST                 DECIDE
(Tuần 1-3)            (Tuần 3-4)           (Tuần 4-6)           (Tuần 6-7)
                                                    
"Tại sao?"            "Pattern gì?"        "Đúng không?"        "Build gì?"
                                                    
Qualitative           Synthesis            Quantitative         Product Brief
interviews            & hypotheses         validation           
                                                    
├─ JTBD interviews    ├─ Job mapping       ├─ Survey (n=300+)   ├─ Evidence-based
├─ Switching          ├─ Force analysis    ├─ Concept testing   │  positioning
│  interviews         ├─ Opportunity       ├─ Pricing test      ├─ Validated
├─ Extreme user       │  scoring           ├─ Channel test      │  feature set
│  interviews         ├─ Demand-side       └─ Landing page      ├─ Pricing model
├─ Expert deep dive   │  segmentation         A/B test          ├─ Go-to-market
└─ Competitor                                                   └─ Risk register
   experience audit                                                (real risks)

     GATE 1                GATE 2               GATE 3
     "Có job thực        "Có opportunity      "Có demand
      sự không?"          chưa ai serve?"      đủ lớn không?"
```

---

## PHASE 1: EXPLORE — "Tại sao người ta đi xem bói?"
### Tuần 1-3

Mục tiêu: Thu thập raw stories từ người thật. Không filter, không dẫn dắt.

---

### 1.1 JTBD Interviews (Core method)

**Ai phỏng vấn:** 15-20 người đã từng xem bói/tử vi/kinh dịch trong 12 tháng qua.

**Recruit từ đâu:**
- Facebook groups: "Xem bói online chuẩn" (277K members), "Review xem bói" (101K)
- Post: "Mình đang nghiên cứu về trải nghiệm xem bói/tử vi của người Việt. Nếu bạn đã xem trong năm qua và sẵn lòng chia sẻ trải nghiệm (30 phút, online), mình xin gửi cảm ơn 100K."
- Qua network cá nhân (nhưng tối đa 30% từ network, 70%+ phải là stranger)

**Mix cần đảm bảo:**
- 5-7 người: Xem bói/tử vi cho bản thân (đời sống cá nhân)
- 3-5 người: Xem cho mục đích kinh doanh/công việc
- 3-4 người: Đã dùng app tử vi (Thái Âm, AI Tử Vi, etc.)
- 2-3 người: Đã bỏ tiền nhiều (>500K) cho xem bói
- 2-3 người: Đã bị lừa hoặc thất vọng
- Mix giới tính, tuổi 22-50

**Không phỏng vấn:** Bạn bè thân, người trong team, người biết về project.

---

### 1.2 Bộ câu hỏi JTBD Interview (The Switching Timeline)

Mục tiêu: Reconstruct TOÀN BỘ hành trình từ lúc nảy sinh nhu cầu → tìm kiếm → trải nghiệm → sau đó.

**Phần 1: TRIGGER — Lần xem gần nhất (10 phút)**

```
"Kể cho mình nghe về lần gần nhất bạn đi xem bói/tử vi/kinh dịch."

Probing questions (dùng khi cần, KHÔNG hỏi hết):
- Lúc đó bạn đang ở đâu? Đang làm gì?
- Chuyện gì đang xảy ra trong cuộc sống lúc đó?
- Cảm xúc lúc đó như thế nào?
- Bạn đã suy nghĩ bao lâu trước khi quyết định đi xem?
- Có ai gợi ý hay bạn tự tìm?
- Tại sao lại chọn thời điểm đó để xem?
```

**Phần 2: SEARCH — Quá trình tìm kiếm (10 phút)**

```
"Bạn đã tìm kiếm như thế nào?"

Probing questions:
- Bạn đã cân nhắc những lựa chọn nào? (thầy, app, tự xem, hỏi bạn bè...)
- Tại sao chọn cách này mà không chọn cách khác?
- Bạn dựa vào đâu để biết ai/cái gì đáng tin?
- Có bao nhiêu lựa chọn trước khi quyết định?
- Giá cả có ảnh hưởng không? Bạn sẵn sàng trả bao nhiêu?
- Có rào cản gì khiến bạn suýt không đi xem?
```

**Phần 3: EXPERIENCE — Trải nghiệm (10 phút)**

```
"Kể cho mình nghe trải nghiệm xem bói/tử vi lần đó."

Probing questions:
- Bạn đã hỏi những gì?
- Thầy/app trả lời như thế nào?
- Có điều gì khiến bạn bất ngờ không?
- Có điều gì khiến bạn không thoải mái không?
- Lúc nghe kết quả, cảm xúc thế nào?
- Bạn có hỏi thêm không? Hỏi gì?
```

**Phần 4: AFTERMATH — Sau khi xem (5 phút)**

```
"Sau khi xem xong, chuyện gì xảy ra?"

Probing questions:
- Bạn có làm gì khác so với trước khi xem không?
- Bạn có kể cho ai không? Họ nói gì?
- Nhìn lại, bạn thấy lần xem đó có ích không? Tại sao?
- Bạn có quay lại xem lần nữa không? Tại sao?
- Nếu có thể thay đổi 1 điều về trải nghiệm đó, bạn sẽ thay đổi gì?
```

**Phần 5: META — Bức tranh lớn hơn (5 phút)**

```
Probing questions:
- Khi bạn nói "xem bói", bạn mong đợi nhận được gì?
- Có sự khác biệt giữa "xem cho vui" và "xem thật" không?
- Bạn có phân biệt tử vi, kinh dịch, tarot, thần số học không? Thế nào?
- Có khi nào bạn muốn xem nhưng không xem? Tại sao?
- Ngoài xem bói/tử vi, bạn còn làm gì khi cần hướng dẫn/tư vấn về cuộc sống?
  (VD: hỏi bạn bè, đọc sách, xem coach, tâm lý...)
```

---

### 1.3 Nguyên tắc phỏng vấn (Mom Test rules)

**KHÔNG được:**
- Hỏi "Bạn có dùng app xem tử vi không?" (leading)
- Hỏi "Bạn có muốn app quản lý rủi ro không?" (leading + pitching)
- Nói về idea/product của mình
- Hỏi "Bạn sẽ trả bao nhiêu cho X?" (hypothetical)
- Hỏi yes/no questions

**PHẢI:**
- Hỏi về HÀNH VI QUÁ KHỨ, không hỏi về ý định tương lai
- Hỏi "Lần cuối bạn..." thay vì "Bạn có thường..."
- Khi user nói "tôi thường", hỏi "lần gần nhất là khi nào?"
- Khi user nói điều gì thú vị, im lặng 3 giây — họ sẽ nói thêm
- Ghi chép từng từ (record nếu được phép, LUÔN xin phép trước)

---

### 1.4 Extreme User Interviews (3-5 người)

Phỏng vấn người ở 2 đầu cực:

**Heavy users (2-3 người):**
- Người xem bói/tử vi > 5 lần/năm
- Hoặc đã chi > 2 triệu VNĐ/năm cho xem bói
- Recruit từ: FB groups, hỏi "ai xem thường xuyên nhất"
- Câu hỏi thêm: "Tại sao bạn xem nhiều như vậy? Mỗi lần có khác nhau không?"

**Non-users with same trigger (2-3 người):**
- Người ĐÃ gặp tình huống khó khăn (đổi việc, ly hôn, bệnh...) nhưng KHÔNG đi xem bói
- Recruit từ: Network, post "Ai đã từng phải ra quyết định lớn mà không tham khảo tâm linh?"
- Câu hỏi: "Khi gặp tình huống đó, bạn đã làm gì để quyết định? Tại sao không xem bói?"

**Insight từ extreme users:** Heavy users cho thấy CORE JOB rõ nhất. Non-users cho thấy ALTERNATIVES cạnh tranh thực sự (có thể là therapy, coaching, bạn bè, sách self-help — không phải app khác).

---

### 1.5 Expert Deep Dive (1-2 sessions × 2 giờ)

Phỏng vấn chuyên gia Kinh Dịch (người bạn) — nhưng KHÔNG để design product, mà để hiểu user.

```
"Kể cho mình nghe về những người đến tìm anh/chị xem quẻ."

Câu hỏi:
- Họ thường hỏi về chuyện gì?
- Tâm trạng của họ khi đến thường như thế nào?
- Câu hỏi nào anh/chị gặp nhiều nhất?
- Sau khi xem xong, họ thường phản ứng thế nào?
- Có bao nhiêu % quay lại xem tiếp?
- Anh/chị thấy điều gì khiến họ hài lòng nhất?
- Điều gì khiến họ thất vọng nhất?
- Có nhóm khách nào mà anh/chị cảm thấy giúp được nhiều nhất?
- Có nhóm nào mà anh/chị cảm thấy không nên xem? Tại sao?
- Anh/chị nghĩ phần nào của Kinh Dịch/Tử Vi có value nhất cho người xem?
- Phần nào thường bị hiểu sai nhất?
```

---

### 1.6 Competitor Experience Audit (Parallel, tuần 1-3)

**Tự mình là user** — install và dùng mỗi app 3-5 ngày:

| App | Actions |
|-----|---------|
| Thái Âm | Tạo profile, dùng daily, thử premium |
| AI Tử Vi | Tạo profile, xem Rise/Fall charts |
| I Ching AI | Gieo quẻ, hỏi follow-up |
| Tử Vi Huyền Các | Thử tất cả features |
| Co-Star | UX benchmark, dùng daily |

**Ghi chép cho mỗi app:**
1. First impression (0-30 giây đầu)
2. Onboarding: Hỏi gì? Mất bao lâu? Cảm giác?
3. Wow moment: Có không? Ở đâu? Mất bao lâu để đến?
4. Daily use: Có lý do quay lại không? Notification hữu ích?
5. Paywall: Xuất hiện ở đâu? Có muốn trả không? Tại sao?
6. Chất lượng AI/content: Accurate? Actionable? Generic hay personalized?
7. Điều bực mình nhất
8. Điều thích nhất
9. Tại sao mình sẽ / sẽ không tiếp tục dùng

---

### 1.7 Social Listening (Parallel, tuần 1-3)

**Nơi nghe:**
- Facebook groups xem bói (đọc 100+ posts, KHÔNG post)
- TikTok: #tửvi #kinhdịch #xembói (xem 50+ videos + comments)
- Google Reviews: Thái Âm, AI Tử Vi (đọc 100+ reviews)
- App Store Reviews: Top 5 Vietnamese astrology apps
- Reddit: r/Vietnam, r/astrology (English-speaking Vietnamese)

**Ghi chép:**
- Ngôn ngữ mà user dùng (CHÍNH XÁC TỪ HỌ DÙNG — không paraphrase)
- Câu hỏi phổ biến nhất
- Complaint phổ biến nhất
- Điều họ khen
- Cách họ mô tả nhu cầu của mình

**Template ghi chép social listening:**

| Source | Quote nguyên văn | Category | Sentiment | Insight |
|--------|-----------------|----------|-----------|---------|
| FB group | "Mình muốn xem cho biết năm nay nên cẩn thận gì" | Need | Neutral | Job = phòng tránh, không predict |
| TikTok | "Thầy phán xong lo thêm chứ không bớt lo" | Pain | Negative | Current solution gây thêm anxiety |
| GG Review | "App hay nhưng cứ đọc giống nhau cho mọi người" | Pain | Negative | Thiếu personalization |

---

### GATE 1: Có job thực sự không? (Cuối tuần 3)

**Trước khi sang Phase 2, team phải trả lời được:**

| Câu hỏi | Trả lời bằng gì | Passed nếu |
|---------|------------------|-----------|
| Người ta "hire" xem bói để làm gì? | JTBD statements từ interviews | Có ít nhất 3 jobs rõ ràng, recurring |
| Functional job là gì? | Interview patterns | Có thể articulate trong 1 câu |
| Emotional job là gì? | Interview patterns | Có thể articulate trong 1 câu |
| Social job là gì? | Interview patterns | Có thể articulate trong 1 câu |
| Trigger phổ biến nhất là gì? | Switching timeline data | Top 3 triggers rõ ràng |
| Alternatives thực sự là gì? | Extreme user + non-user data | Biết ít nhất 5 alternatives |
| Current solutions fail ở đâu? | Experience stories | Top 3 pain points rõ ràng |

**Nếu KHÔNG pass:** Tiếp tục interview thêm hoặc pivot research direction.
**Nếu pass:** Sang Phase 2.

---

## PHASE 2: PATTERN — "Những gì chúng ta học được nghĩa là gì?"
### Tuần 3-4

Mục tiêu: Tổng hợp raw data thành patterns, hypotheses, và opportunities có thể test.

---

### 2.1 Job Mapping

Từ interviews, map ra:

```
JOB STATEMENT FORMAT:
"When [situation/trigger], I want to [motivation], 
 so I can [desired outcome]."

VÍ DỤ (giả thuyết — phải validate từ data thực):
"When tôi sắp ra quyết định lớn về career, 
 I want to có thêm một góc nhìn/perspective ngoài logic,
 so I can cảm thấy tự tin hơn khi quyết định."

Mỗi job có 3 dimensions:
- FUNCTIONAL: Cái gì cần xảy ra? (VD: nhận được advice cụ thể)
- EMOTIONAL: Cảm thấy thế nào? (VD: bớt lo lắng, tự tin hơn)
- SOCIAL: Người khác nghĩ gì? (VD: không bị đánh giá là mê tín)
```

**Workshop format:** Team ngồi lại, mỗi người đọc notes interview, viết job statements lên sticky notes (hoặc Miro/FigJam). Cluster thành groups. Vote cho jobs phổ biến nhất.

---

### 2.2 Forces of Progress Analysis

Cho mỗi job chính, phân tích 4 lực tác động vào quyết định "hire" solution:

```
                    PUSH (khiến muốn thay đổi)
                    ↓
    ┌───────────────────────────────┐
    │   SITUATION HIỆN TẠI          │
    │   (current solution)          │──→ PULL (hấp dẫn của new solution)
    │                               │
    └───────────────────────────────┘
                    ↑
    ANXIETY                 HABIT
    (lo ngại về              (quen với
     cái mới)                cái cũ)
```

**Điền từ interview data:**

| Force | Câu hỏi | Ghi từ data |
|-------|---------|-------------|
| **Push** | Điều gì không ổn với cách hiện tại? | [từ interviews] |
| **Pull** | Điều gì hấp dẫn ở giải pháp mới? | [từ interviews] |
| **Anxiety** | Họ lo gì khi thử cái mới? | [từ interviews] |
| **Habit** | Tại sao họ vẫn dùng cách cũ? | [từ interviews] |

**Insight quan trọng:** Nếu Push + Pull > Anxiety + Habit → có cơ hội. Nếu Anxiety + Habit quá mạnh → cần giải quyết chúng trước khi build features.

---

### 2.3 Opportunity Scoring

Liệt kê TẤT CẢ needs/outcomes mà user mention trong interviews. Score theo:

| Need / Desired Outcome | Importance (1-10) | Satisfaction hiện tại (1-10) | Opportunity = Imp + (Imp - Sat) |
|------------------------|-------------------|-------------------------------|----------------------------------|
| [Need A từ interview] | [user rating] | [user rating] | [calculated] |
| [Need B từ interview] | [user rating] | [user rating] | [calculated] |

**Opportunity score = Importance + (Importance - Satisfaction)**

- Score > 15: Rất hấp dẫn (important nhưng chưa ai serve tốt)
- Score 10-15: Đáng quan tâm
- Score < 10: Đã được serve tốt hoặc không quan trọng

**Đây là cách chúng ta biết nên build gì — build cho needs có opportunity score cao nhất, KHÔNG build theo assumption.**

---

### 2.4 Demand-Side Segmentation

Không segment theo demographics (tuổi, giới tính) mà segment theo JOB:

```
VÍ DỤ (phải validate):
Segment A: "Decision validators" 
  — Đã có quyết định rồi, cần thêm confidence
  
Segment B: "Direction seekers"
  — Chưa biết nên làm gì, cần guidance
  
Segment C: "Risk identifiers"  
  — Biết muốn gì, nhưng muốn biết rủi ro
  
Segment D: "Emotional processors"
  — Không thực sự cần advice, cần ai lắng nghe
```

**Cho mỗi segment, ghi:**
- Size estimate (từ survey ở Phase 3)
- Willingness to pay (từ interview data)
- Current solution đang dùng
- Underserved needs
- Phù hợp với capability của team?

---

### GATE 2: Có opportunity chưa ai serve? (Cuối tuần 4)

| Câu hỏi | Trả lời bằng gì | Passed nếu |
|---------|------------------|-----------|
| Top 3 unmet needs là gì? | Opportunity scoring | Score > 15 cho ít nhất 3 needs |
| Segment nào attractive nhất? | Demand-side segmentation | 1-2 segments rõ ràng |
| Forces of progress có thuận lợi? | Force analysis | Push + Pull > Anxiety + Habit |
| Team có capability serve? | Honest assessment | Yes cho core needs |
| Competitive gap thực sự tồn tại? | Competitor audit + user data | Users confirm gap |

**Nếu KHÔNG pass:** Pivot focus, research thêm, hoặc reconsider opportunity.
**Nếu pass:** Sang Phase 3 — validate at scale.

---

## PHASE 3: TEST — "Data có confirm pattern không?"
### Tuần 4-6

Mục tiêu: Quantify patterns từ Phase 2 + test solution concepts.

---

### 3.1 Survey Design (n=300+)

**Recruit:** Facebook Ads targeting "quan tâm tử vi / phong thủy / tâm linh" (25-50 tuổi, VN). Budget: ~3-5 triệu VNĐ.

**Cấu trúc survey (15 phút max):**

```
SECTION 1: Screening (2 câu)
- Bạn đã xem bói/tử vi/kinh dịch trong 12 tháng qua? [Y/N]
- Dưới hình thức nào? [Multi-select: Gặp trực tiếp / Online 1:1 / App / 
  TikTok livestream / Facebook group / Tự xem / Khác]

SECTION 2: Behavior (5 câu — hỏi về QUÁ KHỨ, không tương lai)
- Bao nhiêu lần trong 12 tháng qua? [1 / 2-3 / 4-6 / 7+]
- Chi bao nhiêu tổng cộng? [Free / <100K / 100-500K / 500K-1M / >1M]
- Chủ đề quan tâm nhất? [Rank: career/wealth/health/love/family]
- Bạn đã từng dùng app tử vi/bói chưa? [Y/N] → Nếu Y: App nào?
- Trải nghiệm tổng thể? [1-10 satisfaction scale]

SECTION 3: Jobs validation (4 câu)
- [Dựa trên top jobs từ Phase 2]
- "Khi bạn đi xem bói/tử vi, điều nào quan trọng NHẤT với bạn?"
  [Rank top 5 outcomes từ Phase 2]
- "Điều nào bạn thấy THIẾU nhất ở dịch vụ hiện tại?"
  [Rank top 5 unmet needs từ Phase 2]
- "Bạn đã từng cảm thấy KHÔNG thoải mái khi xem bói?" [Y/N]
  → Nếu Y: Vì sao? [Multi-select options từ Phase 1 pain points]
- "Ngoài xem bói, bạn còn tìm lời khuyên từ đâu?"
  [Multi-select: bạn bè / gia đình / sách / tâm lý / coach / internet / khác]

SECTION 4: Concept test (3 câu)
- [Trình bày 2-3 concept descriptions ngắn — MỖI concept focus vào 
   1 positioning khác nhau, dựa trên Phase 2 insights]
- "Concept nào hấp dẫn bạn nhất?" [Rank]
- "Nếu concept [winner] tồn tại, bạn có dùng không?" 
  [Chắc chắn / Có thể / Không chắc / Không]
- "Bạn sẵn sàng trả bao nhiêu/tháng cho dịch vụ này?"
  [Free only / <50K / 50-100K / 100-200K / 200-500K / >500K]

SECTION 5: Demographics (3 câu)
- Tuổi / Giới tính / Nghề nghiệp
```

---

### 3.2 Concept Testing (Low-fidelity)

Tạo 2-3 concept cards (NOT wireframes — chỉ text + visual direction):

```
CONCEPT A: [Dựa trên top JTBD từ Phase 2]
Tên tạm: "..."
Mô tả 1 dòng: "..."
3 benefits chính:
1. ...
2. ...
3. ...
Visual: Screenshot/mockup đơn giản hoặc Figma prototype 3-5 screens

CONCEPT B: [Dựa trên second JTBD]
...

CONCEPT C: [Dựa trên alternative framing]
...
```

**Test bằng cách:**
- Đưa concept vào survey (Section 4)
- Show cho 10 người từ Phase 1 interviews (đã có trust) → in-depth feedback
- Landing page A/B test (xem phần 3.3)

---

### 3.3 Landing Page A/B Test

Tạo 2-3 landing page variants, mỗi variant test 1 positioning:

**Mỗi page gồm:**
- Headline (positioning statement)
- 3 bullet benefits
- CTA: "Nhận bản phân tích miễn phí" → Email capture
- NO PRODUCT — chỉ promise

**Run Facebook Ads:** Cùng audience, cùng budget, 7 ngày.

**Metrics so sánh:**
- CTR (Click-through rate từ ad)
- Landing page → Email signup rate
- Cost per email signup

**Variant thắng = positioning mà market response tốt nhất.**

---

### 3.4 Willingness to Pay Analysis

Từ survey data, phân tích:

| Price Point | % "Chắc chắn dùng" | % "Có thể dùng" | Revenue estimate |
|-------------|---------------------|-------------------|------------------|
| Free only | X% | - | $0 |
| <50K | X% | Y% | ... |
| 50-100K | X% | Y% | ... |
| 100-200K | X% | Y% | ... |
| 200-500K | X% | Y% | ... |

**Van Westendorp analysis (nếu survey đủ lớn):**
- "Ở giá nào thì quá rẻ (nghi ngờ chất lượng)?"
- "Ở giá nào thì đáng tiền?"
- "Ở giá nào thì đắt nhưng vẫn cân nhắc?"
- "Ở giá nào thì quá đắt?"

---

### GATE 3: Có demand đủ lớn không? (Cuối tuần 6)

| Câu hỏi | Trả lời bằng gì | Passed nếu |
|---------|------------------|-----------|
| Top JTBD có confirmed at scale? | Survey data | >60% rank same top job |
| Concept nào win? | Concept test + A/B | 1 clear winner |
| Conversion potential? | Landing page signup rate | >5% visit→signup |
| Price point viable? | WTP analysis | >30% willing at target price |
| Market size enough? | Survey + market data | TAM > 500K users |
| Competitive advantage real? | User data confirms | Users want what we uniquely offer |

**Nếu KHÔNG pass:** Reassess opportunity, consider pivot.
**Nếu pass:** Sang Phase 4 — Product Brief.

---

## PHASE 4: DECIDE — Evidence-Based Product Brief
### Tuần 6-7

Tổng hợp TOÀN BỘ evidence thành 1 document quyết định.

---

### 4.1 Product Brief Template

```
PRODUCT BRIEF — [App Name]
Date: ___
Based on: [X] interviews, [Y] survey responses, [Z] concept tests

1. TARGET USER
   - Primary segment: [from demand-side segmentation]
   - Job statement: "When [trigger], I want [motivation], so I can [outcome]"
   - Evidence: [X/15 interviewees mentioned this job, Y% survey confirmed]

2. PROBLEM WORTH SOLVING
   - Top unmet need: [from opportunity scoring]
   - Opportunity score: [number]
   - Current alternatives: [list] — why they fail: [evidence]
   
3. POSITIONING
   - One-liner: [from winning concept test]
   - A/B test result: [X% CTR vs Y% for alternatives]
   - User language: [exact words from interviews/social listening]
   
4. CORE FEATURES (Evidence-linked)
   - Feature A: Solves [need] — Evidence: [X% said this is top priority]
   - Feature B: Solves [need] — Evidence: [Y/15 mentioned in interviews]
   - Feature C: Solves [need] — Evidence: [opportunity score Z]
   
5. WHAT WE ARE NOT BUILDING (And why)
   - [Feature X]: Only Y% mentioned, low opportunity score
   - [Feature Y]: Already well-served by competitors
   
6. MONETIZATION
   - Model: [from data] — [X%] willing to pay at [price]
   - Free tier: [what's free — based on what drives acquisition]
   - Paid trigger: [what's paid — based on highest WTP items]
   
7. GO-TO-MARKET
   - Channel: [where our users actually are — from recruit data]
   - Message: [exact language that resonated — from A/B test]
   - Seasonal timing: [from behavioral data]
   
8. RISKS (Real, not assumed)
   - Risk 1: [evidence-based risk + mitigation]
   - Risk 2: ...
   
9. OPEN QUESTIONS (What we still don't know)
   - ...
```

---

## TOOLS & TEMPLATES

### Recording & Note-taking

| Tool | Purpose | Cost |
|------|---------|------|
| Google Docs | Interview notes (1 doc per interview) | Free |
| Miro / FigJam | Synthesis workshops (clustering, mapping) | Free tier |
| Google Forms / Typeform | Survey | Free / $29/mo |
| Google Sheets | Data analysis, opportunity scoring | Free |
| Notion | Research repository (all findings) | Free |
| Loom | Record remote interviews (with permission) | Free |
| Facebook Ads Manager | Survey recruit + Landing page A/B | ~3-5M VNĐ |

### Interview Note Template

```
INTERVIEW #___
Date: ___
Name/alias: ___
Age/Gender: ___
Occupation: ___
Duration: ___ min
Recruited from: ___

CONTEXT:
- What's happening in their life right now?
- Last time they xem bói/tử vi: when, why, how

TRIGGER:
- What specifically triggered it?
- Emotional state?

SEARCH:
- How did they find a solution?
- What alternatives did they consider?
- Why this choice over others?

EXPERIENCE:
- What happened?
- What was good?
- What was bad?
- Did they follow the advice?

AFTERMATH:
- Did it help?
- Would they do it again?
- What would they change?

KEY QUOTES (verbatim):
1. "..."
2. "..."
3. "..."

MY OBSERVATIONS (separate from data):
- ...

JTBD HYPOTHESIS from this interview:
"When ___, I want ___, so I can ___."
```

---

## TIMELINE & RESPONSIBILITY

| Week | Activity | Owner | Hours/week |
|------|----------|-------|------------|
| 1 | Recruit interviewees + setup tools | Founder | 10h |
| 1-2 | Conduct 8-10 JTBD interviews | Founder | 15h |
| 1-2 | Competitor audit (use 5 apps) | Founder or team | 5h |
| 2-3 | Conduct 5-7 more interviews + extremes | Founder | 12h |
| 2-3 | Expert deep dive (2 sessions) | Founder + Expert | 4h |
| 1-3 | Social listening (parallel) | Anyone on team | 5h/week |
| 3 | GATE 1 check | Team | 3h |
| 3-4 | Synthesis workshop (job mapping, forces, opportunities) | Team | 8h |
| 4 | GATE 2 check | Team | 3h |
| 4-5 | Design survey + concept cards | Founder + Designer | 10h |
| 5 | Launch survey + landing page A/B | Founder | 8h |
| 5-6 | Collect + analyze data | Team | 10h |
| 6 | GATE 3 check | Team | 3h |
| 6-7 | Write Evidence-Based Product Brief | Founder | 8h |

**Total effort: ~6-7 weeks, ~15-20 hours/week from founder**

---

## ANTI-PATTERNS — Những điều KHÔNG được làm

1. **KHÔNG skip interviews để chạy survey trước** — Survey chỉ confirm/deny patterns, không discover patterns
2. **KHÔNG hỏi "Bạn có muốn app XYZ không?"** — Mọi người nói yes cho cái gì cũng ok
3. **KHÔNG dùng data để confirm assumption** — Dùng data để THAY ĐỔI assumption
4. **KHÔNG chỉ nói chuyện với người đồng ý với mình** — Tìm người phản đối
5. **KHÔNG bỏ qua Gate checks** — Nếu evidence không đủ, DỪNG LẠI và research thêm
6. **KHÔNG outsource interviews** — Founder PHẢI trực tiếp nói chuyện với user
7. **KHÔNG bắt đầu code trước khi có Product Brief** — Code là investment lớn nhất, phải đúng hướng

---

## MỐI QUAN HỆ VỚI SPECS ĐÃ VIẾT

Specs đã viết (product_spec_module_spec_v1, research_plan_v02) là **giả thuyết tốt nhất hiện tại** dựa trên market research + team knowledge. Chúng KHÔNG sai nhưng CHƯA được validate.

Sau khi hoàn thành Framework này:
- Product Brief sẽ THAY THẾ hoặc CONFIRM các assumptions trong specs
- Một số features có thể bị cắt (không ai cần)
- Một số features mới có thể xuất hiện (user nói cần nhưng ta chưa nghĩ tới)
- Positioning có thể hoàn toàn khác ("risk management" có thể KHÔNG phải framing đúng)
- Pricing có thể thay đổi
- Platform có thể thay đổi (có thể Zalo Mini App là đúng hơn web app)

**Specs cũ = hypothesis. Framework này = validation. Product Brief = evidence-based plan.**

---

*Framework version 1.0 — Adapt khi cần, nhưng KHÔNG skip steps.*