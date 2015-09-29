from irc import IrcConnection
from config import CLIENT_ID, CLIENT_SECRET, CHANNELS, TOKEN


def run():
	channel_list = CHANNELS.split(',')
	irc_conn = IrcConnection(TOKEN, channel_list)
	irc_conn.connect()


if __name__ == '__main__':
	run()
