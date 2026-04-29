from django.urls import path
from posts.views import post_view, tag_results

urlpatterns = [
    path("<slug:post_slug>/", post_view, name="post_view"),
]
