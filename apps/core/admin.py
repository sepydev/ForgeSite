from .models import WebsitePage, Widget

from django.contrib import admin


@admin.register(WebsitePage)
class WebsitePageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "slug")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
