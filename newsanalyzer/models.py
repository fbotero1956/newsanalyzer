from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

class Article(models.Model): 
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
        )

    def get_absolute_url(self):
        return reverse('article_detail', args=[int(self.id)])
            
    def __str__(self):
        return self.title

