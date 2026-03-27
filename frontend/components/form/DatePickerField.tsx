'use client';
import { useState } from 'react';
import { format } from 'date-fns';
import { vi } from 'date-fns/locale';
import { Calendar as CalendarIcon, ChevronDown, AlertCircle } from 'lucide-react';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { Calendar } from '@/components/ui/calendar';

interface DatePickerFieldProps {
  value: Date | undefined;
  onChange: (date: Date | undefined) => void;
  error?: string;
}

export default function DatePickerField({ value, onChange, error }: DatePickerFieldProps) {
  const [open, setOpen] = useState(false);
  const currentYear = new Date().getFullYear();

  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-[13px] font-medium text-text-primary">
        Ngày sinh <span className="text-accent">*</span>
      </label>

      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger
          data-error={error ? 'true' : undefined}
          className={`w-full h-12 flex items-center gap-2 px-3 text-sm text-left
            border rounded-[6px] bg-bg-surface transition-colors duration-100
            focus:outline-none focus:ring-1 focus:ring-border-focus focus:border-border-focus
            ${error
              ? 'border-red-400 focus:border-red-500 focus:ring-red-400'
              : 'border-border hover:border-gray-300'
            }`}
        >
          <CalendarIcon size={16} className="text-text-tertiary flex-shrink-0" />
          <span className={`flex-1 ${value ? 'text-text-primary' : 'text-text-tertiary'}`}>
            {value ? format(value, 'dd/MM/yyyy') : 'Chọn ngày sinh'}
          </span>
          <ChevronDown size={16} className="text-text-tertiary flex-shrink-0" />
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            mode="single"
            selected={value}
            onSelect={(date) => {
              onChange(date);
              setOpen(false);
            }}
            startMonth={new Date(1920, 0)}
            endMonth={new Date(currentYear, 11)}
            captionLayout="dropdown"
            showOutsideDays={false}
            locale={vi}
            className="rounded-[8px]"
          />
        </PopoverContent>
      </Popover>

      {error && (
        <p className="flex items-center gap-1 text-xs text-red-500 mt-0.5">
          <AlertCircle size={14} />
          {error}
        </p>
      )}
    </div>
  );
}
