"""
# Libraries
"""
# docs : https://github.com/GeneralMills/pytrends
from pytrends.request import TrendReq
from math import ceil
import numpy as np
import time
import operator

"""
# Methods
-------
1. Individual Search : Search and suggestions
2. Multiple Search : Search and sort
"""
def individualSearch(keywords, timeframe, geo):
    count = 1
    with open('analysis.csv', 'w') as file:
        print("keyword", "maxTimestamp", "suggestions", "relatedTopics", "relatedQuery", sep=";", file=file)

        for keyword in keywords:
            print("Progress :", count, "/", len(keywords), end = "\r")
            pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo = geo)

            try:
                maxTimestamp = pytrends.interest_over_time()[keyword].idxmax()
                suggestions = pytrends.suggestions(keyword)
                keys = ['title', 'type']
                suggestions = [[suggestion[key] for key in keys] for suggestion in suggestions]
                relatedQuery = pytrends.related_queries()
                relatedTopics = pytrends.related_topics()
            except (KeyError):
                maxTimestamp = "NaN"
                suggestions = "NaN"

            try:
                print(keyword, maxTimestamp, suggestions, relatedTopics[keyword]['rising']['topic_title'].tolist(), relatedQuery[keyword]['rising']['query'].tolist(), sep=';', file=file)
            except (KeyError, TypeError):
                print(keyword, maxTimestamp, suggestions, "NaN", "NaN", sep=';', file=file)
            count += 1

def multipleSearch(keywords, timeframe, geo):
    matrix = {keyword: 0.0 for keyword in keywords}
    iterations = ceil(len(keywords)/4)

    for i in range(iterations):
        print("Progress :", i + 1, "/", iterations)

        try:
            currentKeywords = (keywords[i * 4 : i * 4 + 4])
        except IndexError:
            currentKeywords = (keywords[i * 4 :])

        if(i>0):
            currentKeywords.insert(0, max)
            
        print(currentKeywords)
        pytrends.build_payload(currentKeywords, timeframe=timeframe, geo = geo)

        for keyword in currentKeywords:
            maxTimestamp = pytrends.interest_over_time()[keyword].idxmax()
            maxValue = pytrends.interest_over_time()[keyword].max()
            
            matrix[keyword] = maxValue

            if (maxValue == 100):
                if (i > 0):
                    keys = keywords[: i * 4]
                    keys.remove(max)

                    for key in keys:
                        matrix[key] *= (matrix[max] / 100)
                max = keyword
    
    with open('analysis.csv', 'w') as file:
        for key in matrix.keys():
            print(key, ";", matrix[key], file=file)

"""
# Main body
"""
t = time.time()

pytrends = TrendReq(hl='en-US', tz=420) # Connect to Google

keywords = ["Mahfud MD","Airlangga Hartarto","Muhadjir Effendy","Luhut Binsar Panjaitan","Prabowo Subianto","Pratikno","Tito Karnavian","Retno Marsudi","Fachrul Razi","Yasonna Laoly","Sri Mulyani Indrawati","Nadiem Makarim","Terawan Agus Putranto","Juliari Batubara","Ida Fauziah","Agus Gumiwang Kartasasmita","Agus Suparmanto","Arifin Tasrif","Basuki Hadimuljono","Budi Karya","Johnny G. Plate","Syahrul Yasin Limpo","Siti Nurbaya Bakar","Edhy Prabowo","Abdul Halim Iskandar","Sofyan Djalil","Suharso Monoarfa","Tjahjo Kumolo","Erick Thohir","Teten Masduki","Wishnutama","Gusti Ayu Darmavati","Bambang Brodjonegoro","Zainudin Amali"]

timeframe = 'now 7-d'

geo = 'ID'

multipleSearch(keywords, timeframe, geo)

print("Elapsed Time :", time.time() - t, "sec")