import Link from 'next/link';

export default function FinalCTASection() {
  return (
    <section className="py-14 sm:py-20 text-center">
      <h2 className="text-[18px] sm:text-[22px] font-semibold text-text-primary">
        Bắt đầu ngay. Miễn phí. Không cần đăng ký.
      </h2>
      <p className="text-sm text-text-secondary mt-3">
        Nhận luận giải tử vi cá nhân hóa trong 30 giây.
      </p>
      <Link
        href="/form"
        className="inline-flex items-center bg-accent hover:bg-accent-hover text-white
          font-medium text-base px-10 h-[52px] rounded-md mt-8
          transition-colors duration-100"
      >
        Xem luận giải của bạn &rarr;
      </Link>
    </section>
  );
}
