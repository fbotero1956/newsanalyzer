from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

class Article(models.Model): 
    title = models.CharField(max_length=255, null=True)
    link = models.URLField(null=True)
    description = models.CharField(max_length=255, null=True)
    date = models.CharField(max_length=255, null=True)
    word_count = models.IntegerField(null=True)
    positivity_index = models.IntegerField(null=True)
    record_type = models.IntegerField(null=True)
    num_articles = models.IntegerField(null=True)
    distinct_word_count = models.IntegerField(null=True)
    avg_word_length = models.IntegerField(null=True)
    pos_tally = models.IntegerField(null=True)
    neg_tally = models.IntegerField(null=True)
    common_words_1 = models.CharField(max_length=25, null=True)
    common_words_tally_1 = models.IntegerField(null=True)
    common_words_2 = models.CharField(max_length=25, null=True)
    common_words_tally_2 = models.IntegerField(null=True)
    common_words_3 = models.CharField(max_length=25, null=True)
    common_words_tally_3 = models.IntegerField(null=True)
    common_words_4 = models.CharField(max_length=25, null=True)
    common_words_tally_4 = models.IntegerField(null=True)
    common_words_5 = models.CharField(max_length=25, null=True)
    common_words_tally_5 = models.IntegerField(null=True)

    def get_absolute_url(self):
        return reverse('article_detail', args=[int(self.id)])
            
    def __str__(self):
        return self.title

