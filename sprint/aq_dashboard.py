"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
import openaq
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(APP)
migrate = Migrate()
db.init_app(APP)
migrate.init_app(APP, db)


class Record(db.Model):
    """create record class to store air quality information"""
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(25))
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "Time: {}. Value: {}".format(self.datetime, self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    # drop current data
    db.drop_all()
    db.create_all()

    # get data from OpenAQ
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    data = body["results"]

    # loop through data, create Record objects, and add to db
    i = 1
    for point in data:
        time = point["date"]["utc"]
        value = point["value"]

        # initialize record
        print("Record number:", i)
        db_point = Record.query.get(i) or Record(id=i)

        # assign column values
        print("Assigning values")
        db_point.datetime = time
        db_point.value = value

        # commit record to database
        print("Committing")
        db.session.add(db_point)
        db.session.commit()
        i += 1

    db.session.commit()
    return 'Data refreshed!'


@APP.route('/')
def root():

    # get air quality data
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    # list of dictionaries
    # each line/dictionary is a data point for a given location and time
    data = body["results"]

    # create a list of tuples containing datetimes and air quality value
    time_list = []

    for point in data:
        time = point["date"]["utc"]
        value = point["value"]
        time_list.append((time, value))

    # # enable this code to pull info and create records on the root/home page
    # # store our tuples in a database
    # i=1
    # for point in time_list:
    #     print("Record number:", i)
    #     # initialize record
    #     db_point = Record.query.get(i) or Record(id = i)

    #     print("Assigning values")

    #     # assign column values
    #     db_point.datetime = point[0]
    #     db_point.value = point[1]

    #     print("Committing")
    #     db.session.add(db_point)
    #     db.session.commit()
    #     i += 1

    # filter records for areas with a pm greater than some threshol
    threshold = 10
    high_risk = Record.query.filter(Record.value >= threshold).all()
    message = "Here are the records for LA that have a pm greater than {}".format(threshold)
    
    return render_template("records.html", records = high_risk, message=message)
