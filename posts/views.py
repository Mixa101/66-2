from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

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
    q = request.GET.get("q", None)

    posts = Post.objects.filter()

    if q:
        posts = posts.filter(title__icontains=q)

    post_count = posts.count()

    context_obj = {"posts": posts, "count": post_count}

    return render(request, "posts/post_list.html", context_obj)
