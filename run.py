from irc import IrcConnection
from config import CLIENT_ID, REDIRECT_URI, CLIENT_SECRET, CHANNELS, TOKEN


def run():
	irc_conn = IrcConnection(TOKEN, CHANNELS)
	irc_conn.connect()


if __name__ == '__main__':
	run()
