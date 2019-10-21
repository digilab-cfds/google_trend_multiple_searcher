# docs : https://github.com/GeneralMills/pytrends
from pytrends.request import TrendReq
from math import ceil
import numpy as np
import time
import operator

t = time.time()

pytrends = TrendReq(hl='en-US', tz=420) # Connect to Google

keywords = ["Paul Rudd", "Emma Watson", "Christopher Nolan", "Philip Seymour Hoffman", "Johnny Depp", "Derek Jeter", "Patricia Arquette", "Jim Carrey","Chris Brown","Franco Nero","Mark Harmon","Jim Parsons","John Travolta","Bill Murray","Jason Biggs","Courteney Cox","50 Cent","Howard Stern","Julia Louis-Dreyfus","Bruce Springsteen","Tom Cruise","Jeremy Renner","Kevin Garnett","Shah Rukh Khan","Clint Eastwood","Antonio Banderas","Golshifteh Farahani","Morgan Freeman","Danny Trejo","Angelina Jolie"]

iterations = ceil(len(keywords)/5) + 2
dataPointer = 4

matrix = {keyword : 0.0 for keyword in keywords}

for i in range(0, iterations):
    if(i==0):
        max = None
        currentKeywords = keywords[dataPointer*i : dataPointer*i + 4]
        pytrends.build_payload(currentKeywords, cat=0, timeframe='today 5-y')
        maxNeighbours = currentKeywords
    else:
        currentKeywords = keywords[dataPointer*i : dataPointer*i + 4]
        currentKeywords.append(max)
        pytrends.build_payload(currentKeywords, cat=0, timeframe='today 5-y')

    for keyword in currentKeywords:
        maxTimestamp = pytrends.interest_over_time()[keyword].idxmax()
        maxValue = pytrends.interest_over_time()[keyword].max()
        suggestions = pytrends.suggestions(keyword)
        
        matrix[keyword] = maxValue

        if(maxValue == 100 and keyword != max):
            max = keyword

    if max != currentKeywords[-1]:
        if(i==0):
            pass
        else:
            maxNeighbours.remove(currentKeywords[-1])
        for keyword in maxNeighbours:
            matrix[keyword] *= matrix[currentKeywords[-1]]/100
        maxNeighbours = currentKeywords[:-1]

print(sorted(matrix.items, key=operator.itemgetter(1)))

print("Elapsed Time :", time.time() - t, end = " sec\n")