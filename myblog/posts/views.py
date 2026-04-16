from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from posts.models import Tag, Post
from django.db.models.functions import Substr

def post_list(request):

    tags = Tag.objects.all()
   
    posts = (
        Post.objects
        .order_by('-created_at')
        .defer("body_html")
        .annotate(body_preview=Substr("body_html", 1, 300))
    )

   
    page = int(request.GET.get("page", 1))


    initial_size = 5   # startup posts
    next_size = 2      # posts per scroll request

    if page == 1:
        start = 0
        end = initial_size
    else:
        start = initial_size + (page - 2) * next_size
        end = start + next_size

    current_posts = posts[start:end]
    has_next = posts[end:end+1].exists()
    next_page = page + 1

    context = {
        "site_name": "My Blog",
        "posts_list": current_posts,
        "has_next": has_next,
        "next_page": next_page,
        "tags": tags,
    }

    template_name = "posts_chunk.html" if request.htmx else "posts_list.html"
    return render(request, template_name, context)


def post_view(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)
    tags = Tag.objects.all()
    context = {
        "site_name": "My Blog",
        "post": post,
        "tags": tags,
    }

    return render(request, "post_entry.html", context)


def search_results(request):
    q = request.GET.get('q', '').strip()
    page_number = request.GET.get("page", 1)

    results = Post.objects.filter(
        Q(post_title__icontains=q) | Q(tags__name__icontains=q)
    ).distinct().prefetch_related('tags').order_by('-created_at')
    
    paginator = Paginator(results, 3)
    page_object = paginator.get_page(page_number)
    result_tags = Tag.objects.filter(posts__in=results).distinct()


    context = {
        'site_name': 'My blog',
        'q': q, 
        'tags': result_tags,
        'posts_list': page_object.object_list,
        'has_next': page_object.has_next(),
        'next_page': page_object.next_page_number() if page_object.has_next() else None,
    }
    template_name = "posts_chunk.html" if request.htmx else "search_results.html"
    return render(request, template_name, context)

def tag_results(request, tag: str):
    page_number = request.GET.get("page", 1)
    tag_obj = get_object_or_404(Tag, name__iexact=tag)

    results = (
        Post.objects.filter(tags=tag_obj)
        .prefetch_related("tags")
        .order_by("-created_at")
        .defer("body_html")
        .annotate(body_preview=Substr("body_html", 1, 300))
    )
    paginator = Paginator(results, 3)
    page_object = paginator.get_page(page_number)
    tags_list = Tag.objects.all()

    context = {
        "site_name": "My blog",
        "tag": tag_obj.name,
        "tags": tags_list,
        "posts_list": page_object.object_list,
        "has_next": page_object.has_next(),
        "next_page": page_object.next_page_number() if page_object.has_next() else None,
    }

    template_name = "posts_chunk.html" if request.htmx else "tag_results.html"
    
    return render(request, template_name, context)
