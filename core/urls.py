from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/<slug:slug>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
    path('category/<str:name>/', views.category_detail, name='category_detail'),
    path('about/', views.about, name='about'),
]