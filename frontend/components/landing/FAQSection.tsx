'use client';
import {
  Accordion, AccordionContent, AccordionItem, AccordionTrigger,
} from '@/components/ui/accordion';

const faqs = [
  {
    q: 'Khác gì với xem bói trực tuyến thông thường?',
    a: 'Tử Vi Đẩu Số là hệ thống có phương pháp rõ ràng — lá số được tính toán từ dữ liệu cụ thể (ngày giờ sinh, giới tính) và cho cùng một kết quả với cùng dữ liệu đầu vào. AI của chúng tôi chỉ luận giải dựa trên điểm số thực từ lá số của bạn — không bịa đặt, không nói chung chung.',
  },
  {
    q: 'Kết quả có chính xác không?',
    a: 'Tử Vi Đẩu Số là hệ thống có tính logic cao, nhưng không có hệ thống nào dự đoán tương lai 100%. Kết quả phản ánh xu hướng vận khí — hãy dùng như một công cụ tham khảo để ra quyết định tốt hơn, không phải lời phán quyết tuyệt đối.',
  },
  {
    q: 'Thông tin của tôi có được bảo mật không?',
    a: 'Dữ liệu ngày giờ sinh được lưu dưới dạng mã hóa, chỉ dùng để tạo lá số. Chúng tôi không liên kết với danh tính thật của bạn và không bán dữ liệu cho bên thứ ba.',
  },
  {
    q: 'Tại sao cần biết giờ sinh chính xác?',
    a: 'Trong Tử Vi Đẩu Số, giờ sinh xác định Cung Mệnh — yếu tố quan trọng nhất của lá số. Sai giờ sinh có thể dẫn đến kết quả hoàn toàn khác. Nếu không biết chính xác, hãy hỏi cha mẹ hoặc xem sổ khai sinh.',
  },
  {
    q: 'Hoàn toàn miễn phí không?',
    a: 'Có, giai đoạn này hoàn toàn miễn phí. Chúng tôi đang trong giai đoạn thử nghiệm với nhóm người dùng nhỏ để thu thập phản hồi và cải thiện chất lượng luận giải.',
  },
];

export default function FAQSection() {
  return (
    <section className="py-10 sm:py-16 -mx-4 px-4 bg-bg-subtle">
      <div className="max-w-3xl mx-auto">
        <h2 className="text-[18px] sm:text-[22px] font-semibold text-text-primary text-center mb-10">
          Câu hỏi thường gặp
        </h2>

        <div className="max-w-[600px] mx-auto">
          <Accordion defaultValue={[]}>
            {faqs.map((faq, i) => (
              <AccordionItem key={i} value={`faq-${i}`} className="border-b border-border last:border-0">
                <AccordionTrigger className="text-sm font-medium text-text-primary py-4 hover:no-underline text-left">
                  {faq.q}
                </AccordionTrigger>
                <AccordionContent className="text-sm text-text-secondary pb-4 leading-relaxed">
                  {faq.a}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </section>
  );
}
