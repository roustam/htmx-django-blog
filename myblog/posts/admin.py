from django.contrib import admin
from django import forms
from .models import Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id","name",)
    search_fields = ("id", "name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ("id","post_title", "post_slug", "tag_list", "created_at", "updated_at")
    search_fields = ("post_title", "post_slug", "tags__name")
    list_filter = ("tags", "created_at", "updated_at")
    filter_horizontal = ("tags",)

    @admin.display(description="Tags")
    def tag_list(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
