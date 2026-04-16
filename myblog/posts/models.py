from typing import Any

from django.db import models
from django.utils.text import slugify
from django_prose_editor.fields import ProseEditorField


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    extensions_config: dict[str, Any] = {
    "Bold": True,
    "Italic": True,
    "Link": True,
    "Caption":True,
    "Image":True,
    "BulletList": True,
    "OrderedList": True,
    "ListItem": True, # Used by BulletList and OrderedList
    "Blockquote": True,
    "History": True,       # Enables undo/redo
    "HTML": True,          # Allows HTML view
    "Typographic": True,   # Enables typographic chars
    "Heading": {
    "levels": [1, 2, 3]},

}
    post_title = models.CharField(max_length=255, unique=True, blank=True)
    post_slug = models.SlugField(max_length=255, unique=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    body_html =  ProseEditorField(extensions=extensions_config, sanitize=True) # pyright: ignore[reportCallIssue]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.post_title
    
    def save(self, *args, **kwargs):
        if not self.post_slug:
            self.post_slug = self._generate_unique_slug()
        super().save(*args, **kwargs)


    
    def _generate_unique_slug(self):
        base_slug = slugify(self.post_title)[:240] or "post"
        slug = base_slug
        i = 2
        while Post.objects.filter(post_slug=slug).exclude(pk=self.pk).exists():
            suffix = f"-{i}"
            slug = f"{base_slug[:255-len(suffix)]}{suffix}"
            i += 1
        return slug





