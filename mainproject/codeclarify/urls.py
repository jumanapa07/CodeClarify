from .import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.index),
    path('home',views.home),
    path('loginn/',views.loginn),
    path("register_view/", views.register_view, name="register_view"),
    path('register/',views.user_register),
    path('explore/',views.explore),
    path('explanation/',views.explanation),
    path('share/',views.share),
    path('snippet_view/<int:id>',views.snippet_view),
    path('language_snippet/<str:language>',views.language_snippet),
    ###coding practice ###
    path('practice/',views.practice),
    path('problem_view/<int:id>',views.problem_view),
    path('challenge/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('compile/<int:challenge_id>', views.compile_code, name='compile_code'),
    path('compile_submit/<int:challenge_id>', views.compile_submit, name='compile_code'),

    path('result/', views.result, name=''),







    
    
    
    
    
]