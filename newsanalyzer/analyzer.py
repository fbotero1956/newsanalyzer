# 
# Text Analyzer, written by Felipe Botero for Rutgers Python programming course
#

# library imports
import requests, re
from bs4 import BeautifulSoup
from lxml import html
from urllib.request import urlopen
from collections import Counter
import statistics as stats
import string

#main class definition
class TextAnalyzer():
    # validate that the src_type and the src match
    def validate_src_type(self, src, src_type):  
            #if url then the src string must start with http
            if src_type == "url":
                txt = src
                x = re.search("^http.", txt)
                if x:
                    #print('valid url provided')
                    return x
                else:
                    print('invalid url')
                    return x
            # if path then the file extension should be txt
            if src_type == "path":
                txt = src
                x = re.search("txt$", txt)
                #print("search result ", x)
                if x != "None":
                    #print('valid path provided')
                    return x
                else:
                    print('invalid path')
                    return x
            #if text then the src should be a valid string
            if src_type == "text":
                txt = src
                x = isinstance(txt, str)
                if x:
                    #print('valid text provided')
                    return x
                else:
                    print('invalid text')
                    return x
            # if there is a value and it is not url, path or text then raise an error
            else:
                print('invalid parameter passed')
                x = False
                return x
   
    # if src_type is not specified then examine the src parameter to determine the type        
    def discover_src_type(self, src):
            txt = src
            #if the string starts with http then assume it is a url
            x = re.search("^http", txt)
            if x:
                d_src_type = "url"
                return d_src_type
            #if the string ends with txt then assume it is a path
            x = re.search("txt$", txt)
            if x:
                d_src_type = "path"
                return d_src_type
            #otherwise if the parameter is a string pass it in
            x = isinstance(txt, str)
            if x:
                d_src_type = "text"
                return d_src_type
            else:
                #if none of the above then raise an error
                print('invalid parameter, must be url, path or string')
                d_src_type = "Error"
                return d_src_type
    
    #sets _content to the text within the "tag" html element
    def set_content_to_tag(self, tag, tag_id=None, content_tag=None):
        response = urlopen(self._src).read()
        
        soup = BeautifulSoup(response, 'html.parser')
        print(soup.title)
        txt = soup.find(id=tag)
        self._orig_content = str(txt) 
        # print(self._orig_content)
        txt = soup.find_all( tag, tag_id)
        for t in txt:
         self._content += str(txt)
        # print("content = ", self._content)
        return 

        #sets _content to the text within the "tag" html element
    def set_MWcontent_to_tag(self, tag, tag_id=None, content_tag=None):
        response = urlopen(self._src).read()
        
        soup = BeautifulSoup(response, 'html.parser')
        print(soup.title)
        txt = soup.find(tag, tag_id)
        self._orig_content = str(txt) 
        # print(self._orig_content)
        txt = soup.find_all(content_tag)
        for t in txt:
         self._content += str(txt)
        # print("content = ", self._content)
        return 
    
    #reset the content variable when needed
    def reset_content(self):
        self._content = self._orig_content
        return
    
    # convert the content text into a list of words
    def _words(self, casesensitive=False):
        if casesensitive:
            words = self._content.split()
        else:
            words = self._content.upper().split()
        
        words = [word.strip(string.punctuation) for word in words]   
        self._content = words
        return self._content
        
    #determine the word frequency within the text
    def common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False):
        counts = dict()
        words = self._words(casesensitive=casesensitive)

        for word in words:
            if len(word) >= minlen and len(word) <= maxlen and word.isalpha():
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
       
        tmp_words = Counter(counts)
        com_words = tmp_words.most_common(count)
        return com_words
    
    #determine the character frequency
    def char_distribution(self, casesensitive=False, letters_only=False):
        counts = dict()
        
        chars = self._content
        if not casesensitive:
            chars = self._content.upper()

        for char in chars:
            if char.isalpha():
                if char in counts:
                    counts[char] += 1
                else:
                    counts[char] = 1
        #print("char counts = ", counts)
        sort_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return sort_counts

    # calculate the positivity score
    def calculate_positivity_score(self):
        tally = 0
        tallyPos = 0
        tallyNeg = 0
        p = open('positive.txt', "r")        
        pos = p.read().split()
        
        n = open('negative.txt', "r")
        neg = n.read().split()
        for word in self.words:
            if word in pos:
                tally += 1
                tallyPos += 1
            else:
                if word in neg:
                    tally -= 1
                    tallyNeg += 1
        print("tallyPos: ", tallyPos)
        print("tallyNeg: ", tallyNeg)
        self.pos_tally = tallyPos
        self.neg_tally = tallyNeg
        return tally

        
    def __init__(self, desc, src, src_type='none'):
        #src_type will specify discover, url, path, text
        #validate src to start with http and end with txtig_content
        #print ('First step', src_type)
        #print('path = ', src)
        self._src = src
        if not src_type == 'none':                         
            x = self.validate_src_type(src, src_type)
        if not src_type == 'none':
            if x:
                self._src_type = src_type
            else:
                print ('Error in src_type validation')
                return src_type
        else:
            d_src_type = self.discover_src_type(src)
            if not d_src_type == "Error":
                self._src_type = d_src_type
            else:
                print ('Error in src_type discovery')
                return d_src_type
        
        # initialize the properties
        if self._src_type == "path":
            p = open(src, "r")
        #   print('file is open')
            self._content = p.read()
        #   print('file is read')
            self._orig_content = self._content
        #   print(self._content)
        elif self._src_type == "text":
            self._content = src
            self._orig_content = self._content
        elif self._src_type == "url":
            self._content = ""
            #
            # may need to vary this line based on rss feed
            #
            if desc == 'CNN Top Political Stories RSS':
               self.set_content_to_tag(tag="div", tag_id="zn-body__paragraph", content_tag='p')

            if desc == 'CNN Top Stories RSS':
               self.set_content_to_tag(tag="div", tag_id="zn-body__paragraph", content_tag='p')

            if desc == 'CNBC Market Insider':
               self.set_MWcontent_to_tag(tag="div", tag_id="ArticleBody-articleBody", content_tag='p')

            if desc == 'MarketWatch Top Stories RSS':
               self.set_MWcontent_to_tag(tag="div", tag_id="js-article-body", content_tag='p')

            # print("here is the content:")
            # print(self._content)
            self._orig_content = self._content
        else:
            print('Error in src_type')
        #   print("content = ", self._content)
        words = self._words(casesensitive=True)
        # print("back from words", words)
        self.word_count = len(words)
        #print("number of words = ", self.word_count)
        if self.word_count == 0:
            print("no content found please try again later")
            return

        words_length = 0
        for word in words:
            words_length += len(word)
            
        self.avg_word_length = round(words_length / self.word_count, 2) 
        # print ("average word length = ", self.avg_word_length)
        self.reset_content()
        self.distinct_word_count = 0
        words_upper = self._words(casesensitive=False)
        # print ("uppercase = ", words_upper)
        self.words = words_upper
        wcounts = []
        for word in words_upper:
            if not word in wcounts:
                wcounts.append(word)
                self.distinct_word_count += 1
        #print("distinct word count = ", self.distinct_word_count)
        self.tally = self.calculate_positivity_score()
        #print ("Tally = ", tally)
        self.positivity = round(self.tally / self.word_count * 1000)
        #print("positivity index = ", self.positivity)
        self.reset_content()
        self._cwords = self.common_words()
        #self.plot_common_words()
        self.reset_content()
        self._cchars= self.char_distribution()
        #self.plot_char_distribution()

