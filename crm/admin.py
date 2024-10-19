from django.contrib import admin
from .models import Task, Observers, Performers

admin.site.register(Performers)

admin.site.register(Observers)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'performer', 'deadline', 'creator')
    list_filter = ('status', 'performer', 'creator')
    search_fields = ('title', 'description')