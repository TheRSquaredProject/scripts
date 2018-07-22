import os
import time as pytime
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta

base = "https://www.thedailystar.net/"
numOfDaysToScrape = 8


class Section:
    """ 
    Represents a section for Daily Star i.e. Front Page, Sports etc
    """
    def __init__(self, section_title,articles_raw,date):
        """ 
        Constructor
        
        @param {string} section_title - Title of the section
        @param {[BeautifulSoup obj]} articles_raw - A list of BeautifulSoup obj. Each obj contains all the articles for a section
        @param {string} date - Date of the articles
        """
        self.section_title = section_title
        self.articles_raw = articles_raw
        self.date = date
        
    def writeArticlesToFile(self):
        """ 
        Extracts and transforms each article from BeautifulSoup to an Article obj, then writes the article text to file
        """
        counter = 0
        for article in self.articles_raw:
            try:
                article_title = article.h5.text
                article_url = base + article.a['href']
                article_html = urlopen(article_url)
                article_soup = BeautifulSoup(article_html, 'html.parser')
                articleObj = Article(self.section_title, article_title,article_soup, self.date)
                articleObj.writeToFile()
                counter += 1
            except Exception as e:             
                print(f"Error writing {article_title}")
                print(f"Error message: {e}")
                continue
        
        waitTime = 70
        
        print(f"Wrote {counter} articles to file")
        print(f"Waiting {waitTime} seconds before making new requests...")
        pytime.sleep(waitTime)
        
            

class Article:
    """
    Represents a Daily Star article
    """
    def __init__(self,section_title,article_title,article_content, date):
        """ 
        Constructor
        
         @param {string} section_title - Title of the section
         @param {string} article_title - Title of the article
         @param {BeautifulSoup obj} article_content - A BeautifulSoup obj that encapsulates the contents of the article
         @param {string} date - Date of the articles
        """
        self.section_title = section_title
        self.article_title = article_title
        self.article_content = article_content
        self.date = date
    
    def getSectionTitle(self):
        """ 
        Returns the section_title
        """
        return self.section_title
    
    def getArticleTitle(self):
        """ 
        Returns the aritlce_title
        """
        return self.article_title
    
    def getArticleContent(self):
        """ 
        Returns the article_content
        """
        return self.article_content
    
    def extractText(self):
        """
        Extracts the articles from article_content and transforms it from BeautifulSoup obj to string
        
        @returns Article text in string format
        """
        paras = self.article_content.find('div',attrs={'class':["field-body view-mode-full","field-body"]}).find_all('p')
        text = self._extractParasAndFormText(paras)
        return text
    
    def _extractParasAndFormText(self,paras):
        """
        Extracts the string text from BeautifulSoup paragraphs
        
        @param {BeautifulSoup obj} paras - Contains article text
        @returns Article text in string format
        """
        
        text = "\n ".join([str(para.text) for para in paras])
        return text
    
    def _createDirectories(self,dirPath):
        """ 
        Creates directories if they do not exist
        
        @param {string} dirPath - Directory path
        """
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
            
    def _sanitizeText(self,text):
        """
        Removes undesireable characters from the text so that they are valid file name.
        
        @param {string} text - tex tto be sanitized
        """
        text = text.strip().lower()
        textWithoutSpecialChar = re.sub("[.?!\"\n',:]","",text)
        return re.sub("[ ]","_",textWithoutSpecialChar)
            
    def writeToFile(self):
        """ 
        Write the article to a txt file.
        """
        dirPath  = self._sanitizeText(f"{self.date}/{self.section_title}")
        self._createDirectories(dirPath)
    
        fileName = self._sanitizeText(f'{self.date}/{self.section_title}/{self.article_title}') + ".txt"
    
        with open(fileName,"w+", encoding="utf-8") as fobj:
            #print(f"{self.section_title}: {self.article_title}")
            fobj.write(self.extractText())
        
        
        
        
### HELPER METHODS
        
def getContent(date):
    """ 
    Makes a GET request and gets html content back. 
    
    @param {string} date - Date for which we want the html content
    @returns 
    """
    address = "https://www.thedailystar.net/newspaper?date={}".format(date)
    
    #createDirectories(date)

    html = urlopen(address)
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all('div',attrs={'class':"panel-pane pane-news-col no-title block"}) 

    return content

def findSectionsAndArticlesFromContent(date, content):
    """ 
    Finds and extracts all the news sections from the html content
    
    @param {string} date - String representation of the date for the sections
    @param {BeautifulSoup obj} - BeautifulSoup obj that contains all the html content
    @returns A dictionary mapping sections to their articles
    """
    articlesInSection = {}
    
    for section in content:
        section_title = section.find('div',attrs={'class':"container page-title centered"}).find('h2').text
        articles = section.find_all('div',attrs={'class':"list-content"})
        articlesInSection[section_title] = articles
        
    return articlesInSection

def populateSections(date, articlesInSection):
    """Returns a list of Section objects """
    sections = []
    for section_title, articles in list(articlesInSection.items()):
        sectionObj = Section(section_title,articles, date)
        sections.append(sectionObj)
    
    return sections


def getContentAndTimeList(numOfDaysToScrape):
    """Retrieves a list of content from Daily Star according to the number of days to scrape""" 
    content_list = []
    
    time_list = getDatesToScrape()
       
    for i in range(len(time_list)): #O(n)
        content_list.append(getContent(time_list[i]))
        
    return content_list, time_list

def getDatesToScrape():
    """ 
    Returns a list of date in string format, iterating  from start to end date.
    Start and end dates need to changed manually inside the method.
    """

    end_date = date(2018, 7, 21)  
    star_date = date(2018, 7, 21)  
    dates = [star_date + timedelta(days=x) for x in range((end_date-star_date).days + 1)]

    return [str(d) for d in dates]

def keepTrackOfScrapedArticles(date):
    """
    Writes the date to file a file. The date represents successfull scraping for that date
    """
    
    with open("successful_scraped_dates.txt", "a+") as file:
        file.write(date)
            
### MAIN        
def main():        
    content_list, time_list = getContentAndTimeList(numOfDaysToScrape)
        
    for i in range(len(content_list)):
        start = pytime.time()
        
        articlesInSection = findSectionsAndArticlesFromContent(time_list[i],content_list[i])     
        sections = populateSections(time_list[i], articlesInSection)
        [section.writeArticlesToFile() for section in sections]
        keepTrackOfScrapedArticles(time_list[i])
        
        end = pytime.time()
        delta = end - start
        print(f"It took {delta} seconds to write to file.")
        
if __name__ == "__main__":
    main()
    
    

