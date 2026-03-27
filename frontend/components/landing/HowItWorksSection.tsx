import { ClipboardList, BarChart2, FileText } from 'lucide-react';

const steps = [
  {
    icon: ClipboardList,
    title: 'Nhập ngày giờ sinh',
    desc: 'Chỉ cần ngày sinh dương lịch, giờ sinh và giới tính.',
  },
  {
    icon: BarChart2,
    title: 'AI phân tích lá số',
    desc: 'Hệ thống tính toán biểu đồ vận mệnh dựa trên Tử Vi Đẩu Số.',
  },
  {
    icon: FileText,
    title: 'Nhận luận giải chi tiết',
    desc: '8 lĩnh vực đời sống (bao gồm Vận mệnh tổng thể), mỗi lĩnh vực có biểu đồ và lời khuyên cụ thể.',
  },
];

export default function HowItWorksSection() {
  return (
    <section className="py-10 sm:py-16">
      <h2 className="text-[18px] sm:text-[22px] font-semibold text-text-primary text-center mb-10">
        Cách hoạt động
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6 relative">
        {steps.map((step, i) => {
          const Icon = step.icon;
          return (
            <div
              key={i}
              className="flex flex-row sm:flex-col items-start sm:items-center
                sm:text-center gap-4 sm:gap-0 p-4 sm:p-6
                bg-bg-surface border border-border rounded-[12px]"
            >
              <div className="w-10 h-10 rounded-full bg-accent-light flex items-center justify-center flex-shrink-0">
                <Icon size={20} className="text-accent" />
              </div>
              <div className="sm:mt-4">
                <h3 className="text-[15px] font-semibold text-text-primary">
                  {step.title}
                </h3>
                <p className="text-sm text-text-secondary mt-1 sm:mt-2 leading-relaxed">
                  {step.desc}
                </p>
              </div>
            </div>
          );
        })}

        {/* Connector lines -- desktop only */}
        <div className="hidden sm:block absolute top-[52px] left-[calc(33.33%-8px)] w-[calc(16px)]
          border-t border-dashed border-border pointer-events-none" />
        <div className="hidden sm:block absolute top-[52px] left-[calc(66.66%-8px)] w-[calc(16px)]
          border-t border-dashed border-border pointer-events-none" />
      </div>
    </section>
  );
}
