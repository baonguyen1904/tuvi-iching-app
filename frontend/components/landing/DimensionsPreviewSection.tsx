import { Briefcase, TrendingUp, Heart, Activity, Home, BookOpen, Baby, Compass, type LucideIcon } from 'lucide-react';

const dimensions: Array<{ icon: LucideIcon; name: string; desc: string }> = [
  { icon: Briefcase,   name: 'Sự nghiệp', desc: 'Xu hướng thăng tiến, thời điểm thuận lợi' },
  { icon: TrendingUp,  name: 'Tiền bạc',  desc: 'Biến động tài chính, cơ hội tích lũy' },
  { icon: Heart,       name: 'Hôn nhân',  desc: 'Tình duyên, tương thích, thời điểm tốt' },
  { icon: Activity,    name: 'Sức khỏe',  desc: 'Giai đoạn cần chú ý, cách phòng tránh' },
  { icon: Home,        name: 'Đất đai',   desc: 'Mua bán bất động sản, thời điểm giao dịch' },
  { icon: BookOpen,    name: 'Học tập',   desc: 'Phát triển bản thân, học vấn, thi cử' },
  { icon: Baby,        name: 'Con cái',   desc: 'Vận con cái, thời điểm sinh con' },
  { icon: Compass,     name: 'Vận mệnh',  desc: 'Bức tranh toàn cục và vận khí tổng thể' },
];

export default function DimensionsPreviewSection() {
  return (
    <section className="py-10 sm:py-16 -mx-4 px-4 bg-bg-subtle">
      <div className="max-w-3xl mx-auto">
        <h2 className="text-[18px] sm:text-[22px] font-semibold text-text-primary text-center mb-2">
          8 lĩnh vực được phân tích
        </h2>
        <p className="text-sm text-text-secondary text-center mb-10">
          Mỗi lĩnh vực có biểu đồ và lời khuyên riêng
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {dimensions.map((dim) => {
            const Icon = dim.icon;
            return (
              <div
                key={dim.name}
                className="flex flex-col items-center text-center p-4 min-h-[100px]
                  bg-bg-surface border border-border rounded-[12px]
                  hover:border-accent-border transition-colors duration-150"
              >
                <div className="w-10 h-10 rounded-[8px] bg-accent-light flex items-center justify-center">
                  <Icon size={20} className="text-accent" />
                </div>
                <p className="text-[13px] font-medium text-text-primary mt-3">{dim.name}</p>
                <p className="text-xs text-text-secondary mt-1 leading-snug">{dim.desc}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
