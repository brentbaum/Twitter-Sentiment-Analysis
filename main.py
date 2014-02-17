from __future__ import print_function
import sys
import twitter
import operator
import urllib
import urllib2
import json
import codecs
import cmd

import sentiment_analysis
import dev_keys


twitterURL = "http://twitter.com"


def fetch(user):
    data = {}
    api = twitter.Api( consumer_key = dev_keys.consumer_key,
                       consumer_secret = dev_keys.consumer_secret,
                       access_token_key = dev_keys.access_token_key,
                       access_token_secret = dev_keys.access_token_secret )

    max_id = None
    total = 0
    while True:
        statuses = api.GetUserTimeline( screen_name=user, count=200, max_id=max_id )
        newCount = ignCount = 0
        for s in statuses:
            if s.id in data:
                ignCount += 1
            else:
                data[s.id] = s
                newCount += 1
        total += newCount
        print( "Fetched %d new, %d old, %d total" %(
                newCount, ignCount, total ) )
        if newCount == 0:
            break
        max_id = min([s.id for s in statuses]) - 1
    return data.values()


def getSentiment(tweets):
    url = 'http://www.sentiment140.com/api/bulkClassifyJson?appid=bwb8ta@virginia.edu'
    encoded_str = json.dumps(tweets)
    response = urllib2.urlopen(url, encoded_str).read()
    return json.loads(response)


def getTweetSentiments( username=None ):
    assert( username )
    tweet_list = fetch( username )
    tweet_text_list = []
    for tweet in tweet_list:
        try:
            contents = (tweet.text).replace("'","")
            tweet_text_list.append({"text":str(contents)})
        except UnicodeEncodeError:
            continue

    tweet_body = {'data':tweet_text_list}
    tweets_with_sentiment = getSentiment(tweet_body)
    return getSentiment(tweet_body)


def analyze( sentiments, username ):
    print( 'analyzing %s...' %username )
    happiness = sentiment_analysis.averageSentiments( sentiments )
    return happiness[0], happiness[1]


def makeGraph( sentiments, username ):
    sentiment_analysis.analyzeSentiments( sentiments, username )


if __name__ == '__main__':
    while (True):
        username = raw_input('\nEnter username as @username: ')
        if len( username ) == 0:
            print( 'Need a username!' )
            continue
        if( username[0] == '@' ):
            username = username[1:]
        sentiments = getTweetSentiments( username )
        extremes, overall = analyze( sentiments, username )
        makeGraph( sentiments, username )
        print( 'Happiness by extremes: %s' %extremes )
        print( 'Happiness by overall: %s' %overall )
        print( "Created file at "+username+"_analysis.html with full analysis" )
        more = raw_input( '\nContinue? (y/n) ' )
        if more != 'y' and more != 'Y':
            break
