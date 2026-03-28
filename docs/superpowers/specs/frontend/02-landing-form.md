# Frontend Spec — Part 2: Landing Page + Input Form

> Part of the frontend design spec. Index: ../2026-03-27-frontend-design-spec.md

---

## PART 3: PAGE 1 — LANDING PAGE (`/`)

### 3.1 Component Tree

```
app/page.tsx (Server Component, SSR)
├── LandingLayout (layout wrapper, max-w-3xl centered)
│   ├── LandingNav
│   ├── HeroSection
│   ├── HowItWorksSection
│   ├── DimensionsPreviewSection
│   ├── TrustBuildingSection
│   ├── SamplePreviewSection
│   ├── FAQSection
│   ├── FinalCTASection
│   └── LandingFooter
```

### 3.2 LandingNav

```
Position: sticky top-0, z-50
Height: 56px
Background: rgba(250,250,250,0.9) with backdrop-blur-sm
Border-bottom: 1px solid #E5E7EB (shows on scroll — add via scroll listener in client component)

Left: App logo/name — text "TuVi AI", font-semibold text-text-primary
Right: Button "Xem luận giải" → href="/form" (primary button, height 36px, text-sm)

Mobile: same layout, logo left, button right
Scroll behavior: border fades in after 8px scroll (JS in client child component)
```

**Component:** `frontend/components/landing/LandingNav.tsx`
Client component (needs scroll listener for border).

```typescript
interface LandingNavProps {} // no props, self-contained
```

---

### 3.3 HeroSection

```
Layout: flex-col items-center text-center, py-20 (desktop) / py-14 (mobile)
Max-width: 600px centered within parent

[Optional eyebrow tag]
  Pill badge: bg-accent-light border border-accent-border text-accent text-xs font-medium
  px-3 py-1 rounded-full
  Text: "Miễn phí · Không cần đăng ký"

[Headline — h1]
  Text: "Hiểu vận mệnh — Ra quyết định tốt hơn"
  Desktop: text-[36px] font-bold text-text-primary leading-tight
  Mobile: text-[28px] font-bold

[Subheadline — p]
  Text: "Luận giải tử vi cá nhân hóa bằng AI, dựa trên hệ thống Tử Vi Đẩu Số và kiến thức chuyên gia."
  Font: text-body-lg text-text-secondary mt-4 max-w-[480px]

[CTA Button]
  Text: "Xem luận giải miễn phí →"
  Style: primary button, height 48px, px-8, text-base font-medium
  mt-8, href="/form"
  Hover: bg-accent-hover, transform scale(1.01) transition-transform duration-100

[Sub-text below CTA]
  "Miễn phí · Không cần đăng ký · Kết quả trong 30 giây"
  text-caption text-text-tertiary mt-3

[Hero Visual]
  mt-12
  Abstract geometric SVG illustration — concentric circles with node dots
  representing star chart positions (not a real astrology wheel, purely decorative)
  Size: 280px × 280px desktop / 220px × 220px mobile
  Colors: accent blue + gray-200, no fill, stroke only
  Alt text: "Biểu đồ tử vi trực quan"
  SVG hardcoded in component (no external image dependency)
```

**Component:** `frontend/components/landing/HeroSection.tsx`
Server component. No state.

---

### 3.4 HowItWorksSection

