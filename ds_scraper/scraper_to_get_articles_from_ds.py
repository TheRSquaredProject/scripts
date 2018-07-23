import time as pytime
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

from Section import Section
from get_fake_user_proxies import getProxy       

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


def getContentAndTimeList():
    """Retrieves a list of content from Daily Star and a list of dates for which to scrape""" 
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

    end_date = date(2018, 7, 20)  
    star_date = date(2018, 7, 12)  
    dates = [star_date + timedelta(days=x) for x in range((end_date-star_date).days + 1)]

    return [str(d) for d in dates]

def getContent(date):
    """ 
    Makes a GET request and gets html content back. 
    
    @param {string} date - Date for which we want the html content
    @returns 
    """
    address = "https://www.thedailystar.net/newspaper?date={}".format(date)
    
    response = makeSpoofedRequest(address)
    #spoofedIp = getProxy()['ip']
    #proxy = {"http": str(spoofedIp)}
    #response = requests.get(address, proxies=proxy)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    content = soup.find_all('div',attrs={'class':"panel-pane pane-news-col no-title block"}) 

    return content

def makeSpoofedRequest(address):
    spoofedIp = getProxy()['ip']
    proxy = {"http": str(spoofedIp)}
    response = requests.get(address, proxies=proxy)

    return response        
    
def keepTrackOfScrapedArticles(date):
    """
    Writes the date to file a file. The date represents successfull scraping for that date
    """
    
    with open("successful_scraped_dates.txt", "a+") as file:
        file.write(f"{date}\n")
            
### MAIN        
def main():        
    content_list, time_list = getContentAndTimeList()
        
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
    
    

