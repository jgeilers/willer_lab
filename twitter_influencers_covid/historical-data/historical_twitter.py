
#booklet of how to run this dataset for others

import tweepy
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import csv
import urllib.request as url 
import os

def parse_tweet(status, video, pic):
	for i in status.extended_entities['media']:
		if i['type'] == 'video':
			for item in i['video_info']['variants']:
				if item['content_type'] == "application/x-mpegURL":
					video.append(item['url'])
		elif i['type'] == 'photo':
			pic.append(i['media_url_https'])
	return video, pic


def get_tweets(account_list, auth_api):

	if len(account_list) > 0:
		count, line_count, csv_count, tweet_count = 0, 662510, 1, 0
		csv_name = "covid_tweets" + str(csv_count) + ".csv"
		header_check = True
		
		for target in account_list:
			tweet_dict = dict()
			if line_count >= 1000000:
				csv_count += 1
				csv_name = "covid_tweets" + str(csv_count) + ".csv"
				line_count, header_check = 0, True

			count += 1
			print("%s / %s" % (count, len(account_list)), target)
			tweet_dict[target], start_date, tweet_count = [], datetime(2020, 2, 1, 0, 0, 0), 0
			with open(csv_name, newline = '', mode='a', encoding='utf-8') as csv_file:
				writer = csv.writer(csv_file, delimiter=',', quotechar='"')
				if header_check:
					fieldnames = ["Twitter Handle","date","text","picture","video","quote handle","quote text","quote picture","quote video"]
					writer.writerow(fieldnames)
					header_check = False
				try:
					tweets = Cursor(auth_api.user_timeline, id=target, exclude_replies=True, tweet_mode='extended', wait_on_rate_limit=True).items()
					for tweet_num, status in enumerate(tweets):
						if status.created_at <= start_date and tweet_count <= 500:
							created = status.created_at.strftime('%m/%d/%Y - %H:%M:%S')
							video_link, pic_link, text, q_handle, q_video_link, q_pic_link, q_text = [], [], "", "", [], [], ""
							# Gets text, video, and image from retweets
							if hasattr(status, "retweeted_status"):
								text = status.retweeted_status.full_text.replace('\n','').replace('\r','')
								if hasattr(status.retweeted_status, "extended_entities"):
									video_link, pic_link = parse_tweet(status.retweeted_status, video_link, pic_link)
									
							# Gets text, video, and image from tweet
							else:
								# Checks if quoted tweet and gets text, video, and image from quote
								if hasattr(status, "quoted_status"):
									q_handle = status.quoted_status.user.screen_name
									q_text = status.quoted_status.full_text.replace('\n','').replace('\r','')
									if hasattr(status.quoted_status, "extended_entities"):
										q_video_link, q_pic_link = parse_tweet(status.quoted_status, q_video_link, q_pic_link)
								
								# Gets regular tweet information
								text = status.full_text.replace('\n','').replace('\r','')
								if hasattr(status, "extended_entities"):
									video_link, pic_link = parse_tweet(status, video_link, pic_link)

							tweet_dict[target].append([created, text, pic_link, video_link, q_handle, q_text, q_pic_link, q_video_link])
							line_count += 1
							tweet_count += 1

					for item in tweet_dict:
						for elem in tweet_dict[item]:
							writer.writerow([item, elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7]])
				except:
					pass


def main():

	# Authenticate to Twitter
	auth = tweepy.OAuthHandler("ykhXYXaehvutBn9KrDJl8yoUy", "h07UCbLAnN1wjll339Sg16gCtlpWmfwitC1njJSn8cED7IbACQ")
	auth.set_access_token("556463747-o4O8x8ZxxxbLsyoX7M9p9HZfjBOfWnLiNEtRYNZn","qT2ZfL573eoB8MBegrVrkyjaH4K6WddjKPk8cfo64arTw")
	auth_api = tweepy.API(auth)
	
	# test authentication
	try:
	    auth_api.verify_credentials()
	except:
	    print("Error during authentication")
	
	#begin reading input
	account_list = []
	if (len(sys.argv) > 1):
		twitter_handle_list = sys.argv[1:]
		with open(twitter_handle_list[0], "r") as a_file:
			for line in a_file:
			    stripped_line = line.strip()
			    account_list.append(stripped_line)
	else:
	  print("Please provide a list of usernames at the command line.")
	  sys.exit(0)

	get_tweets(account_list, auth_api)


if __name__ == "__main__":
    main()

