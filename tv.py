
import urllib2, json
from datetime import *


API_KEY = ''
USERNAME = 'aho338'
base_url = 'http://api.trakt.tv/user/calendar/shows.json/'

WEEKDAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

days_ago = 0 # days before today to search
days_ahead = 7 # days after today to search
total_days_to_search = days_ago + days_ahead
date_difference = timedelta(days_ago)
start_date = (date.today()-date_difference).isoformat().replace('-','')


def parse_date(date_string):
	weekday_num = datetime.strptime(date_string,'%Y-%m-%d').weekday() # Monday = 0
	return WEEKDAYS[weekday_num]

full_url = base_url+API_KEY+'/'+USERNAME+'/'+start_date+'/'+str(total_days_to_search)
req = urllib2.Request(full_url)
req.add_header('User-Agent', USERNAME+' tv-bot')

try:
	response = urllib2.urlopen(req)
	data = json.loads(response.read()) # store post data
	for day in data:
		print('---- '+parse_date(day['date'])+' ------------')
		print('---- DATE: '+day['date']+' ----')
		for episode in day['episodes']:
			print('Show: '+episode['show']['title'])
			print('Episode: '+episode['episode']['title'])
			if episode['episode']['overview'] != "":
				print('Overview: '+episode['episode']['overview'])
			print('')
except urllib2.HTTPError:
	print("HTTP Error")

