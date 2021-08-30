from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Article, History
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


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

    def getRSS(RSS_URL):
        feed = ReadRss(RSS_URL, headers)

class ArticleHistoryView(ListView):
    model = History
    template_name = 'article_history.html'

class FeedHistoryView(DetailView):
    model = History
    template_name = 'feed_history.html'

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


def history_plotter_graph(request, feed="CNN Top Political Stories RSS"):
   
    # matplotlib needs thread synchronization

    with thread_control:

        history = History.objects.all()
        print("in graph function", feed)
        
        char = []
        count = []
        run = 0
        for a in history:
            if a.title == feed:
                run += 1
                char.append(run)
                count.append(a.positivity_index)
        #fig = plt.subplots(2,3)
        
        f = plt.figure(figsize=(4,3), edgecolor='red')
        plt.title(feed)
        plt.xlabel('Run')
        plt.ylabel('Index')
        #plt.xticks(rotation='vertical')
        # bar1 = plt.plot(h, color='Green',alpha=0.65)
        plt.bar(char, count)
        canvas = FigureCanvasAgg(f)    
        response = HttpResponse(content_type='image/jpg')
        canvas.print_jpg(response)
        plt.close(f)
        return response

def history_plotter_graph_saved(request, feed):
        #plot the most common words

    history = History.objects.all()
 
    
    char = []
    count = []
    run = 0
    for a in history:
        if a.title == feed:
           run += 1
           char.append(run)
           count.append(a.positivity_index)
    #fig = plt.subplots(2,3)
    plt.bar(char, count)
    plt.title(feed[0])
    plt.xlabel("Run")
    plt.ylabel("Index")
    #plt.show()
    
    fig = plt.gcf()
    #convert graph into string buffer, then 64 bit code into png image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return uri

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

def some_view(request):
       return redirect(article.link)

class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article_select.html'
    fields = ('title', 'description', )
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
            print(self.num_articles)

            try:    
                print('entering parsing routine')
                self.articles_dicts = [{'title':a.find('title').text,'link':a.link.next_sibling.replace('\n','').replace('\t',''),'description':a.find('description').text,'pubdate':a.find('pubdate').text} for a in self.articles]
                print('dictionary successfully created')
                self.urls = [d['link'] for d in self.articles_dicts if 'link' in d]
                print('urls successfully created')
                self.titles = [d['title'] for d in self.articles_dicts if 'title' in d]
                print('title successfully created')
                self.descriptions = [d['description'] for d in self.articles_dicts if 'description' in d]
                print('description successfully created')
                self.pub_dates = [d['pubdate'] for d in self.articles_dicts if 'pubdate' in d]
                print('pub_date successfully created')
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
      print('length of feed', len(feed.urls))
      print ('end :', end)
      end = 0
      while i <= len(feed.urls) - 1:
        print ("****************************")
        print ("****************************")
        if feed.urls:
            cwords = TextAnalyzer(desc, feed.urls[i], "url")
        
            print ("Title: ", feed.titles[i])
            print ("URL to article: ", feed.urls[i])
            print ("Date published: ", feed.pub_dates[i])
            print (feed.descriptions[i])
            if desc != 'CNBC Market Insider':
                abstract = list(itertools.islice(feed.descriptions[i], 0, feed.descriptions[i].find('<')))
            else:
                abstract = list(itertools.islice(feed.descriptions[i], 0, len(feed.descriptions[i])))
            listToStr = ''.join([str(elem) for elem in abstract])
            print ("Abstract: ", listToStr)
            # print ("Abstract: ", feed.descriptions[i])


            response = feed.urls[i]

            if cwords.word_count > 0:
                print ("The number of words in the article is: ", cwords.word_count)
                print("distinct word count = ", cwords.distinct_word_count)

                common_words = cwords.common_words(minlen=5, maxlen=12)
                for j in range(5):
                    print("The most common word of at least 5 letters in text is: ", common_words[j][0], "   ", common_words[j][1])
                print ("average word length = ", cwords.avg_word_length)
                # positivity_score = cwords.calculate_positivity_score()
                positivity_score = cwords.tally
                
                print("The positivity score is: ", positivity_score)
                print("The positivity index is: ", cwords.positivity)

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
        print("Total number of words: ", total_word_count)
        print("Total tally: ", total_tally)
        print("Total positivity Index: ", total_positivity)
        article = Article(title=desc, description="Totals for the entire RSS feed", word_count=total_word_count, positivity_index=total_positivity, record_type=0, num_articles=end)
        article.save()
        #
        # save history
        #
        run_date = datetime.now()
        history = History(title=desc, word_count=total_word_count, date=run_date, positivity_index=total_positivity, num_articles=end)
        history.save()
   else:
        response = feed.err
   return HttpResponse(response)

