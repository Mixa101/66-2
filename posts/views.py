from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
)
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from posts.form import PostEditForm, PostForm
from posts.models import Comment, Post


def home(request):
    return HttpResponse("<h1>Hello world!</h1>")


def about(request):
    name = "Islam"
    age = 22
    nickname = "orewaisa"

    response = f"<h1>{name}</h1> <br> <h2>{age}</h2> <p>{nickname}</p>"

    return HttpResponseBadRequest(response)


# def post_list(request: HttpRequest):

#     posts = Post.objects.filter().select_related("user")

#     if search := request.GET.get("search", None):
#         posts = posts.filter(title__icontains=search)

#     post_count = posts.count
#     posts = posts.all
#     context_obj = {"posts": posts, "count": post_count}

#     return render(request, "posts/post_list.html", context_obj)


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/post_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        posts_count = context["posts"].count
        for post in context["posts"]:
            print(post.title_rate)
        context["count"] = posts_count

        return context

    def get_queryset(self) -> QuerySet[Any]:
        qs = (
            Post.objects.all()
            .select_related("user")
            .prefetch_related("comments", "comments__user")
        )
        if search := self.request.GET.get("search", None):
            qs = qs.filter((Q(title__icontains=search) | Q(content__icontains=search)))

        return qs


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


@login_required
def my_posts(request: HttpRequest):
    user = request.user

    posts = (
        Post.objects.filter(user=user)
        .select_related("user")
        .prefetch_related("comments")
        .all()
    )
    if search := request.GET.get("search", None):
        posts = posts.filter(title__icontains=search)

    post_count = posts.count()
    return render(
        request, "posts/post_list.html", context={"posts": posts, "count": post_count}
    )


# def post_detail(request: HttpRequest, pk):
#     post = (
#         Post.objects.select_related("user")
#         .prefetch_related("comments", "comments__user")
#         .get(id=pk)
#     )
#     return render(request, "posts/post_detail.html", context={"post": post})
class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post_detail.html"

    def get_object(self, queryset: QuerySet[Any] | None = None) -> Post:
        qs = queryset
        if queryset:
            qs = queryset.prefetch_related("comments", "comments__user").select_related(
                "user"
            )
        return super().get_object(qs)


# @login_required
# def post_edit(request: HttpRequest, pk):
#     post = Post.objects.select_related("user").get(id=pk)

#     user = request.user

#     if post.user != user:
#         return render(request, "posts/post_detail.html", context={"post": post})

#     if request.method.lower() == "post":
#         form = PostEditForm(request.POST, request.FILES)

#         if form.is_valid():
#             cleaned_data = form.cleaned_data

#             if title := cleaned_data.get("title"):
#                 post.title = title
#             if content := cleaned_data.get("content"):
#                 post.content = content

#             if rate := cleaned_data.get("rate"):
#                 post.rate = rate

#             if image := cleaned_data.get("image"):
#                 post.image = image

#             post.save()

#             return redirect("post_detail", pk=post.pk)

#     return render(request, "posts/post_edit.html", context={"post": post})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    # fields = ["title", "content", "rate", "image"]
    template_name = "posts/post_edit.html"
    success_url = reverse_lazy("post_list")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)

        return HttpResponseRedirect(
            reverse("post_detail", kwargs={"pk": self.kwargs["pk"]})
        )


class CreateCommentGenericView(CreateView):
    model = Comment
    fields = ["content"]
    success_url = reverse_lazy("post_list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        post = Post.objects.get(id=self.kwargs["pk"])
        form.instance.post = post
        if self.request.user.is_anonymous:
            form.instance.user = None
        else:
            form.instance.user = self.request.user
        form.instance.save()
        return super().form_valid(form)

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        response = super().post(request, *args, **kwargs)

        return HttpResponseRedirect(
            reverse("post_detail", kwargs={"pk": self.kwargs["pk"]})
        )


class DeletePostView(DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
