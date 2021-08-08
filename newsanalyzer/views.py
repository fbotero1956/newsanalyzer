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
            self.soup = BeautifulSoup(self.r.text, 'lxml')
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
        self.ten_articles = list(itertools.islice(self.articles,2))
        self.articles = self.ten_articles
        print(self.num_articles)
        print(len(self.articles))
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
   print('successful 1 ' + text)
   #Do whatever with the input variable text
   feed = ReadRss(text, headers)
   # Get list of urls in feed
   print('successful 2')
   if feed:
      print("found " + str(feed.num_articles) + " articles")
      # print list of urls in feed
      print(feed.urls)
              
      # print article data as a list of dicts
      # print(feed.articles_dicts)
 
      # Show article titles
      print(feed.titles)
        
      # Show descriptions
      print(feed.descriptions)
        
      # Show publication dates
      print(feed.pub_dates)
      
      cwords = TextAnalyzer(feed.urls[0], "url")
      print ("The number of words in the article is: ", cwords.word_count)
     # cwords = TextAnalyzer('newsanalyzer\pride-and-prejudice.txt', "path")
      myText = '''The outlook wasn't brilliant for the Mudville Nine that day; 
        the score stood four to two, with but one inning more more more more more good good good good good to play.
        And then when Cooney died at first, and Barrows did the same,
        a sickly silence fell upon the patrons of the game.'''
      # cwords = TextAnalyzer(myText, "text")
      response = feed.urls[0]
      if cwords.word_count > 0:
        common_words = cwords.common_words(minlen=4, maxlen=11)
        print("The most common word of at least 3 letters in text is: ", common_words[0][0])
        positivity_score = cwords.calculate_positivity_score()
        print("The positivity score is: ", positivity_score)
        print("The positivity index is: ", cwords.positivity)
        
   else:
       response = 'feed retrival failed'
   #Send the response 

   return HttpResponse(response)

   text = '''The outlook wasn't brilliant for the Mudville Nine that day;
the score stood four to two, with but one inning more to play.
And then when Cooney died at first, and Barrows did the same,
a sickly silence fell upon the patrons of the game.'''
