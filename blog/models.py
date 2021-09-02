from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()
    user_id = models.IntegerField(default=0)
    user_name = models.CharField(max_length=150, default="")
