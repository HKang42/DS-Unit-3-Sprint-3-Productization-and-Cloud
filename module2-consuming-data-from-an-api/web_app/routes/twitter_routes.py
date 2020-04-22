# web_app/routes/twitter_routes.py

from flask import Blueprint, render_template, jsonify

# import the twitter_api_client so that we don't have to retype the first 
# half of the twitter services code
from web_app.services.twitter_service import twitter_api

twitter_routes = Blueprint("twitter_routes", __name__)

@twitter_routes.route("/users/<screen_name>/fetch")
def fetch_user_data(screen_name=None):
    
    print(screen_name)
    
    api = twitter_api()
    user = api.get_user(screen_name)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    
    # to keep things simple, we'll just return the number of statuses
    # switch to this line to return actual statuses
    #return jsonify({"user": user._json, "tweets": [s._json for s in statuses]})
    
    return jsonify({"user": user._json, "tweet_count": len(statuses)})

