# web_app/__init__.py

from flask import Flask
from web_app.models import db, migrate

# put our root director somewhere else
from web_app.routes.home_routes import home_routes
from web_app.routes.book_routes import book_routes
from web_app.routes.twitter_routes import twitter_routes
from web_app.routes.admin_routes import admin_routes
from web_app.routes.stats_routes import stats_routes

# application factory pattern
# function to congfigure and return the app
# can invoke whenever we need to test the app
# tell our app to use those new roots
def create_app():
    app = Flask(__name__)

    # configure our app to use a database
    # We'll use the relative path option here
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///twitoff_hkang.db"
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/mjr/Desktop/web-app-inclass-11/twitoff_hkang.db"

    # configure app to use migration object (allow app to interface with data)
    db.init_app(app)
    migrate.init_app(app, db)

    # configure routes
    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    app.register_blueprint(twitter_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(stats_routes)
    return app

# when you run the file, it will run the app
if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)