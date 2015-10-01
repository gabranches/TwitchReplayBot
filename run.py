from irc import IrcConnection
from config import TOKEN
from twitch.streams import CHANNELS


def run():
    channel_list = CHANNELS.lower().split(',')
    irc_conn = IrcConnection(TOKEN, channel_list)
    irc_conn.connect()


if __name__ == '__main__':
    run()
