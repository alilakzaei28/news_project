from django import template
import jdatetime

register = template.Library()

# لیست نام ماه‌های فارسی
PERSIAN_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
]

# تابع کمکی برای تبدیل اعداد انگلیسی به فارسی
def translate_to_persian(text):
    english_nums = "0123456789"
    persian_nums = "۰۱۲۳۴۵۶۷۸۹"
    translation_table = str.maketrans(english_nums, persian_nums)
    return str(text).translate(translation_table)

@register.filter
def to_jalali(value):
    if value is None:
        return ""
    
    # تبدیل تاریخ میلادی به شمسی
    jalali_date = jdatetime.datetime.fromgregorian(datetime=value)
    
    # گرفتن نام ماه
    month_name = PERSIAN_MONTHS[jalali_date.month - 1]
    
    # ساخت رشته نهایی (هنوز اعداد انگلیسی هستند)
    date_str = f"{jalali_date.day} {month_name} {jalali_date.year}"
    
    # تبدیل اعداد به فارسی و برگرداندن
    return translate_to_persian(date_str)

@register.simple_tag
def current_jalali_date():
    jalali_date = jdatetime.datetime.now()
    month_name = PERSIAN_MONTHS[jalali_date.month - 1]
    
    date_str = f"{jalali_date.day} {month_name} {jalali_date.year}"
    
    return translate_to_persian(date_str)

# ... کدهای قبلی (translate_to_persian و to_jalali) ...

@register.filter
def fa_num(value):
    """
    این فیلتر هر عدد یا متنی را می‌گیرد و اعدادش را فارسی می‌کند.
    استفاده: {{ post.views|fa_num }}
    """
    if value is None:
        return ""
    return translate_to_persian(str(value))