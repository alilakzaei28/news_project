from django.contrib import admin
from .models import Category, Post, Comment

# ۱. ثبت مدل دسته‌بندی (فقط یک بار)
admin.site.register(Category)

# ۲. ثبت و تنظیمات مدل خبر
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'created_at', 'views')
    list_filter = ('status', 'created_at', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    # تنظیم چیدمان فیلدها در صفحه ویرایش
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'status', 'lead', 'content'),
        }),
        ('تنظیمات پیشرفته', {
            'fields': ('author', 'image', 'video', 'views'),
        }),
    )

# ۳. ثبت و تنظیمات مدل نظرات
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('name', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)