from django.urls import path

from posts.views import post_view

urlpatterns = [
    path("<slug:post_slug>/", post_view, name="post_view"),
]
