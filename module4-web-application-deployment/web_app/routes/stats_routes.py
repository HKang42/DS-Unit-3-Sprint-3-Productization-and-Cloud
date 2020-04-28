from flask import Blueprint, request, jsonify, render_template
from sklearn.datasets import load_iris # just to have some data to use when predicting
from sklearn.linear_model import LogisticRegression

from web_app.models import User
from web_app.services.basilica_service import basilica_api_client as basilica_connection

#from web_app.classifier import load_model

stats_routes = Blueprint("stats_routes", __name__)

@stats_routes.route("/stats/iris")
def iris():

    # load data and split into X and y
    X, y = load_iris(return_X_y=True)

    # train model
    clf = LogisticRegression(random_state=0, solver='lbfgs',
                            multi_class='multinomial').fit(X, y)

    return str(clf.predict(X[:2, :]))

#@stats_routes.route("/stats/prediction_form")
@stats_routes.route("/")
def twitoff_prediction_form():

    return render_template("prediction_form.html")

@stats_routes.route("/stats/predict", methods=["POST"])
def twitoff_prediction():
    print("FORM DATA:", dict(request.form))

    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    #
    # TRAIN THE MODEL
    #
    # inputs = embeddings for each tweet
    # labels = screen name for each tweet

    # create model object
    model = LogisticRegression()
    
    user_a = User.query.filter(User.screen_name == screen_name_a).one()
    user_b = User.query.filter(User.screen_name == screen_name_b).one()

    user_a_tweets = user_a.tweets
    user_b_tweets = user_b.tweets

    all_tweets = user_a_tweets + user_b_tweets
    embeddings = []
    labels = []

    for tweet in all_tweets:
        embeddings.append(tweet.embedding)
        labels.append(tweet.user.screen_name)

    model.fit(embeddings, labels)

    #
    # MAKE PREDICTION
    #

    # input our test or real tweet and see what we get
    test_embedding = basilica_connection().embed_sentence(tweet_text, model="twitter")
    result = model.predict([test_embedding])
    screen_name_most_likely = result[0]

    return render_template("prediction_results.html"
        , screen_name_a=screen_name_a
        , screen_name_b = screen_name_b
        , tweet_text = tweet_text
        , screen_name_most_likely = screen_name_most_likely) 