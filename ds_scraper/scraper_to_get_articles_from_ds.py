import os
import time as pytime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta

base = "https://www.thedailystar.net/"
numOfDaysToScrape = 2

class Section:
    def __init__(self, section_title,articles_raw):
        self.section_title = section_title
        self.articles_raw = articles_raw
        self.articles = []
        
    def createArticles(self):
        for article in self.articles_raw:
            try:
                article_title = article.h5.text
                article_url = base + article.a['href']
                article_html = urlopen(article_url)
                article_soup = BeautifulSoup(article_html, 'html.parser')
                self.articles.append(Article(self.section_title, article_title,article_soup))
                
            except:
                continue
        pytime.sleep(300)
        print(f"Created {len(self.articles)} articles")
        return self.articles
            

class Article:
    def __init__(self,section_title,article_title,article_content):
        self.section_title = section_title
        self.article_title = article_title
        self.article_content = article_content
    
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
        
def createDirectories(date):
    if not os.path.isdir(date):
        os.makedirs(date)
        
def getContent(date):  
    address = "https://www.thedailystar.net/newspaper?date={}".format(date)
    
    createDirectories(date)

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
        sectionObj = Section(section_title,articles)
        sections.append(sectionObj)
    
    return sections

def getArticleText(date, articleList):
    for article in articleList:
        text = ""
        section_title = article.getSectionTitle()
        article_title = article.getArticleTitle()
        text = article.extractText()
        
        print(f"{section_title}: {article_title}")
        
        writeArticlesToFile(date,section_title,article_title, text)
        
def writeArticlesToFile(date,section_title,article_title, article_text):
    if not os.path.isdir("{}/{}".format(date,section_title)):

        os.makedirs("{}/{}".format(date,section_title))
    
    with open(f'{date}/{section_title}/{article_title}.txt'.replace('?',""),"w") as fobj:
        fobj.write(article_text)


        
content_list = []
time_list = []            
for i in range(1,numOfDaysToScrape): #O(n)
    time = str(date.today()-timedelta(i))
    time_list.append(time)
    content_list.append(getContent(time))
    
for i in range(len(content_list)): #O(3n^2)   
    articlesInSection = findSectionsAndArticlesFromContent(time_list[i],content_list[i])     
    sections = populateSections(time_list[i], articlesInSection)
    articleList = [section.createArticles() for section in sections]
    getArticleText(time_list[i], articleList)
    