```
Layout: py-16 (desktop) / py-10 (mobile)
Section header: "Cách hoạt động", h2 text-heading-md text-center mb-10

Steps container:
  Desktop (≥640px): grid grid-cols-3 gap-6
  Mobile (<640px): flex flex-col gap-4

Each StepCard:
  Layout: flex flex-col items-center text-center p-6
  Background: bg-bg-surface border border-border rounded-[12px]
  Mobile: flex-row items-start text-left gap-4 p-4

  [Step number + icon]
    Circle: w-10 h-10 rounded-full bg-accent-light flex items-center justify-center
    Icon: Lucide, 20px, color accent
    Step 1: ClipboardList icon
    Step 2: BarChart2 icon
    Step 3: FileText icon

  [Step title]
    text-heading-sm text-text-primary mt-4 (desktop) / mt-0 (mobile, inline)

  [Step description]
    text-body text-text-secondary mt-2

Step content:
  1: icon=ClipboardList, title="Nhập ngày giờ sinh", desc="Chỉ cần ngày sinh dương lịch, giờ sinh và giới tính."
  2: icon=BarChart2, title="AI phân tích lá số", desc="Hệ thống tính toán biểu đồ vận mệnh dựa trên Tử Vi Đẩu Số."
  3: icon=FileText, title="Nhận luận giải chi tiết", desc="8 lĩnh vực đời sống (bao gồm Vận mệnh tổng thể), mỗi lĩnh vực có biểu đồ và lời khuyên cụ thể."
     — I11: Changed from "7 lĩnh vực" to "8 lĩnh vực" to include van_menh. Consistent with §3.5 header "8 lĩnh vực được phân tích".

Connector lines between steps (desktop only):
  Position: absolute, top 50% of icon row, between cards
  Style: 1px dashed #E5E7EB
  Hidden on mobile
```

**Component:** `frontend/components/landing/HowItWorksSection.tsx`
Server component.

---

### 3.5 DimensionsPreviewSection

```
Layout: py-16 / py-10, bg-bg-subtle (full-width band, -mx-4 to break out of container)
Section header: "8 lĩnh vực được phân tích", h2 text-heading-md text-center mb-2
Sub-header: "Mỗi lĩnh vực có biểu đồ và lời khuyên riêng", text-body text-text-secondary text-center mb-10

Cards grid:
  Desktop (≥640px): grid grid-cols-4 gap-3  (2 rows × 4 cols)
  Mobile (<640px): grid grid-cols-2 gap-3

IMPORTANT: Include van_menh as the 8th card.

Each DimensionPreviewCard:
  Size: auto height, min-height 100px
  Layout: flex flex-col items-center text-center p-4
  Background: bg-bg-surface border border-border rounded-[12px]
  Hover: border-accent-border transition-colors duration-150

  [Icon container]
    w-10 h-10 rounded-[8px] bg-accent-light flex items-center justify-center
    Icon: 20px Lucide, color accent

  [Name]
    text-label text-text-primary mt-3

  [Description]
    text-body-sm text-text-secondary mt-1 leading-snug

Card data (8 cards in order):
  su_nghiep: icon=Briefcase,   name="Sự nghiệp", desc="Xu hướng thăng tiến, thời điểm thuận lợi"
  tien_bac:  icon=TrendingUp,  name="Tiền bạc",  desc="Biến động tài chính, cơ hội tích lũy"
  hon_nhan:  icon=Heart,       name="Hôn nhân",  desc="Tình duyên, tương thích, thời điểm tốt"
  suc_khoe:  icon=Activity,    name="Sức khỏe",  desc="Giai đoạn cần chú ý, cách phòng tránh"
  dat_dai:   icon=Home,        name="Đất đai",   desc="Mua bán bất động sản, thời điểm giao dịch"
  hoc_tap:   icon=BookOpen,    name="Học tập",   desc="Phát triển bản thân, học vấn, thi cử"
  con_cai:   icon=Baby,        name="Con cái",   desc="Vận con cái, thời điểm sinh con"
  van_menh:  icon=Compass,     name="Vận mệnh",  desc="Bức tranh toàn cục và vận khí tổng thể"
```

**Component:** `frontend/components/landing/DimensionsPreviewSection.tsx`
Server component.

---

### 3.6 TrustBuildingSection

```
Layout: py-16 / py-10
Section header: "Tại sao khác biệt?", h2 text-heading-md text-center mb-10

Trust points container: flex flex-col gap-4 max-w-[560px] mx-auto

Each TrustPoint:
  Layout: flex items-start gap-4
  Icon: CheckCircle2 (Lucide), 20px, color alert-positive, flex-shrink-0 mt-0.5
  Text: text-body text-text-primary

4 trust points:
  "Dựa trên Tử Vi Đẩu Số — hệ thống có phương pháp khoa học, không phải xem bói cảm tính"
  "Knowledge base được xây dựng từ chuyên gia 20+ năm kinh nghiệm thực chiến"
  "AI phân tích dữ liệu thực từ lá số của bạn — không bịa đặt, không generic"
  "Biểu đồ trực quan theo từng giai đoạn đời người, lời khuyên cụ thể có thể hành động ngay"
```

