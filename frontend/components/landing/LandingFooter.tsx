export default function LandingFooter() {
  return (
    <footer className="border-t border-border py-8">
      <div className="max-w-3xl mx-auto px-4 flex flex-col sm:flex-row items-start sm:items-center
        justify-between gap-3">
        <span className="text-xs text-text-tertiary">&copy; 2026 TuVi AI</span>
        <p className="text-[11px] text-text-tertiary max-w-[400px] leading-relaxed">
          Nội dung mang tính tham khảo, không phải lời khuyên chuyên nghiệp.
          Mọi quyết định cuối cùng là của bạn.
        </p>
      </div>
    </footer>
  );
}
