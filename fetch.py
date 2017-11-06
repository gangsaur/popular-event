from twython import Twython, TwythonError
import json

app_key=''
app_secret=''
oauth_token=''
oauth_token_secret=''

twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

#Search for Bandung ID
#str = twitter.search_geo(lat = '-6.914744', long = '107.609810', count=30, rad = '100mi')
#with open('loc.txt','w') as outfile:
#	json.dump(str, outfile)
#twitter.get_lastfunction_header('x-rate-limit-remaining')

#Search
str = twitter.search(geocode='-6.914744,107.609810,15km', count='150')
with open('tweets.txt','w') as outfile:
	print(json.dump(str, outfile, indent=4))
twitter.get_lastfunction_header('x-rate-limit-remaining')