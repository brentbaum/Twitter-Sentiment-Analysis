

import sys, twitter, urllib2, json, pickle
from pygooglechart import SimpleLineChart
from graphy.backends import google_chart_api
#import matplotlib.pyplot as pl

twitterURL = "http://twitter.com"


def fetch(user):
    data = {}
    api = twitter.Api(consumer_key='gMrL2bCARpzY7ZQqGzJzlQ',
                      consumer_secret='PvQ8vmXcrC6plV9CYl4FhDpOIhx4DPPXBUX85Mej3I',
                      access_token_key='752422021-2dUbwPfFXoDlJTSdQpDC4b7rsSkbHBtIsj6CNCP8',
                      access_token_secret='GOcpB40Kq2i1InTl589qAMeEkzgV1Zw4jvZq781ENBc')
    max_id = None
    total = 0
    print "Fetching tweets..."
    while True:
        statuses = api.GetUserTimeline(user, count=200, max_id=max_id)
        newCount = ignCount = 0
        for s in statuses:
            if s.id in data:
                ignCount += 1
            else:
                data[s.id] = s
                newCount += 1
        total += newCount
        print "..."
        if newCount == 0:
            break
        max_id = min([s.id for s in statuses]) - 1
    return data.values()


def getSentiment(tweets):
    print "Analyzing Tweets...\n"
    url = 'http://www.sentiment140.com/api/bulkClassifyJson?appid=bwb8ta@virginia.edu'
    encoded_str = json.dumps(tweets)
    response = urllib2.urlopen(url, encoded_str).read()
    return json.loads(response)


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
        #if tweet["polarity"] != 2:
        y += tweet["polarity"]-2
        data_x.append(x)
        data_y.append(y)
        data_pairs.append([x, y])

    chart = google_chart_api.LineChart(data_y[:1500])

    return chart.display.Img(600, 200)

    #max_y = 200
    #chart = SimpleLineChart(200, 125, y_range=[0, max_y])
    #chart.add_data(data_y)
    #file_name = input+".png"
    #chart.download(file_name)
    #print "Chart created and is available at ",file_name


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


def getTweetSentiments(username):
    if username:
        tweet_list = fetch(username)
    tweet_text_list = []
    for tweet in tweet_list:
        try:
            contents = tweet.text.replace("'", "")
            tweet_text_list.append({"text": str(contents)})
        except UnicodeEncodeError:
            pass

    tweet_body = {'data': tweet_text_list}
    return getSentiment(tweet_body)


def analyzeSentiments(tweets_with_sentiment):
    happiness = averageSentiments(tweets_with_sentiment)

    counts = sentimentCount(tweets_with_sentiment)

    graph = makeSentimentGraph(tweets_with_sentiment)

    output = ""
    output += "<html><head></head><body><h1>Sentiment analysis for " + input + "</h1>"
    output += "<p>Happiness by extremes: " + str(happiness[0]) + "<br />Happiness overall: " + str(happiness[1]) + "</p>"
    output += "<p>Sentiment counts: <br /><br />Negative: " + str(counts[0]) + \
        "<br />Neutral: " + str(counts[1]) + "<br />Positive: " + str(counts[2]) + "</p>"
    output += graph
    output += "</body></html>"
    f = open(input+'_analysis.html', 'w')
    f.write(output)
    print "Created file at "+input+"_analysis.html with full analysis"


while (True):
    input = raw_input("\nEnter a twitter username in the form @username. For example, to see my happiness I would enter: @bbombgardener\n\n")
    if(input[0] == '@'):
        input = input[1:]
    print("")
    sentiments = getTweetSentiments(input)
    analyzeSentiments(sentiments)
