import os
import time as pytime
import re
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta

base = "https://www.thedailystar.net/"
numOfDaysToScrape = 2

class Section:
    def __init__(self, section_title,articles_raw,date):
        self.section_title = section_title
        self.articles_raw = articles_raw
        self.date = date
        
    def createArticles(self):
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
    def __init__(self,section_title,article_title,article_content, date):
        self.section_title = section_title
        self.article_title = article_title
        self.article_content = article_content
        self.date = date
    
    def getSectionTitle(self):
        return self.section_title
    
    def getArticleTitle(self):
        return self.article_title
    
    def getArticleContent(self):
        return self.article_content
    
    def extractText(self):
        paras = self.article_content.find('div',attrs={'class':["field-body view-mode-full","field-body"]}).find_all('p')
        text = self._extractParasAndFormText(paras)
        return text
    
    def _extractParasAndFormText(self,paras):
        
        text = "\n ".join([str(para.text) for para in paras])
        return text
    
    def _createDirectories(self,dirPath):
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
            
    def _sanitizeText(self,title):
        title = title.strip().lower()
        textWithoutSpecialChar = re.sub("[.?!\"\n',]","",title)
        return re.sub("[ ]","_",textWithoutSpecialChar)
            
    def writeToFile(self):    
        dirPath  = self._sanitizeText(f"{self.date}/{self.section_title}")
        self._createDirectories(dirPath)
    
        fileName = self._sanitizeText(f'{self.date}/{self.section_title}/{self.article_title}') + ".txt"
    
        with open(fileName,"w+", encoding="utf-8") as fobj:
            #print(f"{self.section_title}: {self.article_title}")
            fobj.write(self.extractText())
        
        
        
        
### HELPER METHODS
        
def getContent(date):  
    address = "https://www.thedailystar.net/newspaper?date={}".format(date)
    
    #createDirectories(date)

    html = urlopen(address)
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all('div',attrs={'class':"panel-pane pane-news-col no-title block"}) 

    return content

def findSectionsAndArticlesFromContent(date, content):
    articlesInSection = {}
    
    for section in content:
        section_title = section.find('div',attrs={'class':"container page-title centered"}).find('h2').text
        articles = section.find_all('div',attrs={'class':"list-content"})
        articlesInSection[section_title] = articles
        
    return articlesInSection

def populateSections(date, articlesInSection):
    sections = []
    for section_title, articles in list(articlesInSection.items()):
        sectionObj = Section(section_title,articles, date)
        sections.append(sectionObj)
    
    return sections


def getContentAndTimeList(numOfDaysToScrape):
    content_list = []
    time_list = [] 
           
    for i in range(1,numOfDaysToScrape): #O(n)
        time = str(date.today()-timedelta(i))
        time_list.append(time)
        content_list.append(getContent(time))
    return content_list, time_list


### MAIN        
def main():        
    
    content_list, time_list = getContentAndTimeList(numOfDaysToScrape)
        
    for i in range(len(content_list)): #O(3n^2)   
        articlesInSection = findSectionsAndArticlesFromContent(time_list[i],content_list[i])     
        sections = populateSections(time_list[i], articlesInSection)
        [section.createArticles() for section in sections]
        
if __name__ == "__main__":
    main()
    
    

