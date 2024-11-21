# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.login_view, name='login'),
    path('contact/', views.ContactMessageView.as_view(), name='contact'),
    path('blog/', views.BlogPostListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog_detail'),
    path('about/', views.about_view, name='about'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('profile/', views.profile, name='profile'),
]
