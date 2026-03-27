import type { Metadata } from 'next';
import LandingNav from '@/components/landing/LandingNav';
import HeroSection from '@/components/landing/HeroSection';
import HowItWorksSection from '@/components/landing/HowItWorksSection';
import DimensionsPreviewSection from '@/components/landing/DimensionsPreviewSection';
import TrustBuildingSection from '@/components/landing/TrustBuildingSection';
import SamplePreviewSection from '@/components/landing/SamplePreviewSection';
import FAQSection from '@/components/landing/FAQSection';
import FinalCTASection from '@/components/landing/FinalCTASection';
import LandingFooter from '@/components/landing/LandingFooter';

export const metadata: Metadata = {
  title: 'TuVi AI — Luận giải tử vi cá nhân hóa bằng AI',
  description: 'Nhập ngày giờ sinh, nhận luận giải tử vi chi tiết cho 8 lĩnh vực đời sống dựa trên Tử Vi Đẩu Số.',
  openGraph: {
    title: 'TuVi AI — Luận giải tử vi cá nhân hóa bằng AI',
    description: 'AI phân tích lá số tử vi của bạn, cho ra luận giải chi tiết từng lĩnh vực.',
    type: 'website',
  },
};

export default function LandingPage() {
  return (
    <main id="main-content">
      <LandingNav />
      <div className="max-w-3xl mx-auto px-4">
        <HeroSection />
        <HowItWorksSection />
      </div>
      <DimensionsPreviewSection />
      <div className="max-w-3xl mx-auto px-4">
        <TrustBuildingSection />
        <SamplePreviewSection />
      </div>
      <FAQSection />
      <div className="max-w-3xl mx-auto px-4">
        <FinalCTASection />
      </div>
      <LandingFooter />
    </main>
  );
}
