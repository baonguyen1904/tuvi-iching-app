export interface BirthInput {
  name?: string;
  birthDate: string;       // ISO: "1994-07-19"
  birthHour: string;       // enum: ty|suu|dan|mao|thin|ty_|ngo|mui|than|dau|tuat|hoi
  gender: 'male' | 'female';
  namXem: number;          // current year, auto-set
}

export interface ChartDataPoint {
  label: string;           // x-axis: "10-20", "2026", "Th.1"
  duong: number;
  am: number;
  tb: number;
}

export interface DimensionScores {
  // NOTE: label types vary by timeframe:
  //   lifetime → integer ages:  [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
  //   decade   → integer years: [2026, 2027, 2028, ..., 2035]
  //   monthly  → strings:       ["Th.1/2026", "Th.2/2026", ..., "Th.12/2026"]
  // Chart data transforms must call String(label) before using as React key or display text.
  labels: (string | number)[];
  duong: number[];
  am: number[];
  tb: number[];
}

export interface Alert {
  type: 'positive' | 'negative';
  period: string;          // matches chart x-axis label
  tag: string;             // Vietnamese tag text
  level: 30 | 50;
  starName: string;
}

export interface DimensionData {
  label: string;
  summaryScore: number;
  lifetime: DimensionScores;
  decade: DimensionScores;
  monthly: DimensionScores;
  alerts: Alert[];
  interpretation: string | null;   // null for van_menh
}

export interface ProfileMetadata {
  nam: string;             // "Giap Tuat"
  menh: string;            // "Moc"
  cuc: string;             // "Thuy Nhi Cuc"
  amDuong: string;         // "Duong Nam"
  cungMenh: string;
  nguHanh: string;
}

export interface ProfileData {
  profileId: string;
  name: string | null;
  birthDate: string;
  birthHour: string;       // human-readable: "Gio Dan (03:00-05:00)"
  gender: string;          // "Nam" | "Nu"
  metadata: ProfileMetadata;
  overview: { summary: string };
  dimensions: Record<string, DimensionData>;
  createdAt: string;
}

export interface ProfileStatus {
  profileId: string;
  status: 'processing' | 'completed' | 'failed';
  step: string;
  message: string;
  aiProgress?: number;     // 0-8
}

export interface Feedback {
  profileId: string;
  helpful: boolean;
  comment?: string;
}
