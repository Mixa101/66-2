from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# CRUD

# C - Create -> 'INSERT INTO table_name (a, b, c) VALUES (1, 2, 3);'

# R - Read -> 'SELECT title, content FROM table_name;'

# U - update -> 'UPDATE table_name SET a = 1;'

# D - Delete -> 'DELETE table_name WHERE id = 1;'


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    rate = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(
        User, models.CASCADE, null=True, blank=True, related_name="posts"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self) -> str:
        return f"{self.title}    {self.pk}"
