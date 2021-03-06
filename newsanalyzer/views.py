from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Article, History, Single_history
from bs4 import BeautifulSoup
import requests
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .analyzer import TextAnalyzer
import itertools
from django.shortcuts import redirect
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import io 
import urllib, base64
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from threading import RLock

thread_control = RLock()

#
#To display the results of the feed analysis
#
class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

    def getRSS(RSS_URL):
        feed = ReadRss(RSS_URL, headers)
#
#Not in use
#
class ArticleHistoryView(ListView):
    model = History
    template_name = 'article_history.html'
#
#To display the history details of a specific feed
#
class FeedHistoryView(ListView):
    model = Single_history
    template_name = 'single_feed_history.html'
#
#Creates a list of the individual feeds, which is used to drive #the graph creation process
#
def history_plotter(request):
        #plot the most common words

    history = History.objects.all()
    print("in plotter function")
    feeds = []
    for a in history:
        if a.title not in feeds:
            feeds.append(a.title)

    feeds_dict = {feeds[i]: i for i in range(0, len(feeds))}

    return render(request, 'feed_history.html', {'data' :  feeds_dict})

#
#Creates the feed history graphs for each feed
#
def history_plotter_graph(request, feed="CNN Top Political Stories RSS"):
   
    # matplotlib needs thread synchronization

    with thread_control:

        history = History.objects.all()
        print("in graph function", feed)
        
        char = []
        count = []
        run = 0
        avg = 0
        for a in history:
            if a.title == feed:
                run += 1
                avg += a.positivity_index
                char.append(run)
                count.append(a.positivity_index)
        avg = avg / run
        avg = round(avg)
        plt.tight_layout()
        if avg > 2:
            f = plt.figure(figsize=(3,3), facecolor='green')
        else:
            if avg < -2:
                f = plt.figure(figsize=(3,3), facecolor='red')
            else:
                f = plt.figure(figsize=(3,3), facecolor='white')
        ax = plt.axes()
        ax.set_facecolor("white")
        plt.title(feed)
        label = "Average: " + str(avg)
        plt.xlabel(label)
        plt.ylabel('Index')
        plt.tight_layout()
        plt.grid(axis = 'y')
        
        #plt.xticks(rotation='vertical')
        # bar1 = plt.plot(h, color='Green',alpha=0.65)
        plt.bar(char, count)

        #plt.savefig(f, bbox_inches='tight')
        canvas = FigureCanvasAgg(f)    
        response = HttpResponse(content_type='image/jpg')
        canvas.print_jpg(response)
        plt.close(f)
        return response
#
#Creates the temporary database with the feed history for th selected feed
#
def single_feed_history(request, feed="CNN Top Political Stories RSS"):
   
    # matplotlib needs thread synchronization

    with thread_control:

        history = History.objects.all()
        print("in single feed history function", feed)
        
        single_hst = Single_history.objects.all()
        single_hst.delete()

        run = 0
        for a in history:
            if a.title == feed:
                run += 1
                single_hst = Single_history(title=a.title, word_count=a.word_count, date=a.date, positivity_index=a.positivity_index, num_articles=a.num_articles)

                single_hst.save()
                

        response = redirect('/newsanalyzer/single_feed_history/')
        return response

#
#Displays the detail statistics for a particular article after analysis
#
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

def some_view(request):
       return redirect(article.link)
#
#allows the user to select an RSS feed to analyze
#
class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article_select.html'
    fields = ('title', 'description', )
    success_url = reverse_lazy('article_list')
#
#displays the about us view
#
class ArticleAboutView(ListView):
    model = Article
    template_name = "about.html"

#
#user agent needed for the RSS url get
#
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
#
# gets the RSS feed and parses it (using beautifulsoup4) for the analyzer to use
#start and end enable control over the number of articles to process
#Heroku has a 30 second thread limit and so a limit of 5 articles has been set
#
class ReadRss:
 
    def __init__(self, rss_url, headers, start, end):
 
        self.ok = False
        self.err = ""
        self.url = rss_url
        self.headers = headers
        try:
            self.r = requests.get(rss_url, headers=self.headers)
            print('self.status_code ', self.r)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', rss_url)
            print(e)
            self.ok=False
            self.err='Error fetching the URL: '
            return 

        print('self.status_code ', self)
        try:    
            self.soup = BeautifulSoup(self.r.text, 'html.parser')
        except Exception as e:
            print('Could not parse the html: ', self.url)
            print(e)
            self.ok=False
            self.err='Could not parse the html: '
            return 

        self.articles = self.soup.findAll('item')
        self.num_articles = len(self.articles)
        # limit the number of articles
        #if self.num_articles <= end:
        #    end = self.num_articles - 1

        i = 0
        while i < self.num_articles:
            if self.articles[i] is None:
                print("invalid index is " + str(i))
                self.articles[i] = []
            i += 1
        while not self.ok:
            self.ok = True
            self.ten_articles = list(itertools.islice(self.articles,start,end))
            self.articles = self.ten_articles
            self.num_articles = len(self.articles)
            #print(self.num_articles)

            try:    
                #print('entering parsing routine')
                self.articles_dicts = [{'title':a.find('title').text,'link':a.link.next_sibling.replace('\n','').replace('\t',''),'description':a.find('description').text,'pubdate':a.find('pubdate').text} for a in self.articles]
                #print('dictionary successfully created')
                self.urls = [d['link'] for d in self.articles_dicts if 'link' in d]
                #print('urls successfully created')
                self.titles = [d['title'] for d in self.articles_dicts if 'title' in d]
                #print('title successfully created')
                self.descriptions = [d['description'] for d in self.articles_dicts if 'description' in d]
                #print('description successfully created')
                self.pub_dates = [d['pubdate'] for d in self.articles_dicts if 'pubdate' in d]
                #print('pub_date successfully created')
            except Exception as e:
                # print('Could not parse the article dictionary: ', self.articles)
                print(e)
                self.ok=False
                self.err='Could not parse the article dictionary: '
                start += 1
        



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

