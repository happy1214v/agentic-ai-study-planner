from django.contrib import admin

from .models import AgentMemory


@admin.register(AgentMemory)
class AgentMemoryAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("task", "user__username")