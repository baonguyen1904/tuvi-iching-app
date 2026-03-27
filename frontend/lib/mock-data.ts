import type { ProfileData, DimensionData } from '@/lib/types';

const lifetimeLabels = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110];
const decadeLabels = [2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035];
const monthlyLabels = [
  'Th.1/2026', 'Th.2/2026', 'Th.3/2026', 'Th.4/2026',
  'Th.5/2026', 'Th.6/2026', 'Th.7/2026', 'Th.8/2026',
  'Th.9/2026', 'Th.10/2026', 'Th.11/2026', 'Th.12/2026',
];

function makeDimension(overrides: Partial<DimensionData> & { label: string }): DimensionData {
  return {
    summaryScore: 6.5,
    lifetime: {
      labels: lifetimeLabels,
      duong: [2, 5, 8, 10, 7, 3, -1, -4, -2, 1, 3, 5],
      am:    [-1, -3, -5, -2, 1, 4, 6, 8, 5, 2, 0, -2],
      tb:    [0.5, 1, 1.5, 4, 4, 3.5, 2.5, 2, 1.5, 1.5, 1.5, 1.5],
    },
    decade: {
      labels: decadeLabels,
      duong: [5, 7, 10, 8, 3, -2, 1, 4, 6, 8],
      am:    [-2, -1, 3, 5, 7, 9, 6, 2, -1, -3],
      tb:    [1.5, 3, 6.5, 6.5, 5, 3.5, 3.5, 3, 2.5, 2.5],
    },
    monthly: {
      labels: monthlyLabels,
      duong: [3, 5, 7, 4, 2, -1, 1, 6, 8, 5, 3, 4],
      am:    [-1, 2, 4, 6, 3, 1, -2, -1, 3, 5, 7, 2],
      tb:    [1, 3.5, 5.5, 5, 2.5, 0, -0.5, 2.5, 5.5, 5, 5, 3],
    },
    alerts: [],
    interpretation: null,
    ...overrides,
  };
}

