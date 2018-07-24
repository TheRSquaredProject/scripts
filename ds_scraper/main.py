# -*- coding: utf-8 -*-
"""
Main module. Use this to run the scraper. 

"""

import time as pytime
from datetime import date
from scraper import getContentAndTimeList, findSectionsAndArticlesFromContent, populateSections, keepTrackOfScrapedArticles


def main():
    #Input the start and end date. End date must be LATER than start date
    star_date = date(2018, 6, 9) 
    end_date = date(2018, 6, 9)  
         
    content_list, time_list = getContentAndTimeList(star_date, end_date )
        
    for i in range(len(content_list)):
        start = pytime.time()
        
        articlesInSection = findSectionsAndArticlesFromContent(content_list[i])     
        sections = populateSections(time_list[i], articlesInSection)
        [section.writeArticlesToFile() for section in sections]
        keepTrackOfScrapedArticles(time_list[i])
        
        end = pytime.time()
        delta = end - start
        print(f"It took {delta} seconds to write to file.")
        
if __name__ == "__main__":
    main()