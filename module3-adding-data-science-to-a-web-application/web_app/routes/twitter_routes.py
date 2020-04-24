# web_app/routes/twitter_routes.py

from flask import Blueprint, render_template, jsonify
from web_app.models import User, Tweet, db, parse_records

# import the twitter_api_client so that we don't have to retype the first 
# half of the twitter services code
from web_app.services.twitter_service import twitter_api

# import basilica_api_client for the same reason as above
from web_app.services.basilica_service import basilica_api_client

twitter_routes = Blueprint("twitter_routes", __name__)

@twitter_routes.route("/users/<screen_name>/fetch")
def fetch_user_data(screen_name=None):
    
    print(screen_name)
    
    # get our user data for whichever twitter user
    api = twitter_api()
    twitter_user = api.get_user(screen_name)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)

    #
    # STORE USER
    #

    # get existing user from the db 
    # or initialize a new one if the query returns None
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    
    # assign column values to the twitter information
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    
    # add user to database
    db.session.add(db_user)
    db.session.commit()
    
    #breakpoint()
    #return "OK"
    #return render_template("user.html", user=db_user, tweets=statuses) # tweets=db_tweets

    #
    # STORE TWEETS
    #

    # initialize basilica api
    basilica_api = basilica_api_client()
    
    # create list of tweet texts
    all_tweet_texts = [status.full_text for status in statuses]
    
    # pass tweets to api so it can embed the sentences using the twitter model
    embeddings = list(basilica_api.embed_sentences(all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS", len(embeddings))

    # TODO: explore using the zip() function maybe...
    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")
        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id # or db_user.id
        db_tweet.full_text = status.full_text
        #embedding = basilica_client.embed_sentence(status.full_text, model="twitter") # todo: prefer to make a single request to basilica with all the tweet texts, instead of a request per tweet
        embedding = embeddings[counter]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter+=1
    db.session.commit()
    #breakpoint()
    return "OK"
    #return render_template("user.html", user=db_user, tweets=statuses) # tweets=db_tweets

@twitter_routes.route("/users")
def list_users_human_friendly():
    db_users = User.query.all()
    return render_template("users.html", users=db_users, message="The database contains the following users") # tweets=db_tweets@

@twitter_routes.route("/users.json")
def list_users():
    db_users = User.query.all()
    users_response = parse_records(db_users)
    return jsonify(users_response)

@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)

    db_user = User.query.filter(User.screen_name == screen_name).one()

    return render_template("user.html", user=db_user, tweets=db_user.tweets)

