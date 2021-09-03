from django.db import models

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

#
#The Article model is used to hold the results of the analyzer
#A rowis written for each article analyzed and one for the overall results at the feed level
#The database is cleared prior to begining a new run
#

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
#
#The History model contains a summary of the results of each analysis run at the feed level
#The data is persistent and can be viewed via the graphical representation and the feed detail pages
#
class History(models.Model): 
    title = models.CharField(max_length=255, null=True)
    date = models.CharField(max_length=255, null=True)
    word_count = models.IntegerField(null=True)
    positivity_index = models.IntegerField(null=True)
    num_articles = models.IntegerField(null=True)

    def get_absolute_url(self):
        return reverse('article_history', args=[int(self.id)])
            
    def __str__(self):
        return self.title
#
#The Single_history model is used for display purposes and is a temporary storage area
#It is loaded once a graph is selected via click and the data is then displayed in the listview
#
class Single_history(models.Model): 
    title = models.CharField(max_length=255, null=True)
    date = models.CharField(max_length=255, null=True)
    word_count = models.IntegerField(null=True)
    positivity_index = models.IntegerField(null=True)
    num_articles = models.IntegerField(null=True)

    def get_absolute_url(self):
        return reverse('article_history', args=[int(self.id)])
            
    def __str__(self):
        return self.title
