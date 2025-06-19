from django.shortcuts import redirect

def blog_redirect(request):
    return redirect("blog:post_list")