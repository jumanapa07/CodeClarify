# models.py
from django.db import models
from django.contrib.auth.models import User
from django import forms
class CodeSnippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=100)
    code = models.TextField(forms.Textarea)
    created_at = models.DateField(auto_now_add=True)
    # tags = models.CharField(max_length=255, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title
