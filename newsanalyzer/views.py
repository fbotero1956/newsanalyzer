from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Article 
from bs4 import BeautifulSoup
import requests
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .analyzer import TextAnalyzer
import itertools


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

    def getRSS(RSS_URL):
        feed = ReadRss(RSS_URL, headers)
   
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
  
class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article_select.html'
    fields = ('title', 'link', )
    success_url = reverse_lazy('article_list')

#   def form_valid(self, form):
#        form.instance.author = self.request.user
#        return super().form_valid(form)

class ArticleAboutView(ListView):
    model = Article
    template_name = "about.html"

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

class ReadRss:
 
    def __init__(self, rss_url, headers):
 
        self.url = rss_url
        self.headers = headers
        try:
            self.r = requests.get(rss_url, headers=self.headers)
            print('self.status_code ', self.r)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', rss_url)
            print(e)
        print('self.status_code ', self)
        try:    
            self.soup = BeautifulSoup(self.r.text, 'html.parser')
        except Exception as e:
            print('Could not parse the xml: ', self.url)
            print(e)

        self.articles = self.soup.findAll('item')
        self.num_articles = len(self.articles)
        i = 0
        while i < self.num_articles:
            if self.articles[i] is None:
                print("invalid index is " + str(i))
                self.articles[i] = []
            i += 1
        self.ten_articles = list(itertools.islice(self.articles,4))
        self.articles = self.ten_articles
        # print(self.num_articles)
        # print(len(self.articles))
        try:    
            self.articles_dicts = [{'title':a.find('title').text,'link':a.link.next_sibling.replace('\n','').replace('\t',''),'description':a.find('description').text,'pubdate':a.find('pubdate').text} for a in self.articles]
            self.urls = [d['link'] for d in self.articles_dicts if 'link' in d]
            self.titles = [d['title'] for d in self.articles_dicts if 'title' in d]
            self.descriptions = [d['description'] for d in self.articles_dicts if 'description' in d]
            self.pub_dates = [d['pubdate'] for d in self.articles_dicts if 'pubdate' in d]
        except Exception as e:
            print('Could not parse the article dictionary: ', self.articles)
            print(e)



    if __name__ == '__main__':
 
        feed = ReadRss('https://www.jcchouinard.com/author/jean-christophe-chouinard/feed/', headers)
        # Get list of urls in feed
        print(feed.urls)
        # Get article data as a list of dicts
        print(feed.articles_dicts)
 
        # Show article titles
        print(feed.titles)
        
        # Show descriptions
        print(feed.descriptions)
        
        # Show publication dates
        print(feed.pub_dates)


@csrf_exempt
def rsscall(request):
   #Get the variable text
   text = request.POST['text']
   # print('successful 1 ' + text)
   #Do whatever with the input variable text
   feed = ReadRss(text, headers)
   # Get list of urls in feed
   # print('successful 2')
   if feed:
      print("found " + str(feed.num_articles) + " articles")
      # print list of urls in feed
      # print(feed.urls)
              
      # print article data as a list of dicts
      # print(feed.articles_dicts)
 
      # Show article titles
      # print(feed.titles)
        
      # Show descriptions
      # print(feed.descriptions)
        
      # Show publication dates
      # print(feed.pub_dates)

      # print(len(feed.urls))
      
      i = 0
      while i <= 3:
        print ("****************************")
        print ("****************************")
        cwords = TextAnalyzer(feed.urls[i], "url")
        print ("Title: ", feed.titles[i])
        print ("URL to article: ", feed.urls[i])
        print ("Date published: ", feed.pub_dates[i])
        abstract = list(itertools.islice(feed.descriptions[i], 0, feed.descriptions[i].find('<')))
        listToStr = ''.join([str(elem) for elem in abstract])
        print ("Abstract: ", listToStr)
        # print ("Abstract: ", feed.descriptions[i])


        response = feed.urls[0]

        if cwords.word_count > 0:
            print ("The number of words in the article is: ", cwords.word_count)
            print("distinct word count = ", cwords.distinct_word_count)

            common_words = cwords.common_words(minlen=5, maxlen=12)
            for j in range(5):
                print("The most common word of at least 5 letters in text is: ", common_words[j][0])
            print ("average word length = ", cwords.avg_word_length)
            positivity_score = cwords.calculate_positivity_score()
            
            print("The positivity score is: ", positivity_score)
            print("The positivity index is: ", cwords.positivity)
        i += 1
   else:
       response = 'feed retrival failed'
   #Send the response 

   return HttpResponse(response)

