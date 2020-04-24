from flask import Blueprint, request, jsonify, render_template
from sklearn.datasets import load_iris # just to have some data to use when predicting
from sklearn.linear_model import LogisticRegression

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

print ("hi")