**Component:** `frontend/components/landing/TrustBuildingSection.tsx`
Server component.

---

### 3.7 SamplePreviewSection

```
Layout: py-16 / py-10
Section header: "Kết quả bạn sẽ nhận được", h2 text-heading-md text-center mb-2
Sub-header: text-body text-text-secondary text-center mb-10

Preview container:
  max-w-[600px] mx-auto
  border border-border rounded-[12px] overflow-hidden
  shadow-lg relative

  [Blurred overlay on bottom 40% of image]
    Position: absolute, bottom-0, left-0, right-0, height-40%
    Background: linear-gradient(transparent, #FAFAFA)

  [Sample image]
    A static screenshot of the result page with sample data (blurred)
    File: /public/images/sample-result-preview.png
    Width: 100%, aspect-ratio: 16/10
    Next.js Image component, priority={false}, loading="lazy"
    alt: "Ví dụ kết quả luận giải tử vi"

    M1 — PLACEHOLDER: If sample-result-preview.png does not yet exist, render a placeholder:
    <div className="w-full aspect-[16/10] bg-bg-subtle rounded-[12px] flex items-center justify-center">
      <p className="text-body-sm text-text-tertiary">Ảnh mẫu đang được cập nhật...</p>
    </div>
    Use a conditional: if image file exists (checked at build time via fs.existsSync or simply
    always render placeholder during development), show placeholder. Replace with real Image
    component when screenshot is available.

  [CTA overlay on blurred area]
    Position: absolute bottom-6 left-0 right-0, flex justify-center
    Button: "Xem kết quả của bạn →", primary style
```

**Component:** `frontend/components/landing/SamplePreviewSection.tsx`
Server component.

---

### 3.8 FAQSection

```
Layout: py-16 / py-10, bg-bg-subtle (full-width band)
Section header: "Câu hỏi thường gặp", h2 text-heading-md text-center mb-10

FAQ container: max-w-[600px] mx-auto

Use shadcn Accordion (type="single", collapsible):
  Custom styling: no horizontal padding on AccordionTrigger, py-4
  Border-bottom between items, no border-top on first
  Icon: ChevronDown (Lucide) rotates 180° when open — built into shadcn

5 FAQ items:

Q1: "Khác gì với xem bói trực tuyến thông thường?"
A1: "Tử Vi Đẩu Số là hệ thống có phương pháp rõ ràng — lá số được tính toán từ dữ liệu
    cụ thể (ngày giờ sinh, giới tính) và cho cùng một kết quả với cùng dữ liệu đầu vào.
    AI của chúng tôi chỉ luận giải dựa trên điểm số thực từ lá số của bạn — không bịa
    đặt, không nói chung chung."

Q2: "Kết quả có chính xác không?"
A2: "Tử Vi Đẩu Số là hệ thống có tính logic cao, nhưng không có hệ thống nào dự đoán
    tương lai 100%. Kết quả phản ánh xu hướng vận khí — hãy dùng như một công cụ tham
    khảo để ra quyết định tốt hơn, không phải lời phán quyết tuyệt đối."

Q3: "Thông tin của tôi có được bảo mật không?"
A3: "Dữ liệu ngày giờ sinh được lưu dưới dạng mã hóa, chỉ dùng để tạo lá số. Chúng tôi
    không liên kết với danh tính thật của bạn và không bán dữ liệu cho bên thứ ba."

Q4: "Tại sao cần biết giờ sinh chính xác?"
A4: "Trong Tử Vi Đẩu Số, giờ sinh xác định Cung Mệnh — yếu tố quan trọng nhất của lá
    số. Sai giờ sinh có thể dẫn đến kết quả hoàn toàn khác. Nếu không biết chính xác,
    hãy hỏi cha mẹ hoặc xem sổ khai sinh."

Q5: "Hoàn toàn miễn phí không?"
A5: "Có, giai đoạn này hoàn toàn miễn phí. Chúng tôi đang trong giai đoạn thử nghiệm
    với nhóm người dùng nhỏ để thu thập phản hồi và cải thiện chất lượng luận giải."

Accordion styling overrides:
  AccordionTrigger: text-body font-medium text-text-primary, no underline on hover
  AccordionContent: text-body text-text-secondary pb-4
```

