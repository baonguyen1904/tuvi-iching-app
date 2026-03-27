import { CheckCircle2 } from 'lucide-react';

const points = [
  'Dựa trên Tử Vi Đẩu Số — hệ thống có phương pháp khoa học, không phải xem bói cảm tính',
  'Knowledge base được xây dựng từ chuyên gia 20+ năm kinh nghiệm thực chiến',
  'AI phân tích dữ liệu thực từ lá số của bạn — không bịa đặt, không generic',
  'Biểu đồ trực quan theo từng giai đoạn đời người, lời khuyên cụ thể có thể hành động ngay',
];

export default function TrustBuildingSection() {
  return (
    <section className="py-10 sm:py-16">
      <h2 className="text-[18px] sm:text-[22px] font-semibold text-text-primary text-center mb-10">
        Tại sao khác biệt?
      </h2>

      <div className="flex flex-col gap-4 max-w-[560px] mx-auto">
        {points.map((point, i) => (
          <div key={i} className="flex items-start gap-4">
            <CheckCircle2 size={20} className="text-alert-positive flex-shrink-0 mt-0.5" />
            <p className="text-sm text-text-primary leading-relaxed">{point}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
