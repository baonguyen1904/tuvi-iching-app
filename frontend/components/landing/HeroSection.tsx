import Link from 'next/link';
import HeroIllustration from './HeroIllustration';

export default function HeroSection() {
  return (
    <section className="flex flex-col items-center text-center py-14 sm:py-20">
      <div className="max-w-[600px]">
        {/* Eyebrow badge */}
        <span className="inline-block bg-accent-light border border-accent-border text-accent
          text-xs font-medium px-3 py-1 rounded-full mb-6">
          Miễn phí &middot; Không cần đăng ký
        </span>

        {/* Headline */}
        <h1 className="text-[28px] sm:text-[36px] font-bold text-text-primary leading-tight">
          Hiểu vận mệnh — Ra quyết định tốt hơn
        </h1>

        {/* Subheadline */}
        <p className="text-base text-text-secondary mt-4 max-w-[480px] mx-auto leading-relaxed">
          Luận giải tử vi cá nhân hóa bằng AI, dựa trên hệ thống Tử Vi Đẩu Số và kiến thức chuyên gia.
        </p>

        {/* CTA */}
        <Link
          href="/form"
          className="inline-flex items-center bg-accent hover:bg-accent-hover text-white
            font-medium text-base px-8 h-12 rounded-md mt-8
            hover:scale-[1.01] transition-all duration-100"
        >
          Xem luận giải miễn phí &rarr;
        </Link>

        {/* Sub-text */}
        <p className="text-xs text-text-tertiary mt-3">
          Miễn phí &middot; Không cần đăng ký &middot; Kết quả trong 30 giây
        </p>
      </div>

      {/* Hero illustration */}
      <div className="mt-12">
        <HeroIllustration />
      </div>
    </section>
  );
}
