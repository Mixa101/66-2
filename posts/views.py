from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render


def home(request):
    return HttpResponse("<h1>Hello world!</h1>")


def about(request):
    name = "Islam"
    age = 22
    nickname = "orewaisa"

    response = f"<h1>{name}</h1> <br> <h2>{age}</h2> <p>{nickname}</p>"

    return HttpResponseBadRequest(response)


def test(request):
    post = {
        "title": "POST #1",
        "content": "Lorem ipsum dolor dasdas",
        "rate": 5,
        "comments": ["Good post", "отстойный пост", "dasdasda"],
    }

    return render(request, "index.html", context={"post": post})
