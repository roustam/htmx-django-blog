from django.contrib import admin
from django.urls import path, include
from posts.views import post_list, search_results, tag_results

urlpatterns = [
    path("", post_list, name="sample_view"),
    path("posts/", include("posts.urls")),
    path("tags/<str:tag>/", tag_results, name="tag_results"),
    path("search/", search_results, name="search_results"),
    path("admin/", admin.site.urls),
]
