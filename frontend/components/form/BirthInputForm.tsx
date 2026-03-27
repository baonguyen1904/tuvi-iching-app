'use client';
import { useState, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import { format } from 'date-fns';
import { Info, Loader2, Lock, AlertCircle } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import DatePickerField from './DatePickerField';
import { BIRTH_HOURS } from '@/lib/constants';
import { generateProfile } from '@/lib/api';

interface FormState {
  name: string;
  birthDate: Date | undefined;
  birthHour: string;
  gender: 'male' | 'female' | '';
}

interface FormErrors {
  birthDate?: string;
  birthHour?: string;
  gender?: string;
  submit?: string;
}

function validateDate(date: Date | undefined): string | undefined {
  const currentYear = new Date().getFullYear();
  if (!date) return 'Vui lòng chọn ngày sinh.';
  const year = date.getFullYear();
  if (year < 1920 || year > currentYear) {
    return `Ngày sinh phải từ năm 1920 đến ${currentYear}.`;
  }
  return undefined;
}

export default function BirthInputForm() {
  const router = useRouter();
  const [formState, setFormState] = useState<FormState>({
    name: '', birthDate: undefined, birthHour: '', gender: '',
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isFormValid = useMemo(
    () => !!formState.birthDate && !validateDate(formState.birthDate)
      && !!formState.birthHour && !!formState.gender,
    [formState.birthDate, formState.birthHour, formState.gender],
  );

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const newErrors: FormErrors = {
      birthDate: validateDate(formState.birthDate),
      birthHour: !formState.birthHour ? 'Vui lòng chọn giờ sinh.' : undefined,
      gender: !formState.gender ? 'Vui lòng chọn giới tính.' : undefined,
    };

    if (Object.values(newErrors).some(Boolean)) {
      setErrors(newErrors);
      // I9: Focus first invalid field
      setTimeout(() => {
        const firstErrorEl = document.querySelector<HTMLElement>('[data-error="true"]');
        firstErrorEl?.focus();
      }, 0);
      return;
    }

    setIsSubmitting(true);
    setErrors({});

    try {
      const birthInputData = {
        name: formState.name || undefined,
        birthDate: format(formState.birthDate!, 'yyyy-MM-dd'),
        birthHour: formState.birthHour,
        gender: formState.gender as 'male' | 'female',
        namXem: new Date().getFullYear(),
      };
      const result = await generateProfile(birthInputData);
      // M4: Store input for retry on processing error
      sessionStorage.setItem('tuvi_last_input', JSON.stringify(birthInputData));
      router.push(`/processing/${result.profileId}`);
    } catch (err) {
      setErrors({ submit: err instanceof Error ? err.message : 'Có lỗi xảy ra. Vui lòng thử lại.' });
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      {/* Form header */}
      <div className="mb-6">
        <h1 className="text-[18px] font-semibold text-text-primary">
          Nhập thông tin ngày sinh
        </h1>
        <p className="text-xs text-text-tertiary mt-1">
          Tất cả thông tin được mã hóa và bảo mật
        </p>
      </div>

      <div className="flex flex-col gap-5">
        {/* Name field -- optional */}
        <div className="flex flex-col gap-1.5">
          <label htmlFor="name" className="text-[13px] font-medium text-text-primary flex items-center">
            Họ tên
            <span className="text-[11px] text-text-tertiary bg-bg-subtle px-1.5 py-0.5 rounded ml-2">
              Không bắt buộc
            </span>
          </label>
          <input
            id="name"
            type="text"
            placeholder="Nguyễn Văn A"
            maxLength={100}
            value={formState.name}
            onChange={(e) => setFormState((s) => ({ ...s, name: e.target.value }))}
            className="w-full h-12 border border-border rounded-[6px] px-3 text-sm
              text-text-primary bg-bg-surface placeholder:text-text-tertiary
              focus:outline-none focus:border-border-focus focus:ring-1 focus:ring-border-focus"
          />
          <p className="text-xs text-text-tertiary">
            Dùng trong luận giải để cá nhân hóa nội dung.
          </p>
        </div>

        {/* Date field */}
        <DatePickerField
          value={formState.birthDate}
          onChange={(date) => setFormState((s) => ({ ...s, birthDate: date }))}
          error={errors.birthDate}
        />

        {/* Hour field */}
        <div className="flex flex-col gap-1.5">
          <label className="text-[13px] font-medium text-text-primary flex items-center">
            Giờ sinh <span className="text-accent ml-0.5">*</span>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger
                  className="ml-1.5 cursor-help"
                  aria-label="Tại sao cần giờ sinh?"
                >
                  <Info size={15} className="text-text-tertiary" />
                </TooltipTrigger>
                <TooltipContent className="max-w-[280px] text-xs p-3 rounded-[8px]">
                  Giờ sinh xác định Cung Mệnh — yếu tố quan trọng nhất trong Tử Vi Đẩu Số.
                  Nếu không biết chính xác, hãy hỏi cha mẹ hoặc xem sổ khai sinh.
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </label>

          <Select
            value={formState.birthHour || undefined}
            onValueChange={(v) => setFormState((s) => ({ ...s, birthHour: v as string }))}
          >
            <SelectTrigger
              data-error={errors.birthHour ? 'true' : undefined}
              className={`w-full h-12 text-sm rounded-[6px]
                ${errors.birthHour ? 'border-red-400' : 'border-border'}`}
            >
              <SelectValue placeholder="Chọn giờ sinh" />
            </SelectTrigger>
            <SelectContent>
              {BIRTH_HOURS.map((h) => (
                <SelectItem key={h.value} value={h.value} className="py-2.5 text-sm">
                  {h.label} ({h.range})
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {errors.birthHour && (
            <p className="flex items-center gap-1 text-xs text-red-500 mt-0.5">
              <AlertCircle size={14} />
              {errors.birthHour}
            </p>
          )}
        </div>

        {/* Gender field */}
        <fieldset className="flex flex-col gap-1.5">
          <legend className="text-[13px] font-medium text-text-primary mb-1.5">
            Giới tính <span className="text-accent">*</span>
          </legend>

          <RadioGroup
            value={formState.gender || undefined}
            onValueChange={(v) => setFormState((s) => ({ ...s, gender: v as 'male' | 'female' }))}
            className="flex gap-4 mt-1"
          >
            {[
              { value: 'male', label: 'Nam' },
              { value: 'female', label: 'Nữ' },
            ].map((opt) => (
              <label
                key={opt.value}
                className="flex items-center gap-2 cursor-pointer"
                data-error={errors.gender && !formState.gender ? 'true' : undefined}
              >
                <RadioGroupItem value={opt.value} className="w-5 h-5" />
                <span className="text-sm text-text-primary">{opt.label}</span>
              </label>
            ))}
          </RadioGroup>

          {errors.gender && (
            <p className="flex items-center gap-1 text-xs text-red-500 mt-0.5">
              <AlertCircle size={14} />
              {errors.gender}
            </p>
          )}
        </fieldset>

        {/* Submit error */}
        {errors.submit && (
          <p className="flex items-center gap-1 text-xs text-red-500">
            <AlertCircle size={14} />
            {errors.submit}
          </p>
        )}

        {/* Submit button */}
        <button
          type="submit"
          disabled={!isFormValid || isSubmitting}
          className={`w-full h-12 rounded-[8px] text-white font-medium text-sm mt-3
            flex items-center justify-center gap-2 transition-colors duration-100
            ${!isFormValid || isSubmitting
              ? 'bg-accent opacity-40 cursor-not-allowed'
              : 'bg-accent hover:bg-accent-hover cursor-pointer'
            }`}
        >
          {isSubmitting ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              Đang xử lý...
            </>
          ) : (
            'Xem luận giải →'
          )}
        </button>

        {/* Privacy note */}
        <p className="flex items-center justify-center gap-1 text-[11px] text-text-tertiary mt-1">
          <Lock size={12} />
          Thông tin ngày sinh không được lưu trữ gắn với danh tính của bạn.
        </p>
      </div>
    </form>
  );
}
