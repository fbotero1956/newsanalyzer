from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

class Article(models.Model): 
    title = models.CharField(max_length=255, null=True)
    link = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    date = models.CharField(max_length=255, null=True)
    word_count = models.IntegerField(null=True)
    positivity_index = models.IntegerField(null=True)
    record_type = models.IntegerField(null=True)


    

    def get_absolute_url(self):
        return reverse('article_detail', args=[int(self.id)])
            
    def __str__(self):
        return self.title