**Component:** `frontend/components/landing/FAQSection.tsx`
Client component (Accordion needs client).
Import shadcn: `import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'`

---

### 3.9 FinalCTASection

```
Layout: py-20 / py-14, text-center

[Headline]
  "Bắt đầu ngay. Miễn phí. Không cần đăng ký."
  text-heading-md text-text-primary

[Sub-text]
  "Nhận luận giải tử vi cá nhân hóa trong 30 giây."
  text-body text-text-secondary mt-3

[CTA Button]
  "Xem luận giải của bạn →"
  Primary button, height 52px, px-10, text-base
  mt-8, href="/form"

No background color — white/transparent, just content centered.
```

**Component:** `frontend/components/landing/FinalCTASection.tsx`
Server component.

---

### 3.10 LandingFooter

```
Layout: border-top border-border py-8
Content: max-w-3xl mx-auto px-4

Flex row on desktop, flex-col on mobile:
  Left: "© 2026 TuVi AI"  text-body-sm text-text-tertiary
  Right (or below on mobile): Disclaimer text, text-caption text-text-tertiary, max-w-[400px]
  Disclaimer: "Nội dung mang tính tham khảo, không phải lời khuyên chuyên nghiệp.
               Mọi quyết định cuối cùng là của bạn."
```

**Component:** `frontend/components/landing/LandingFooter.tsx`
Server component.

---

### 3.11 Landing Page — Full Spec Summary

```typescript
// app/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'TuVi AI — Luận giải tử vi cá nhân hóa bằng AI',
  description: 'Nhập ngày giờ sinh, nhận luận giải tử vi chi tiết cho 8 lĩnh vực đời sống dựa trên Tử Vi Đẩu Số.',
  openGraph: {
    title: 'TuVi AI — Luận giải tử vi cá nhân hóa bằng AI',
    description: 'AI phân tích lá số tử vi của bạn, cho ra luận giải chi tiết từng lĩnh vực.',
    type: 'website',
  },
};

export default function LandingPage() {
  return (
    <main>
      <LandingNav />
      <div className="max-w-3xl mx-auto px-4">
        <HeroSection />
        <HowItWorksSection />
      </div>
      <DimensionsPreviewSection />   {/* full-width bg-subtle band */}
      <div className="max-w-3xl mx-auto px-4">
        <TrustBuildingSection />
        <SamplePreviewSection />
      </div>
      <FAQSection />                  {/* full-width bg-subtle band */}
      <div className="max-w-3xl mx-auto px-4">
        <FinalCTASection />
      </div>
      <LandingFooter />
    </main>
  );
}
```

**Performance:**
- All landing components are Server Components except `LandingNav` (scroll border) and `FAQSection` (accordion)
- No `useEffect` on server components
- Image in SamplePreview: `loading="lazy"`, not `priority`
- Target: Lighthouse ≥ 90 (performance), 100 (SEO)

---

## PART 4: PAGE 2 — INPUT FORM (`/form`)

### 4.1 Component Tree

```
app/form/page.tsx (Server Component, static)
└── FormPageLayout
    ├── FormPageHeader (logo + back link)
    └── BirthInputForm (Client Component — has state/validation)
        ├── NameField
        ├── DateField (shadcn Calendar + Popover)
        ├── HourField (shadcn Select)
        ├── GenderField (shadcn RadioGroup)
        ├── SubmitButton
        └── PrivacyNote
```

### 4.2 Page Layout

```
Background: bg-bg-primary (page), full-height min-h-screen
Layout: flex flex-col items-center justify-center px-4 py-12

FormPageHeader:
  Position: fixed top-0 left-0 right-0, height 56px, bg-bg-surface border-b border-border
  Left: Link "← Trang chủ" (Ghost button, ChevronLeft icon 16px) → href="/"
  Center: "TuVi AI" logo text (absolute centered)
  z-10

Form card:
  max-w-[480px] w-full mx-auto mt-[56px]
  bg-bg-surface border border-border rounded-[12px] shadow-md
  p-6 (desktop) / p-4 (mobile)
```

