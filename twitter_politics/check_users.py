import os
import pandas as pd
import re
from requests_oauthlib import OAuth1Session

# PART 1, GATHER THE DATA
# UN-COMMENT PART 2 ONCE YOU ARE DONE WITH THIS

consumer_key = "key"
consumer_secret = "key

usernames = []
influ = pd.read_csv("twitter_influencers.csv")
for index, line in influ.iterrows():
	user = line["account_handle"]
	usernames.append(user)

fields = "created_at,description,pinned_tweet_id"

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
fetch_response = oauth.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)

oauth_tokens = oauth.fetch_access_token(access_token_url)
access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

data = []
n = len(usernames)
for num, name in enumerate(usernames):
	print(f"on username number {num} of {n}")
	params = {"usernames": name, "user.fields": fields}
	response = oauth.get("https://api.twitter.com/labs/2/users/by?", params=params)
	# print(response)
	# print("Response status: %s" % response.status_code)
	# print("Body: %s" % response.text)
	data.append(response.text)

accts = {'data': data}
df = pd.DataFrame(accts, columns= ['data'])
df.to_csv('usernames.csv', index = False, header=True)



# PART 2, PARSE THE DATA
# ONCE YOU HAVE YOUR DATA IN ONE CSV, READ THROUGH IT AND MAKE SENSE OF IT

# users = []
# names = pd.read_csv("usernames.csv")
# for data in names["data"]:
# 	if data[2:6] == "data":
# 		user_name = re.findall("username\":\"(.*?)\"", data)
# 		users.append(user_name[0])

# all_accts = {'account_handle': users}
# df = pd.DataFrame(all_accts, columns= ['account_handle'])
# df.to_csv('twitter_influencers_active.csv', index = False, header=True)





