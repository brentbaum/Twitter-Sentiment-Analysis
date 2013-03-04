import sys, twitter, operator, urllib, urllib2, json, codecs, cmd

twitterURL = "http://twitter.com"

def fetch(user):
    data = {}
    api = twitter.Api(consumer_key='gMrL2bCARpzY7ZQqGzJzlQ',
                      consumer_secret='PvQ8vmXcrC6plV9CYl4FhDpOIhx4DPPXBUX85Mej3I',
                      access_token_key='752422021-2dUbwPfFXoDlJTSdQpDC4b7rsSkbHBtIsj6CNCP8',
                      access_token_secret='GOcpB40Kq2i1InTl589qAMeEkzgV1Zw4jvZq781ENBc')
    max_id = None
    total = 0
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
        print >>sys.stderr, "Fetched %d/%d/%d new/old/total." % (
            newCount, ignCount, total)
        if newCount == 0:
            break
        max_id = min([s.id for s in statuses]) - 1
    return data.values()

def getSentiment(tweets):
  url = 'http://www.sentiment140.com/api/bulkClassifyJson?appid=bwb8ta@virginia.edu'
  encoded_str = json.dumps(tweets)
  response = urllib2.urlopen(url, encoded_str).read()
  return json.loads(response)

def analyzeSentiment(tweets):
  polarity_total = 0
  polarity_total_without_neutral = 0;
  count = 0
  tl = tweets['data']

  print tl

  for tweet in tl:
    if not (tweet["polarity"] == 2):
      polarity_total += int(float(tweet["polarity"]))
      count = count + 1
    polarity_total_without_neutral += int(float(tweet["polarity"]))

  return (float(polarity_total) / count, float(polarity_total_without_neutral) / float(len(tl)))

def analyze(username):
  if username:
    tweet_list = fetch(username)
  tweet_text_list = []
  for tweet in tweet_list:
    try:
      contents = (tweet.text).replace("'","")
      tweet_text_list.append({"text": str(tweet.text)})
    except UnicodeEncodeError:
      continue
  tweet_body = {'data':tweet_text_list}
  tweets_with_sentiment = getSentiment(tweet_body)

  happiness = analyzeSentiment(tweets_with_sentiment)
  print("Happiness by extremes:", happiness[0],"\nHappiness overall:", happiness[1]);

while (True):
  input = raw_input("\nEnter a twitter username in the form @username. For example, to see my happiness I would enter: @bbombgardener\n\n")
  print("")
  analyze(input)