### 4.3 BirthInputForm Component

**File:** `frontend/components/form/BirthInputForm.tsx`
**Type:** Client Component (`'use client'`)

**State:**

```typescript
interface FormState {
  name: string;
  birthDate: Date | undefined;
  birthHour: string;
  gender: 'male' | 'female' | '';
}

interface FormErrors {
  birthDate?: string;
  birthHour?: string;
  gender?: string;
  submit?: string;
}

const [formState, setFormState] = useState<FormState>({ name: '', birthDate: undefined, birthHour: '', gender: '' });
const [errors, setErrors] = useState<FormErrors>({});
const [isSubmitting, setIsSubmitting] = useState(false);
```

**Form header:**

```
Title: "Nhập thông tin ngày sinh"
  text-heading-sm font-semibold text-text-primary mb-1

Sub-title: "Tất cả thông tin được mã hóa và bảo mật"
  text-body-sm text-text-tertiary mb-6
```

### 4.4 NameField

```
Label: "Họ tên" + Optional badge (text-caption text-text-tertiary bg-bg-subtle px-1.5 py-0.5 rounded ml-2)
Input: type="text" placeholder="Nguyễn Văn A" maxLength={100}
       Standard input styling, height 48px
       onChange: update formState.name

No validation error for this field (optional).
Note below input: text-body-sm text-text-tertiary "Dùng trong luận giải để cá nhân hóa nội dung."
```

### 4.5 DateField

```
Label: "Ngày sinh" + required asterisk (text-accent)

Trigger button:
  Full-width, height 48px, border border-border rounded-[6px]
  text-sm, text-left px-3
  Left: Calendar icon (Lucide, 16px, text-text-tertiary) + gap-2
  Text: selected date formatted as "dd/MM/yyyy" OR placeholder "Chọn ngày sinh" (text-text-tertiary)
  Right: ChevronDown icon, 16px, text-text-tertiary
  Error state: border-red-400

Popover content:
  Use shadcn Popover + Calendar
  Calendar config:
    mode="single"
    selected={formState.birthDate}
    onSelect={handleDateSelect}
    fromYear={1920}
    toYear={new Date().getFullYear()}   // Dynamic: valid up to current year
    defaultMonth: undefined (calendar shows current month initially)
    locale: Vietnamese locale (import from date-fns/locale/vi)
    captionLayout="dropdown-buttons"  // allow year/month jumping
    showOutsideDays={false}

  Calendar styling: match design tokens, accent color for selected day

Error message: "Ngày sinh là bắt buộc. Hợp lệ từ 01/01/1920 đến 31/12/{currentYear}."
  — currentYear is computed at runtime: const currentYear = new Date().getFullYear()
  text-body-sm text-red-500 mt-1.5 flex items-center gap-1
  AlertCircle icon 14px
```

**Validation logic:**

```typescript
function validateDate(date: Date | undefined): string | undefined {
  const currentYear = new Date().getFullYear();
  if (!date) return 'Vui lòng chọn ngày sinh.';
  const year = date.getFullYear();
  if (year < 1920 || year > currentYear) {
    return `Ngày sinh phải từ năm 1920 đến ${currentYear}.`;
  }
  return undefined;
}
```

Error message template (inline in JSX):
```typescript
const currentYear = new Date().getFullYear();
// Error text: `Ngày sinh là bắt buộc. Hợp lệ từ 01/01/1920 đến 31/12/${currentYear}.`
```

### 4.6 HourField

```
Label: "Giờ sinh" + required asterisk
       + Tooltip trigger: Info icon (16px, text-text-tertiary, cursor-help, ml-1)

Tooltip content (shadcn Tooltip, maxWidth 280px):
  "Giờ sinh xác định Cung Mệnh — yếu tố quan trọng nhất trong Tử Vi Đẩu Số.
   Nếu không biết chính xác, hãy hỏi cha mẹ hoặc xem sổ khai sinh."
  text-body-sm, white bg, rounded-[8px], shadow-lg, p-3

shadcn Select:
  value={formState.birthHour}
  onValueChange={(v) => setFormState(s => ({ ...s, birthHour: v }))}

  SelectTrigger: full-width, height 48px, border border-border rounded-[6px]
  SelectValue: placeholder="Chọn giờ sinh"
  Error state: border-red-400 (add class conditionally)

  SelectContent:
    12 SelectItem components from BIRTH_HOURS constant
    Each item: "{label} ({range})"
    e.g. "Giờ Tý (23:00 – 01:00)"
    text-sm, py-2.5 per item (larger tap target)

Error message: "Vui lòng chọn giờ sinh."  text-body-sm text-red-500 mt-1.5
```

