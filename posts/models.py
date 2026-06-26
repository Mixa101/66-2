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
