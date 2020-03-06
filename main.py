from data import db_session
from sqlalchemy import or_
from flask import Flask, render_template, redirect, request
from data import jobs
from data import users

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'


@app.route('/')
def index():
    db_session.global_init("db/mars_explorer.db")
    sessions = db_session.create_session()
    jobs2 = sessions.query(jobs.Jobs)
    return render_template("Journal_works.html", jobs=jobs2)


if __name__ == "__main__":
    app.run()
