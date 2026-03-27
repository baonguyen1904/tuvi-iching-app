import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import { Sparkles, Clock } from 'lucide-react';
import { DimensionKey } from '@/lib/constants';
import { preprocessInterpretation } from '@/lib/utils';

interface Props {
  dimensionKey: DimensionKey;
  interpretation: string | null;
}

export default function AIInterpretationSection({ dimensionKey, interpretation }: Props) {
  return (
    <section className="mt-6">
      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-[18px] h-[18px] text-accent flex-shrink-0" />
        <h2 className="text-label font-semibold text-text-primary">AI Luận Giải</h2>
        <div className="flex-1 h-px bg-border ml-2" />
      </div>

      {/* van_menh: null interpretation -> placeholder */}
      {dimensionKey === 'van_menh' && !interpretation ? (
        <div className="bg-bg-subtle border border-border rounded-[12px] p-6 text-center">
          <Clock className="w-6 h-6 text-text-tertiary mx-auto mb-3" />
          <p className="text-body text-text-secondary">
            Luận giải Vận mệnh đang được cập nhật.
          </p>
          <p className="text-body-sm text-text-tertiary mt-1">
            Vận mệnh là bức tranh tổng thể — xem từng lĩnh vực để hiểu chi tiết.
          </p>
        </div>
      ) : interpretation ? (
        <ReactMarkdown
          rehypePlugins={[rehypeRaw]}
          components={{
            h2: ({ children }) => (
              <h2 className="text-heading-sm font-semibold text-text-primary mt-6 mb-2">
                {children}
              </h2>
            ),
            h3: ({ children }) => (
              <h3 className="text-label font-semibold text-text-primary mt-4 mb-1.5">
                {children}
              </h3>
            ),
            p: ({ children }) => (
              <p className="text-body text-text-secondary leading-relaxed mb-3">
                {children}
              </p>
            ),
            ul: ({ children }) => (
              <ul className="list-disc pl-5 text-body text-text-secondary space-y-1">
                {children}
              </ul>
            ),
            li: ({ children }) => (
              <li className="leading-relaxed">{children}</li>
            ),
            strong: ({ children }) => (
              <strong className="font-semibold text-text-primary">{children}</strong>
            ),
            em: ({ children }) => (
              <em className="italic text-text-secondary">{children}</em>
            ),
            hr: () => <hr className="border-border my-6" />,
            blockquote: ({ children }) => (
              <blockquote className="border-l-2 border-accent pl-4 text-text-secondary italic">
                {children}
              </blockquote>
            ),
          }}
        >
          {preprocessInterpretation(interpretation)}
        </ReactMarkdown>
      ) : (
        <p className="text-body-sm text-text-tertiary">
          Không có nội dung luận giải.
        </p>
      )}
    </section>
  );
}
