# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from Article import Article
import scraper

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
        success = 0
        errors = 0
        
        base = "https://www.thedailystar.net/"

        for article in self.articles_raw:
            try:
                article_title = article.h5.text
                article_url = base + article.a['href']
                response = scraper.makeSpoofedRequest(article_url)
                article_soup = BeautifulSoup(response.text, 'html.parser')
                articleObj = Article(self.section_title, article_title,article_soup, self.date)
                articleObj.writeToFile()
                success += 1
            except Exception as e:             
                print(f"Error writing {article_title}")
                errors += 1
                
                continue
        
        print(f"Wrote {success} articles to file in {self.section_title}")
        print(f"Could not write {errors} articles.")
        
        self._log(success, errors)
    
    def _log(self, successful, errors):
        logText = self._prepareLog(successful, errors)
        
        self._saveLog(logText)
    
    def _prepareLog(self, successful, errors):
        log = "-" * 20
        log += f"Log for {self.date} -- {self.section_title}\n"
        log += f"Sucessfully: {successful} artcles\n"
        log += f"Error: {errors} articles.\n "
        
        return log
    
    def _saveLog(self, log):
        with open("general_log.txt", "a") as file:
            file.write(log)
       
