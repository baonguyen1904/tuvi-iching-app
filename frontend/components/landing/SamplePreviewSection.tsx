import Link from 'next/link';

export default function SamplePreviewSection() {
  return (
    <section className="py-10 sm:py-16">
      <h2 className="text-[18px] sm:text-[22px] font-semibold text-text-primary text-center mb-2">
        Kết quả bạn sẽ nhận được
      </h2>
      <p className="text-sm text-text-secondary text-center mb-10">
        Luận giải chi tiết, biểu đồ trực quan cho từng giai đoạn cuộc đời
      </p>

      <div className="max-w-[600px] mx-auto border border-border rounded-[12px] overflow-hidden shadow-lg relative">
        {/* M1: Placeholder -- replace with Next.js Image when screenshot is ready */}
        <div className="w-full aspect-[16/10] bg-bg-subtle flex items-center justify-center">
          <p className="text-xs text-text-tertiary">Ảnh mẫu đang được cập nhật...</p>
        </div>

        {/* Gradient overlay */}
        <div className="absolute bottom-0 left-0 right-0 h-[40%]
          bg-gradient-to-t from-bg-primary to-transparent pointer-events-none" />

        {/* CTA overlay */}
        <div className="absolute bottom-6 left-0 right-0 flex justify-center">
          <Link
            href="/form"
            className="bg-accent hover:bg-accent-hover text-white font-medium text-sm
              px-6 h-10 rounded-md flex items-center transition-colors duration-100"
          >
            Xem kết quả của bạn &rarr;
          </Link>
        </div>
      </div>
    </section>
  );
}
