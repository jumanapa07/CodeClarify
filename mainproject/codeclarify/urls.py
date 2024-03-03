from .import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.index),
    path('home/',views.home),
    path('loginn/',views.loginn),
    path("register_view/", views.register_view, name="register_view"),
    path('register/',views.user_register),
    path('explore/',views.explore),
    path('explanation/',views.explanation),
    
]