export const MOCK_PROFILE: ProfileData = {
  profileId: 'mock-profile-001',
  name: 'Nguyễn Văn An',
  birthDate: '1994-07-19',
  birthHour: 'Giờ Dần (03:00–05:00)',
  gender: 'Nam',
  metadata: {
    nam: 'Giáp Tuất',
    menh: 'Mộc',
    cuc: 'Thủy Nhị Cục',
    amDuong: 'Dương Nam',
    cungMenh: 'Mệnh Cung Thìn',
    nguHanh: 'Thổ',
  },
  overview: {
    summary:
      'Lá số cho thấy mệnh chủ có nền tảng sự nghiệp vững chắc với giai đoạn thăng tiến mạnh từ 2028–2029. Tài chính ổn định, cần thận trọng giai đoạn 2031 khi Kình Dương nhập cung. Nhìn chung vận khí tổng thể tích cực với nhiều cơ hội phát triển.',
  },
  dimensions: {
    su_nghiep: makeDimension({
      label: 'Sự nghiệp',
      summaryScore: 8.2,
      alerts: [
        { type: 'positive', period: '2028', tag: 'Thiên Quan', level: 50, starName: 'Thiên Quan' },
        { type: 'negative', period: '2031', tag: 'Kình Dương', level: 30, starName: 'Kình Dương' },
      ],
      interpretation:
        '## Sự nghiệp 2026–2035\n\n▲ **Giai đoạn thăng tiến mạnh (2028–2029):** Thiên Quan chiếu cung Quan Lộc, tạo điều kiện thuận lợi cho việc thăng chức hoặc mở rộng kinh doanh. Đây là thời điểm tốt để đầu tư vào sự nghiệp.\n\n▼ **Cần thận trọng (2031):** Kình Dương nhập cung, nên tránh quyết định lớn về chuyển việc hoặc khởi nghiệp. Tập trung duy trì ổn định.',
    }),
    tien_bac: makeDimension({
      label: 'Tiền bạc',
      summaryScore: 7.1,
      alerts: [
        { type: 'positive', period: '2029', tag: 'Lộc Tồn', level: 50, starName: 'Lộc Tồn' },
      ],
      interpretation:
        '## Tiền bạc 2026–2035\n\n▲ **Cơ hội tài chính tốt (2029):** Lộc Tồn chiếu cung Tài Bạch, thu nhập có xu hướng tăng đáng kể. Nên tận dụng giai đoạn này để tích lũy.\n\nNhìn chung dòng tiền ổn định, tránh đầu tư mạo hiểm trong các năm có sao xấu nhập cung.',
    }),
    hon_nhan: makeDimension({
      label: 'Hôn nhân',
      summaryScore: 6.8,
      alerts: [
        { type: 'positive', period: '2027', tag: 'Hồng Loan', level: 50, starName: 'Hồng Loan' },
        { type: 'negative', period: '2032', tag: 'Thiên Hình', level: 30, starName: 'Thiên Hình' },
      ],
      interpretation:
        '## Hôn nhân 2026–2035\n\n▲ **Tình duyên thuận lợi (2027):** Hồng Loan chiếu cung Phu Thê, đây là thời điểm tốt cho các mối quan hệ mới hoặc kết hôn.\n\n▼ **Cần thận trọng (2032):** Thiên Hình gây áp lực trong quan hệ, cần kiên nhẫn và thấu hiểu đối phương.',
    }),
    suc_khoe: makeDimension({
      label: 'Sức khỏe',
      summaryScore: 5.9,
      alerts: [
        { type: 'negative', period: '2030', tag: 'Thiên Hư', level: 50, starName: 'Thiên Hư' },
      ],
      interpretation:
        '## Sức khỏe 2026–2035\n\n▼ **Giai đoạn cần chú ý (2030):** Thiên Hư nhập cung Tật Ách, sức khỏe có thể suy giảm. Nên chú trọng kiểm tra sức khỏe định kỳ và duy trì lối sống lành mạnh.\n\n▲ Nhìn chung thể trạng ổn định, năng lượng tốt trong phần lớn thời gian.',
    }),
    dat_dai: makeDimension({
      label: 'Đất đai',
      summaryScore: 6.3,
      alerts: [
        { type: 'positive', period: '2028', tag: 'Thiên Phủ', level: 30, starName: 'Thiên Phủ' },
      ],
      interpretation:
        '## Đất đai 2026–2035\n\n▲ **Thời điểm tốt cho bất động sản (2028):** Thiên Phủ hỗ trợ cung Điền Trạch, phù hợp cho việc mua nhà hoặc đầu tư đất đai.\n\nCần cân nhắc kỹ lưỡng trước khi giao dịch lớn, đặc biệt trong các năm có biến động.',
    }),
    hoc_tap: makeDimension({
      label: 'Học tập',
      summaryScore: 7.5,
      alerts: [
        { type: 'positive', period: '2026', tag: 'Văn Xương', level: 50, starName: 'Văn Xương' },
      ],
      interpretation:
        '## Học tập 2026–2035\n\n▲ **Học vấn thuận lợi (2026):** Văn Xương chiếu cung, khả năng tiếp thu kiến thức mới rất tốt. Nên tận dụng giai đoạn này để nâng cao trình độ chuyên môn.\n\nNhìn chung, vận học tập ổn định và có nhiều cơ hội phát triển bản thân.',
    }),
    con_cai: makeDimension({
      label: 'Con cái',
      summaryScore: 6.0,
      alerts: [
        { type: 'positive', period: '2029', tag: 'Thiên Đức', level: 30, starName: 'Thiên Đức' },
      ],
      interpretation:
        '## Con cái 2026–2035\n\n▲ **Thời điểm tốt (2029):** Thiên Đức hỗ trợ cung Tử Tức, phù hợp cho việc sinh con hoặc các kế hoạch liên quan đến con cái.\n\nQuan hệ với con cái nhìn chung hài hòa, cần dành thời gian quan tâm trong giai đoạn 2031–2032.',
    }),
    van_menh: makeDimension({
      label: 'Vận mệnh',
      summaryScore: 7.0,
      alerts: [],
      interpretation: null,
    }),
  },
  createdAt: '2026-03-27T10:00:00.000Z',
};
