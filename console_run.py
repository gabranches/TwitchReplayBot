from app.views import make_authorization_url
from app.irc import IrcConnection
from urllib.parse import urlparse, parse_qs
from app.config import CLIENT_ID, REDIRECT_URI, CLIENT_SECRET


def run(token):
	channels = ['#themexicanrunner', 
				'#kaceytron',
				'#claydavis64']

	irc_conn = IrcConnection(token, channels)
	irc_conn.connect()


if __name__ == '__main__':
	run('p6mbbh7iei6k2vebdqxnij7e2mwgwl')
	print(token)
