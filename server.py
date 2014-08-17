
import urllib2, json
from datetime import *
from flask import *

ontv = Flask(__name__)


API_KEY = 'd805aa971b2b7a64cb3c27c6701d6683'
USERNAME = 'aho338'
base_url = 'http://api.trakt.tv/user/calendar/shows.json/'

WEEKDAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
MONTHS = ['January', 'February', 'March','April','May','June','July','August','September','October', 'November','December']

days_ago = 1 # days before today to search
days_ahead = 7 # days after today to search
total_days_to_search = days_ago + days_ahead
date_difference = timedelta(days_ago)
start_date = (date.today()-date_difference).isoformat().replace('-','')

def human_readable_date(date_string): #2014-12-31
	date_string = date_string.replace('-','')
	year = str(date_string[0:4])
	month = int(date_string[4:6])
	day = str(date_string[6:9])
	return MONTHS[month-1]+ ' ' + day+ ', ' + year

def parse_date(date_string):
	weekday_num = datetime.strptime(date_string,'%Y-%m-%d').weekday() # Monday = 0
	return WEEKDAYS[weekday_num]

def request_json_file():
	full_url = base_url+API_KEY+'/'+USERNAME+'/'+start_date+'/'+str(total_days_to_search)
	#full_url = base_url+API_KEY+'/'+start_date+'/'+str(total_days_to_search)
	#print(full_url)
	req = urllib2.Request(full_url)
	req.add_header('User-Agent', USERNAME+' tv-bot')
	try:
		response = urllib2.urlopen(req)
		data = json.loads(response.read())
		return data
	except urllib2.HTTPError:
		print("HTTP Error")
		return

# def read_json_file(filename):	
	# f = open(filename).read()
	# data = json.loads(f) # store post data
	# return data




"""
Add json data to a list of dictionaries.
Each dictionary is a day containing the following keys:
	day_name
	date
	episodes: dictionary containing the following keys:
		show_name
		episode_name
		overview
"""
def extract_data(data):
	rtn = []
	for day_data in data:
		day = {}
		day['day_name'] = get_day_of_week(day_data)
		day['date'] = get_date(day_data)
		day['episodes'] = []
		rtn.append(day)
		for episode in get_episodes(day_data):
			epi_key = {}
			epi_key['show_name'] = get_show_name(episode)
			epi_key['episode_name'] = get_episode_name(episode)
			epi_key['overview'] = get_overview(episode)
			epi_key['poster'] = get_poster(episode)
			epi_key['banner'] = get_banner(episode)
			epi_key['time'] = get_time(episode)
			epi_key['network'] = get_network(episode)
			epi_key['imdb'] = get_imdb(episode)
			day['episodes'].append(epi_key)
	return	rtn

### getters ###

def get_day_of_week(day):
	return parse_date(day['date'])

def get_date(day):
	return human_readable_date(day['date'])

def get_episodes(day):
	return day['episodes']

def get_show_name(episode):
	return episode['show']['title']

def get_episode_name(episode):
	return episode['episode']['title']

def get_overview(episode):
	if episode['episode']['overview'] != '':
		return episode['episode']['overview']
	elif episode['show']['overview'] != '':
		return episode['show']['overview']
	else:
		return ''

def get_poster(episode):
	return episode['show']['images']['poster']

def get_banner(episode):
	return episode['show']['images']['banner']

def get_time(episode):
	return episode['show']['air_time_localized']

def get_network(episode):
	return episode['show']['network']

def get_imdb(episode):
	id = episode['show']['imdb_id']
	if id == "":
		return "#"
	else:
		return 'http://www.imdb.com/title/'+id+'/'


@ontv.route("/")
def index():
	json_data = request_json_file()
	#json_data = read_json_file('sample.json')
	return render_template('index.html', tv_data = extract_data(json_data))

# @app.route("/")
# def index():
# 	return render_template('index.html', tv_data = read_json_file('sample.json'))

if __name__ == "__main__":
    ontv.run(debug=False)


"""
---- Thursday ------------
---- DATE: 2014-05-08 ----
Show: Conan (2010)
Episode: Sharon Stone, Marc Maron, Rodrigo y Gabriela

Show: The Daily Show with Jon Stewart
Episode: Katie Couric
Overview: The New York Senate engages in a spirited debate about yogurt, John Hodgman considers acquiring the Los Angeles Clippers, and Katie Couric discusses the obesity epidemic.

Show: The Colbert Report
Episode: Ellen Page
Overview: Stephen interviews a role-playing congressional candidate, Fox Business anchor Stu Varney gushes about his popular appeal, and Ellen Page talks "X-Men: Days of Future Past."

Show: The Tonight Show Starring Jimmy Fallon
Episode: Michael Fassbender, Zoe Saldana



"""

