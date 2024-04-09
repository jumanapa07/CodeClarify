from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Problem, TestCase, CodeSnippet, Submission
from django.db.models import Count
from django import forms  # Import forms module

# Define an inline for displaying submissions related to a user
class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 0

        
# Custom User admin class
class CustomUserAdmin(UserAdmin):
    inlines = [SubmissionInline]
    list_display = ('username', 'email', 'get_total_submissions')  # Add the 'get_total_submissions' method to display total submissions

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Annotate each user with the total number of submissions
        queryset = queryset.annotate(total_submissions=Count('submission'))
        queryset = queryset.filter(is_staff=False)
        return queryset

    def get_total_submissions(self, obj):
        return obj.total_submissions
    get_total_submissions.short_description = 'Total Submissions'  # Set the column header name

# Register the custom User admin class
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 3

class ProblemAdmin(admin.ModelAdmin):
    inlines = [TestCaseInline]
    list_display = ('title', 'description')
    search_fields = ('title',)

class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'user', 'created_at')
    search_fields = ('title', 'language', 'user__username')
    list_filter = ('language', 'user')

admin.site.register(Problem, ProblemAdmin)
admin.site.register(CodeSnippet, CodeSnippetAdmin)
