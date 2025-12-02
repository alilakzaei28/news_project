from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Post, Category
from .forms import CommentForm

# --- صفحه اصلی ---
def home(request):
    # ۱. همه خبرهای منتشر شده
    all_posts = Post.objects.filter(status='published').order_by('-created_at')

    # ۲. خبر ویژه (بزرگ وسط): اولین خبر لیست
    main_post = all_posts.first()

    # ۳. منتخب اخبار (کناری): خبرهای دوم تا چهارم (۳ تا)
    selected_posts = all_posts[1:4]

    # ۴. آخرین اخبار (ستون راست): ۱۰ خبر آخر
    latest_news = all_posts[:10]

    # ۵. پربیننده‌ترین‌ها (ستون چپ): مرتب‌سازی بر اساس بازدید
    trending_posts = Post.objects.filter(status='published').order_by('-views')[:10]

    # ۶. چندرسانه‌ای (پایین صفحه): فقط خبرهایی که ویدیو دارند
    videos = Post.objects.filter(status='published').exclude(video='').order_by('-created_at')[:4]

    # ۷. یادداشت‌ها
    try:
        notes = Post.objects.filter(category__name='یادداشت', status='published')[:5]
    except:
        notes = []

    context = {
        'main_post': main_post,
        'selected_posts': selected_posts,
        'latest_news': latest_news,
        'trending': trending_posts,
        'videos': videos,
        'notes': notes,
    }
    
    return render(request, 'core/home.html', context)


# --- صفحه جزئیات خبر (با نظرات) ---
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # خبرهای مرتبط: هم‌دسته باشند، منتشر شده باشند، خود خبر فعلی نباشند (exclude)
    # ۳ تا خبر جدیدتر را بگیر
    related_posts = Post.objects.filter(
        category=post.category, 
        status='published'
    ).exclude(id=post.id).order_by('-created_at')[:3]

    # لیست نظرات تایید شده
    comments = post.comments.filter(active=True)
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    post.views += 1
    post.save()

    return render(request, 'core/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'related_posts': related_posts # <--- این را حتما اضافه کنید
    })

# --- صفحه جستجو ---
def search(request):
    query = request.GET.get('q')
    results = []
    
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        )
    
    return render(request, 'core/search.html', {'query': query, 'results': results})


# --- صفحه دسته‌بندی (با صفحه‌بندی/Pagination) ---
def category_detail(request, name):
    category = get_object_or_404(Category, name=name)
    
    # همه خبرهای این دسته
    all_posts = Post.objects.filter(category=category, status='published').order_by('-created_at')
    
    # تنظیمات صفحه‌بندی (6 خبر در هر صفحه)
    paginator = Paginator(all_posts, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # سایدبار (پربازدیدها)
    trending_posts = Post.objects.filter(status='published').order_by('-views')[:5]

    return render(request, 'core/category.html', {
        'category': category,
        'posts': page_obj,
        'trending': trending_posts
    })


# --- صفحه درباره ما ---
def about(request):
    return render(request, 'core/about.html')