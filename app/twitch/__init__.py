import requests
import datetime
import time
import re
import math

def get_channel_videos(channel):
	url = 'https://api.twitch.tv/kraken/channels/{}/videos?broadcasts=true'.format(channel)
	r = requests.get(url)
	print(r.status_code)
	return r.json()


def datetime_to_epoch(datetime_str):
	p = re.compile(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z')
	m = p.match(datetime_str)
	if m:
		year = int(m.group(1))
		month = int(m.group(2))
		day = int(m.group(3))
		hour = int(m.group(4))
		minute = int(m.group(5))
		second = int(m.group(6))

	time_datetime = datetime.datetime(year, month, day, hour, minute, second)
	time_epoch = int(time.mktime(time_datetime.timetuple()))
	return time_epoch

def get_latest_video_data(json_data):
	data = {}
	try:
		data['recorded_at'] = datetime_to_epoch(json_data['videos'][0]['recorded_at'])
		data['url'] = json_data['videos'][0]['url']
	except KeyError:
		return None
	return data 

def get_replay(channel, offset):
	delay = 20
	json_data = get_channel_videos(channel)
	replay_data = get_latest_video_data(json_data)

	if replay_data:
		request_time = int(time.time()) + 4*60*60
		replay_time_total = (request_time - offset - delay) -replay_data['recorded_at']
		replay_min = int(math.floor(replay_time_total / 60))
		replay_sec = replay_time_total % 60
		return(replay_data['url'] + '?t={0}m{1}s'.format(replay_min, replay_sec))
	else:
		return None
