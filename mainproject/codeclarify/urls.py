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
    path('share/',views.share),
    path('snippet_view/<int:id>',views.snippet_view),
    path('language_snippet/<str:language>',views.language_snippet),
    # path('code-explanation/', views.CodeExplanationView.as_view(), name='code_explanation'),

    
    
    
    
    
]