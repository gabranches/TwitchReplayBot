import sys
sys.path.append('/home/gabranches/twitch/app')

import twitch


print(twitch.get_replay('applejacked', 30))