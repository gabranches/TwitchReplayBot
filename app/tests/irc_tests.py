import sys

sys.path.append('/home/gabranches/twitch/app')
from irc import split_line, get_message_type

test_msg = ':desellier!desellier@desellier.tmi.twitch.tv PRIVMSG #froggen :BAN EU CHAT PLZ'
print get_message_type(test_msg)
message = split_line(test_msg)
print message
