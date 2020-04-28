# web_app/routes/home_routes.py

from flask import Blueprint, redirect

home_routes = Blueprint("home_routes", __name__)

# @home_routes.route("/")
# def index():
#     # x = 2 + 2
#     # return f"Hello World! {x}"
#     return redirect("/stats/prediction_form")

@home_routes.route("/about")
def about():
    return "About me"