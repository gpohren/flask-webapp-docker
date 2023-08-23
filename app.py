from crypt import methods
from urllib import request
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import sqlalchemy as sa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Iniatialize the database
db = SQLAlchemy(app)

# Create database model
class Friends(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(200), nullable=False)
    date_created = sa.Column(sa.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# Create a function to return a string when we add something
    def __repr__(self):
        return '<Name %r>' % self.id

subscribers = []

@app.route('/')
def index():
    title = "Home"
    return render_template("index.html", title=title)

@app.route('/about')
def about():
    title = "About"
    return render_template("about.html", title=title)

@app.route('/friends', methods=['POST', 'GET'])
def friends():
    title = "Friends"

    if request.method == "POST":
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)

        # Push to database
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error adding your friend"    

    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template("friends.html", title=title, friends=friends)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == "POST":
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was a problem updating"
    else:
        return render_template('update.html', friend_to_update=friend_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "There was a problem deleting"

@app.route('/subscribe')
def subscribe():
    title = "Subscribe"
    return render_template("subscribe.html", title=title)

@app.route('/form', methods=["POST"])
def form():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        error_statement = "All fields required"
        return render_template("subscribe.html", 
            error_statement=error_statement,
            name=name,
            email=email)

    subscribers.append(f"{name} - {email}")
    title = "Thank you!"
    return render_template("form.html", title=title, subscribers=subscribers)