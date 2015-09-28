from app import app
from app.config import CLIENT_ID, REDIRECT_URI, CLIENT_SECRET
import requests

from app.irc import IrcConnection
from flask import render_template, request, redirect


@app.route('/')
def get_auth_url():
	return redirect(make_authorization_url()) 

@app.route('/callback')
def get_access_token():
	post_data = { 'client_id': CLIENT_ID,
					'client_secret': CLIENT_SECRET,
					'grant_type': 'authorization_code',
					'redirect_uri': REDIRECT_URI,
					'code': request.args.get('code'),
					'state': request.args.get('state')
	}
	r = requests.post('https://api.twitch.tv/kraken/oauth2/token', params=post_data)
	token = r.json()['access_token']
	run(token)
	return 'Connected.'

def run(token):
	channels = ['#themexicanrunner', 
				'#kaceytron',
				'#claydavis64']

	irc_conn = IrcConnection(token, channels)
	irc_conn.connect()

 
def make_authorization_url():
	from uuid import uuid4
	state = str(uuid4())
	params = {'client_id': CLIENT_ID,
				'response_type': 'code',
				'state': state,
				'redirect_uri': REDIRECT_URI,
				'scope': 'chat_login'}
	import urllib
	url = 'https://api.twitch.tv/kraken/oauth2/authorize?' + urllib.parse.urlencode(params)
	return url
