import math
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# --- مدل دسته‌بندی ---
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    
    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

# --- مدل اصلی خبرها ---
class Post(models.Model):
    STATUS_CHOICES = (('draft', 'پیش‌نویس'), ('published', 'منتشر شده'))

    title = models.CharField(max_length=200, verbose_name="عنوان خبر")
    slug = models.SlugField(unique=True, verbose_name="آدرس اینترنتی (Slug)")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نویسنده")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="دسته‌بندی")
    
    # لید و ویدیو
    lead = models.TextField(blank=True, null=True, verbose_name="لید (خلاصه خبر)")
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="ویدیو")

    # متن پیشرفته و تصویر هوشمند
    content = RichTextField(verbose_name="متن کامل خبر")
    image = ProcessedImageField(
        upload_to='posts/',
        processors=[ResizeToFill(800, 600)], # برش خودکار به ابعاد 800x600
        format='JPEG',
        options={'quality': 70}, # کاهش حجم عکس
        blank=True,
        null=True,
        verbose_name="تصویر شاخص"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")

    # تنظیمات فارسی‌سازی در پنل ادمین
    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "اخبار"
        ordering = ['-created_at']

    # محاسبه زمان مطالعه
    def reading_time(self):
        word_count = len(self.content.split())
        minutes = math.ceil(word_count / 200)
        return minutes

    def __str__(self):
        return self.title    
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

# --- مدل نظرات ---
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="خبر مربوطه")
    name = models.CharField(max_length=80, verbose_name="نام کاربر")
    email = models.EmailField(verbose_name="ایمیل")
    body = models.TextField(verbose_name="متن نظر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    active = models.BooleanField(default=False, verbose_name="تایید شده")

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات کاربران"
        ordering = ['created_at']

    def __str__(self):
        return f'نظر {self.name} روی {self.post}'