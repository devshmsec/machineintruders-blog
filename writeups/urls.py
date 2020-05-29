from django.urls import path
from . import views
from urllib.parse import unquote

# url = "blogs/<int:id>/<slug:slug>/%23like"

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/<int:id>/<slug:slug>/', views.detail, name='detail'),
    path('blogs/<int:id>/<slug:slug>/like', views.like, name='like'),
    path('accounts/profile/', views.profile, name='profile')
]
