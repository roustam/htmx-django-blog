from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import Substr
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from posts.models import Post, Tag


def post_list(request):

    page = int(request.GET.get("page", 1))
    tags = Tag.objects.all()
   
    posts = (
        Post.objects
        .order_by('-created_at')
        .defer("body_html")
        .annotate(body_preview=Substr("body_html", 1, 300))
    )

    paginator = Paginator(posts, 3)
    page_object = paginator.get_page(page)


    
    context = {
        "posts_list": page_object.object_list,
        "has_next": page_object.has_next,
        "next_page": page_object.next_page_number() if page_object.has_next() else None,
        "next_url": "?" + urlencode({'page': page_object.next_page_number()}) if page_object.has_next() else None,
        "tags": tags,
    }

    template_name = "base.html"
    return render(request, template_name, context)


def post_view(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)
    tags = Tag.objects.all()
    context = {
        "post": post,
        "tags": tags,
    }

    return render(request, "post_entry.html", context)


def search_results(request):
    q = request.GET.get('q', '').strip()

    if not q:
        raise Http404("No search query provided.")

    page_number = request.GET.get("page", 1)

    results = (
        Post.objects.filter(Q(post_title__icontains=q) | Q(tags__name__icontains=q) | Q(body_html__icontains=q))
        .distinct()
        .prefetch_related("tags")
        .order_by("-created_at")
        .defer("body_html")
        .annotate(body_preview=Substr("body_html", 1, 300))
    )
    
    paginator = Paginator(results, 3)
    page_object = paginator.get_page(page_number)
    result_tags = Tag.objects.filter(posts__in=results).distinct()


    context = {
        'q': q, 
        'tags': result_tags,
        'posts_list': page_object.object_list,
        'has_next': page_object.has_next(),
        'next_page': page_object.next_page_number() if page_object.has_next() else None,
        'next_url': (
            f"{reverse('search_results')}?{urlencode({'q': q, 'page': page_object.next_page_number()})}"
            if page_object.has_next()
            else None
        ),
    }
    template_name = "base.html"
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
        "tag": tag_obj.name,
        "tags": tags_list,
        "posts_list": page_object.object_list,
        "has_next": page_object.has_next(),
        "next_page": page_object.next_page_number() if page_object.has_next() else None,
        "next_url": (
            f"{reverse('tag_results', kwargs={'tag': tag_obj.name})}?{urlencode({'page': page_object.next_page_number()})}"
            if page_object.has_next()
            else None
        ),
    }

    template_name = 'base.html'
    
    return render(request, template_name, context)
