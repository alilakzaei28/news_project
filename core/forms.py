from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        # کلاس‌های Tailwind برای زیبایی فیلدها
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border rounded p-2 mb-4', 'placeholder': 'نام شما'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border rounded p-2 mb-4', 'placeholder': 'ایمیل (نمایش داده نمی‌شود)'}),
            'body': forms.Textarea(attrs={'class': 'w-full border rounded p-2 mb-4', 'rows': 4, 'placeholder': 'نظر خود را بنویسید...'}),
        }