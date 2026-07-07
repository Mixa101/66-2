from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render

from posts.form import PostForm
from posts.models import Post


def home(request):
    return HttpResponse("<h1>Hello world!</h1>")


def about(request):
    name = "Islam"
    age = 22
    nickname = "orewaisa"

    response = f"<h1>{name}</h1> <br> <h2>{age}</h2> <p>{nickname}</p>"

    return HttpResponseBadRequest(response)


def post_list(request: HttpRequest):

    posts = Post.objects.filter().select_related("user")

    if search := request.GET.get("search", None):
        posts = posts.filter(title__icontains=search)

    post_count = posts.count
    context_obj = {"posts": posts, "count": post_count}

    return render(request, "posts/post_list.html", context_obj)


@login_required
def post_create(request: HttpRequest):
    post_form = PostForm()
    if request.method.lower() == "post":
        post = PostForm(request.POST, request.FILES)
        if post.is_valid():
            post_object = Post(**post.cleaned_data)
            post_object.user = request.user
            post_object.save()
            return redirect("post_list")
        return render(
            request, "posts/post_create.html", context={"errors": post.errors}
        )

    return render(request, "posts/post_create.html", context={"form": post_form})
