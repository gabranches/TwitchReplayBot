import socket
import sys
import re
import app.twitch


class IrcConnection(object):

	host = 'irc.twitch.tv'
	port = 6667
	readbuffer = ''

	def __init__(self, token, channels):
		self.channels = channels
		self.nick = 'TwitchReplayBot'
		self.ident = 'twitchreplaybot'
		self.realname = 'TwitchReplayBot'
		self.token = token

	def connect(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.host, self.port))
		s.send('PASS oauth:{}\r\n'.format(self.token).encode())
		print('Sending password')
		s.send('NICK {}\r\n'.format(self.nick).encode())
		print('Sending nick')
		s.send('USER {0} {1} Server {2}\r\n'.format(self.ident, self.host, self.realname).encode())
		print('Sending user')
		for ch in self.channels:
			s.send('JOIN {}\r\n'.format(ch).encode())
			print('Joining %s' % ch)

		while True:
			last_request = 0
			self.readbuffer = self.readbuffer + s.recv(4096).decode()
			temp = self.readbuffer.split('\n')
			self.readbuffer = temp.pop()

			for line in temp:
				line = line.rstrip()
				if get_message_type(line) == 'PRIVMSG':
					message = split_line(line)
					print(message['channel'] + ' ' + message['author'] + 
							' ' + message['text'])
					check_if_cmd(message, s)

				if line.split()[0] == 'PING':
					s.send('PONG {}\r\n'.format(line[1]).encode())

def check_if_cmd(message, s):
	if message['text'] == ':!replay':
		replay_url = app.twitch.get_replay(message['channel'], 90)
		print(replay_url)
		if replay_url:
			s.send('PRIVMSG {0} :Replay VOD {1}\r\n'.format(message['channel'], replay_url).encode())
		else:
			s.send('PRIVMSG {0} :VOD not available yet.\r\n'.format(message['channel']).encode())

def get_message_type(msg):
	p = re.compile(r'PRIVMSG')
	m = p.search(msg)
	if m:
		return 'PRIVMSG'
	else:
		return 'other'

def split_line(line):
	message = {}
	line = line.split()

	# Get author
	p = re.compile(r':(\w*)!')
	m = p.match(line[0])
	if m:
		message['author'] = m.group(1) 

	# Get channel
	message['channel'] = line[2]

	# Get text
	text = []
	for i in range(3, len(line)):
		text.append(line[i])
	message['text'] = ' '.join(text)
	
	return message