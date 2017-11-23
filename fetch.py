from twython import Twython, TwythonError
import json

app_key='XLO8cM3MTk3FooPxeGYrOpYFG'
app_secret='874GxAnlqSXZ61TVJ1XadU8vlq4vPYV6kCBrRJQV8lhcbUOx0W'
oauth_token='760365669267283968-ZgmFMhJhmCFnjXESYB0yJVkNjHYDUtv'
oauth_token_secret='tRUlbFieFzLaaSRGk3FeNM4WeD4F4yPZYQ9Bm2HVCIW5V'

twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

#Search for Bandung ID
#str = twitter.search_geo(lat = '-6.914744', long = '107.609810', count=30, rad = '100mi')
#with open('loc.txt','w') as outfile:
#	json.dump(str, outfile)
#twitter.get_lastfunction_header('x-rate-limit-remaining')

#Search
str = twitter.get_user_timeline(screen_name = "temponewsroom",tweet_mode = "extended", count= 500, include_rts= False)
for tweet in str:
    print(tweet['full_text'])