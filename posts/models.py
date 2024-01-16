from django.db import models


# Create your models here.


class Post(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    rate = models.FloatField(default=0.0)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    price = models.PositiveIntegerField(null=True)
    url = models.URLField(null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text} -> {self.post.title}'
