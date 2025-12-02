from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "daily"  # به گوگل می‌گوید روزانه سر بزن
    priority = 0.9        # اولویت خبرها بالاست

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at