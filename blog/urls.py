"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from posts.views import (
    CreateCommentGenericView,
    DeletePostView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    about,
    home,
    my_posts,
    post_create,
)
from users.views import login_view, register_view

urlpatterns = [
    path("admin", admin.site.urls),
    path("", home),
    path("about/", about, name="about"),
    path("posts/", PostListView.as_view(), name="post_list"),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post_detail"),
    path("posts/create", post_create, name="post_create"),
    path("posts/edit/<int:pk>", PostUpdateView.as_view(), name="post_edit"),
    path("posts/my_posts", my_posts, name="my_posts"),
    path(
        "posts/<int:pk>/comment", CreateCommentGenericView.as_view(), name="add_comment"
    ),
    path("user/login/", login_view, name="login"),
    path("user/register/", register_view, name="register"),
    path("posts/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
