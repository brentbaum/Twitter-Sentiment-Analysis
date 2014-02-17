import sys
import twitter
import urllib2
import json
import pickle
from pygooglechart import SimpleLineChart
from graphy.backends import google_chart_api

import dev_keys


def averageSentiments(tweets):
    polarity_total = 0
    polarity_total_without_neutral = 0
    count = 0
    tl = tweets['data']

    for tweet in tl:
        if not (tweet["polarity"] == 2):
            polarity_total += int(float(tweet["polarity"]))
            count = count + 1
        polarity_total_without_neutral += int(float(tweet["polarity"]))

    return (float(polarity_total) / count, float(polarity_total_without_neutral) / float(len(tl)))


def makeSentimentGraph(tweets):
    tl = tweets['data']
    data_pairs = []
    data_x = []
    data_y = []
    y = 0
    x = 0
    for tweet in tl:
        x += 1
        y += tweet["polarity"]-2
        data_x.append(x)
        data_y.append(y)
        data_pairs.append([x, y])

    chart = google_chart_api.LineChart(data_y[:1500])

    return chart.display.Img(600, 200)


def sentimentCount(tweets):
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    tl = tweets['data']

    for tweet in tl:
        if(tweet["polarity"] == 0):
            negative_count += 1
        elif(tweet["polarity"] == 2):
            neutral_count += 1
        else:
            positive_count += 1

    return (negative_count, neutral_count, positive_count)


def analyzeSentiments( tweets_with_sentiment, username ):
    happiness = averageSentiments(tweets_with_sentiment)

    counts = sentimentCount(tweets_with_sentiment)

    graph = makeSentimentGraph(tweets_with_sentiment)

    output = ""
    output += "<html><head></head><body><h1>Sentiment analysis for " + username + "</h1>"
    output += "<p>Happiness by extremes: " + str(happiness[0]) + "<br />Happiness overall: " + str(happiness[1]) + "</p>"
    output += "<p>Sentiment counts: <br /><br />Negative: " + str(counts[0]) + \
        "<br />Neutral: " + str(counts[1]) + "<br />Positive: " + str(counts[2]) + "</p>"
    output += graph
    output += "</body></html>"
    f = open(username+'_analysis.html', 'w')
    f.write(output)
