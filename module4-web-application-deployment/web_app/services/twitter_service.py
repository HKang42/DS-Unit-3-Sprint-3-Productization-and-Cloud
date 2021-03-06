import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# use a function for the api so we can import it as a module elsewhere
def twitter_api():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    print("AUTH", auth)
    api = tweepy.API(auth)
    print("API", api)
    #print(dir(api))
    return api

if __name__ == "__main__":

    api = twitter_api()
    user = api.get_user("elonmusk")
    print("\nUSER", user)
    print("\nscreen name:",user.screen_name)
    print("\nname:", user.name)
    print("\nfollower count:", user.followers_count)

    statuses = api.user_timeline("elonmusk")

    print("\nstatuses:")
    print(statuses)

    #breakpoint()

    #public_tweets = api.home_timeline()
    #
    #for tweet in public_tweets:
    #    print(type(tweet)) #> <class 'tweepy.models.Status'>
    #    #print(dir(tweet))
    #    print(tweet.text)
    #    print("-------------")