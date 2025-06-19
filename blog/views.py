from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import F
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm, CommentForm
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .utils import truncate_string

def create_page_obj(request, posts, posts_per_page=3):
    p = Paginator(posts, posts_per_page)
    page = request.GET.get("page", 1)
    page_obj = p.page(page)
    page_obj.elided_page_range = p.get_elided_page_range(number=page)
    return page_obj
 
def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag_name = None
    if tag_slug:
        tag = Tag.objects.filter(slug=tag_slug).first()
        if tag:
            tag_name = tag.name
            posts = Post.objects.filter(tags__slug__in=[tag_slug])
    
    page_obj = create_page_obj(request, posts, 3)
    return render(request, "blog/index.html", {"page_obj": page_obj, "tag_name": tag_name})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.all()
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to post a comment.")
            return redirect(request.get_full_path())  # or another view like "post_detail"
        form = CommentForm(data=request.POST)
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    else:
        form = CommentForm()
    return render(request, "blog/post_detail.html", {"post": post, "comments": comments, "form": form})

def post_search(request):
    if "query" in request.GET:
        query = request.GET.get("query")
        posts = Post.objects.annotate(
            title_similarity = TrigramSimilarity("title", query),
            body_similarity = TrigramSimilarity("body", query),
            combined_similarity = F("title_similarity") + F("body_similarity")
        ).filter(combined_similarity__gt=0.1)
        return render(request, "blog/search.html", {"posts": posts})

@login_required
def post_create(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        # ...
    else:
        form = CreatePostForm()
    
    return render(request, "blog/create_post.html", {"form": form})



def add_in_read_later(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(id=post_id)
    post.read_later_users.add(request.user)
    
    return JsonResponse({"post_title": truncate_string(post.title)})

def read_later(request):
    read_later_posts = request.user.read_later_posts.all()
    page_obj = create_page_obj(request, read_later_posts, 3)
    return render(request, "blog/read_later.html", {"page_obj": page_obj, "show_read_later_icon": False})