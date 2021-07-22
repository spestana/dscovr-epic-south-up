import tweepy # import tweepy for twitter api
from keys import * # import keys
from epic import EPIC # import EPIC image handler
import dscovr_ebooks_utils # import my function for making an animation

# command flag to look for in tweets
COMMAND_FLAG_STR = '#dscovr_ebooks'

# default response text to return when mentioned
ABOUT_DSCOVR_EBOOKS = 'I am a bot. Learn more here: https://spestana.github.io/2021/07/dscovr-epic-south-up/'

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
	f_read = open(file_name, 'r')
	last_seen_id = int(f_read.read().strip())
	f_read.close()
	return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
	f_write = open(file_name, 'w')
	f_write.write(str(last_seen_id))
	f_write.close()
	return
	
def retrieve_image():
	# retrieve the requested image
	filepath = 'tmp.jpg'
	
	# return the local temporary filepath to the image
	return filepath

def read_and_reply_to_tweets():
	# retrieve latest seen id
	last_seen_id = retrieve_last_seen_id(FILE_NAME)

	# get mentions since last seen id
	mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
	
	# for each new mention
	for mention in reversed(mentions):
		
		# store latest seen mention id
		last_seen_id = mention.id
		store_last_seen_id(last_seen_id, FILE_NAME)
		
		# if the mention contains the command flag string
		if COMMAND_FLAG_STR in mention.full_text.lower():
			# perform the action we want
			# ABOUT_DSCOVR_EBOOKS
			api.update_status('@' + mention.user.screen_name + ' ' +
                    ABOUT_DSCOVR_EBOOKS, mention.id)
		
def tweet_epic_animation():
	# retrieve the latest DSCOVR EPIC imagery and create a gif
	last_image = dscovr_ebooks_utils.make_animation()
	# post this image to twitter
	api.update_with_media(filename='animation.gif', status=last_image)




# set up api auth
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# run main function	
read_and_reply_to_tweets()
tweet_epic_animation()
