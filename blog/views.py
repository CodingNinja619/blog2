from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import F


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    if tag_slug:
        posts = Post.objects.filter(tags__slug__in=[tag_slug])
    p = Paginator(posts, 3)
    page = request.GET.get("page", 1)
    page_obj = p.page(page)
    page_obj.elided_page_range = p.get_elided_page_range(number=page)
    return render(request, "blog/index.html", {"posts": posts, "page_obj": page_obj, "tag_slug": tag_slug})



def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render(request, "blog/post_detail.html", {"post": post})

def post_search(request):
    if "query" in request.GET:
        query = request.GET.get("query")
        posts = Post.objects.annotate(
            title_similarity = TrigramSimilarity("title", query),
            body_similarity = TrigramSimilarity("body", query),
            combined_similarity = F("title_similarity") + F("body_similarity")
        ).filter(combined_similarity__gt=0.1)
        return render(request, "blog/search.html", {"posts": posts})
