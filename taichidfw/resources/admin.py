from django.contrib import admin

from .models import Resource


@admin.register(Resource)
class ResourcesAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "description",
        "visibility",
        "link_type",
        "link",
        "creator",
    ]
