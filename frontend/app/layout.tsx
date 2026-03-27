import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Toaster } from 'sonner';
import './globals.css';

const inter = Inter({
  subsets: ['latin', 'vietnamese'],
  variable: '--font-inter',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'TuVi AI — Luận giải tử vi cá nhân hóa bằng AI',
  description: 'Nhập ngày giờ sinh, nhận luận giải tử vi chi tiết cho 8 lĩnh vực đời sống dựa trên Tử Vi Đẩu Số.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi" className={inter.variable}>
      <body className="font-sans bg-bg-primary text-text-primary">
        {children}
        <Toaster richColors position="top-center" />
      </body>
    </html>
  );
}
