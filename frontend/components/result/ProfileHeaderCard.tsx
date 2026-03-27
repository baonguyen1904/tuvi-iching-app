import { ProfileData } from '@/lib/types';

interface Props {
  profile: ProfileData;
}

export default function ProfileHeaderCard({ profile }: Props) {
  const birthDate = profile.birthDate;

  return (
    <div className="bg-bg-surface border border-border rounded-[12px] p-6 sm:p-4 flex flex-col gap-1 mt-4">
      <p className="text-caption font-medium text-text-tertiary uppercase tracking-wide mb-1">
        Chánh Ngã Đồ
      </p>

      <h1 className="text-heading-md font-bold text-text-primary">
        {profile.name ? profile.name : 'Kết quả luận giải của bạn'}
      </h1>

      <p className="text-body text-text-secondary mt-1">
        Sinh {birthDate} ({profile.metadata?.nam}), {profile.birthHour}, {profile.gender}
      </p>

      <p className="text-body text-text-secondary">
        Cung Mệnh: {profile.metadata?.cungMenh} — Mệnh {profile.metadata?.menh}
      </p>

      <div className="flex flex-wrap gap-2 mt-3">
        {[profile.metadata?.nam, profile.metadata?.cuc, profile.metadata?.amDuong]
          .filter(Boolean)
          .map((tag) => (
            <span
              key={tag}
              className="text-caption bg-bg-subtle border border-border text-text-secondary px-2 py-1 rounded-full"
            >
              {tag}
            </span>
          ))}
      </div>
    </div>
  );
}