#
#instantiates the class to get the feed and articles
#executes the analyzer on each article and writes the results 
#
@csrf_exempt
def rsscall(request):
   #Get the variable text
   text = request.POST['text']
   desc = request.POST['desc']
   # print('successful 1 ' + text)
   #Do whatever with the input variable text
   articles=Article.objects.all()
   articles.delete()

   start = 0
   end = 5

   total_word_count = 0
   total_tally = 0
   total_positivity = 0
   

   feed = ReadRss(text, headers, start, end)
   # Get list of urls in feed
   # print('successful 2')
   if feed.ok:
      #print("found " + str(feed.num_articles) + " articles")

      i = 0
      #print('length of feed', len(feed.urls))
      #print ('end :', end)
      end = 0
      while i <= len(feed.urls) - 1:
        #print ("****************************")
        #print ("****************************")
        if feed.urls:
            cwords = TextAnalyzer(desc, feed.urls[i], "url")
        
            #print ("Title: ", feed.titles[i])
            #print ("URL to article: ", feed.urls[i])
            #print ("Date published: ", feed.pub_dates[i])
            #print (feed.descriptions[i])
            if desc != 'CNBC Market Insider':
                abstract = list(itertools.islice(feed.descriptions[i], 0, feed.descriptions[i].find('<')))
            else:
                abstract = list(itertools.islice(feed.descriptions[i], 0, len(feed.descriptions[i])))
            listToStr = ''.join([str(elem) for elem in abstract])
            #print ("Abstract: ", listToStr)
            # print ("Abstract: ", feed.descriptions[i])


            response = feed.urls[i]

            if cwords.word_count > 0:
                #print ("The number of words in the article is: ", cwords.word_count)
                #print("distinct word count = ", cwords.distinct_word_count)

                common_words = cwords.common_words(minlen=5, maxlen=12)
                for j in range(5):
                    print("The most common word of at least 5 letters in text is: ", common_words[j][0], "   ", common_words[j][1])
                #print ("average word length = ", cwords.avg_word_length)

                positivity_score = cwords.tally
                
                #print("The positivity score is: ", positivity_score)
                #print("The positivity index is: ", cwords.positivity)

                total_tally += cwords.tally
                total_word_count += cwords.word_count


                article = Article(title=feed.titles[i], link=feed.urls[i], date=feed.pub_dates[i], description=listToStr, word_count=cwords.word_count, positivity_index=cwords.positivity, record_type=1, distinct_word_count=cwords.distinct_word_count, avg_word_length=cwords.avg_word_length, common_words_1=common_words[0][0], common_words_tally_1=common_words[0][1], common_words_2=common_words[1][0], common_words_tally_2=common_words[1][1], common_words_3=common_words[2][0], common_words_tally_3=common_words[2][1], common_words_4=common_words[3][0], common_words_tally_4=common_words[3][1], common_words_5=common_words[4][0], common_words_tally_5=common_words[4][1], pos_tally=cwords.pos_tally, neg_tally=cwords.neg_tally, )
        
                article.save()
                end += 1
        i += 1


   else:
       response = feed.err
   #Send the response 
   if total_word_count > 0:
        total_positivity = round(total_tally / total_word_count * 1000)
        #print("Total number of words: ", total_word_count)
        #print("Total tally: ", total_tally)
        #print("Total positivity Index: ", total_positivity)
        #
        #write feed level stats
        #
        article = Article(title=desc, description="Totals for the entire RSS feed", word_count=total_word_count, positivity_index=total_positivity, record_type=0, num_articles=end)
        article.save()
        #
        # save feed history
        #
        run_date = datetime.now()
        history = History(title=desc, word_count=total_word_count, date=run_date, positivity_index=total_positivity, num_articles=end)
        history.save()
   else:
        response = feed.err
   return HttpResponse(response)

