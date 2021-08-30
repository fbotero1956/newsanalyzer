
​
# library imports
import requests, re
from bs4 import BeautifulSoup
from lxml import html
from urllib.request import urlopen
from collections import Counter
import statistics as stats
import string
import matplotlib.pyplot as plt
import pandas as pd
​
​
#main class definition
class Plotter():
   
    
    #plot the most common words
    def plot_feed_history(self):
        history = self.plot_feed_history
​
        char = []
        count = []
        for a in history:
            char.append(a[0])
            count.append(a[1])
        plt.bar(char, count)
        plt.title("Most common words found in the text")
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.show()
        return
    
​
        
    def __init__(self, src, src_type='none'):
        #src_type will specify discover, url, path, text
        #validate src to start with http and end with txtig_content
        #print ('First step', src_type)
        #print('path = ', src)
        self._src = src
        
        

        character-distribution.png
        common-words.png
        %matplotlib inline
        import numpy as np
        import pandas as pd
        ​
        pd.set_option('display.max_columns', 10)
        pd.set_option('display.max_rows', 10)
        ​
        ta = Plotter()
        ta.plot_feed_history()
        


