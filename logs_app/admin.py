from django.contrib import admin
from .models import * 

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "source", "message", "created_at")
    readonly_fields = ("created_at",)
