from django.contrib import admin
from .models import Problem, TestCase, CodeSnippet

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
