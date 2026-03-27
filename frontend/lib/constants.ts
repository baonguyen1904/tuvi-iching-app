export const DIMENSION_ICONS = {
  su_nghiep: 'Briefcase', tien_bac: 'TrendingUp', hon_nhan: 'Heart',
  suc_khoe: 'Activity', dat_dai: 'Home', hoc_tap: 'BookOpen',
  con_cai: 'Baby', van_menh: 'Compass',
} as const;

export const DIMENSION_LABELS = {
  su_nghiep: 'Sự nghiệp', tien_bac: 'Tiền bạc', hon_nhan: 'Hôn nhân',
  suc_khoe: 'Sức khỏe', dat_dai: 'Đất đai', hoc_tap: 'Học tập',
  con_cai: 'Con cái', van_menh: 'Vận mệnh',
} as const;

export const DIMENSION_ORDER = [
  'su_nghiep', 'tien_bac', 'hon_nhan', 'suc_khoe',
  'dat_dai', 'hoc_tap', 'con_cai', 'van_menh',
] as const;

export type DimensionKey = typeof DIMENSION_ORDER[number];

export const BIRTH_HOURS = [
  { value: 'ty',   label: 'Giờ Tý',   range: '23:00 – 01:00' },
  { value: 'suu',  label: 'Giờ Sửu',  range: '01:00 – 03:00' },
  { value: 'dan',  label: 'Giờ Dần',  range: '03:00 – 05:00' },
  { value: 'mao',  label: 'Giờ Mão',  range: '05:00 – 07:00' },
  { value: 'thin', label: 'Giờ Thìn', range: '07:00 – 09:00' },
  { value: 'ty_',  label: 'Giờ Tỵ',   range: '09:00 – 11:00' },
  { value: 'ngo',  label: 'Giờ Ngọ',  range: '11:00 – 13:00' },
  { value: 'mui',  label: 'Giờ Mùi',  range: '13:00 – 15:00' },
  { value: 'than', label: 'Giờ Thân', range: '15:00 – 17:00' },
  { value: 'dau',  label: 'Giờ Dậu',  range: '17:00 – 19:00' },
  { value: 'tuat', label: 'Giờ Tuất', range: '19:00 – 21:00' },
  { value: 'hoi',  label: 'Giờ Hợi',  range: '21:00 – 23:00' },
] as const;

export const FUN_FACTS: readonly string[] = [
  'Hệ thống Tử Vi Đẩu Số có 14 chính tinh và hơn 100 phụ tinh, tạo ra vô số tổ hợp độc đáo.',
  'Lá số của bạn là duy nhất — chỉ ai sinh cùng ngày, giờ và giới tính mới có lá số giống hệt.',
  'Tử Vi Đẩu Số có nguồn gốc hơn 1000 năm, được hoàn thiện trong triều đại Tống ở Trung Hoa.',
  'Hệ thống chia cuộc đời thành các chu kỳ 10 năm (Đại Vận) — mỗi chu kỳ có năng lượng riêng.',
  'AI đang phân tích hàng trăm điểm dữ liệu từ lá số của bạn để tạo luận giải cá nhân hóa.',
];