### 4.7 GenderField

```
Label: "Giới tính" + required asterisk

shadcn RadioGroup:
  value={formState.gender}
  onValueChange={(v) => setFormState(s => ({ ...s, gender: v as 'male'|'female' }))}
  className="flex gap-4 mt-2"

Two RadioGroupItem options:
  Each option: label wrapping RadioGroupItem
  Layout: flex items-center gap-2, cursor-pointer

  Option 1: value="male",   label="Nam"
  Option 2: value="female", label="Nữ"

  RadioGroupItem size: 20px × 20px
  Custom styling: border-border, checked: border-accent bg-accent
  Label text: text-body text-text-primary, cursor-pointer

Error message: "Vui lòng chọn giới tính."  text-body-sm text-red-500 mt-1.5
```

### 4.8 SubmitButton

```
Placement: mt-8, full-width

States:
  Default (invalid):
    Text: "Xem luận giải →"
    bg-accent opacity-40 cursor-not-allowed (disabled)
    height 48px, w-full, rounded-[8px], text-white font-medium

  Default (valid):
    Same without opacity, cursor-pointer, hover:bg-accent-hover

  Loading (isSubmitting=true):
    Disabled + spinner:
    flex items-center justify-center gap-2
    Loader2 icon (16px, animate-spin) + "Đang xử lý..."

Validation: Submit button enabled only when:
  - birthDate is set AND valid
  - birthHour is not empty
  - gender is not empty
  Use useMemo to derive isFormValid
```

**Submit handler:**

```typescript
async function handleSubmit(e: React.FormEvent) {
  e.preventDefault();

  // Validate all fields
  const newErrors: FormErrors = {
    birthDate: validateDate(formState.birthDate),
    birthHour: !formState.birthHour ? 'Vui lòng chọn giờ sinh.' : undefined,
    gender: !formState.gender ? 'Vui lòng chọn giới tính.' : undefined,
  };

  if (Object.values(newErrors).some(Boolean)) {
    setErrors(newErrors);
    // I9: Focus first invalid field for accessibility
    // Each field wrapper should have data-error="true" when it has an error.
    // Use a short timeout to let React re-render the error state first.
    setTimeout(() => {
      const firstErrorEl = document.querySelector<HTMLElement>('[data-error="true"]');
      firstErrorEl?.focus();
    }, 0);
    return;
  }

  setIsSubmitting(true);
  setErrors({});

  try {
    const birthInputData = {
      name: formState.name || undefined,
      birthDate: format(formState.birthDate!, 'yyyy-MM-dd'),
      birthHour: formState.birthHour,
      gender: formState.gender as 'male' | 'female',
      namXem: new Date().getFullYear(),
    };
    const result = await generateProfile(birthInputData);
    // M4: Store input for retry on processing error
    sessionStorage.setItem('tuvi_last_input', JSON.stringify(birthInputData));
    router.push(`/processing/${result.profileId}`);
  } catch (err) {
    setErrors({ submit: 'Có lỗi xảy ra. Vui lòng thử lại.' });
    setIsSubmitting(false);
  }
}
```

### 4.9 PrivacyNote

```
Placement: mt-4 text-center

Text: "Thông tin ngày sinh không được lưu trữ gắn với danh tính của bạn."
Style: text-caption text-text-tertiary
Icon: Lock (Lucide, 12px) inline before text
```

### 4.10 Field Ordering & Spacing

```
All fields: flex flex-col gap-5 (20px between fields)

Field group structure:
  <div class="flex flex-col gap-1.5">
    <label>...</label>
    <input/select/calendar-trigger>
    {error && <p class="error">...</p>}
  </div>
```

---
