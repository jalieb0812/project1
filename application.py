import os

from flask import Flask, session, jsonify, redirect, render_template, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime, date

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
#@login_required
def index():
    return render_template("index.html")


@app.route("/check", methods=["GET"])
def check():

    username = request.args.get("username")

    usernames = db.execute("SELECT username FROM users WHERE username = :username", {"username": username}).fetchall()

    if not usernames and username:
        print("what the heck")
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        username=request.form.get("username")
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          {"username": username}).fetchall()
                          #username=request.form.get("username"))

        # Ensure username exists and password is correct
        if  rows is None or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]




        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():

 # User reached route via POST (as by submitting a form via POST)
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        rows = db.execute("SELECT username FROM users")  # Query database for username

        # check username entered
        if not request.form.get("username"):
            return apology("choose a user name", 400)

        username = request.form.get("username")

        print(username)

        #if check() == jsonify(False):
            #return apology("sorry username unavialble; choose a user name", 400)

        usernames = db.execute("SELECT username FROM users WHERE username = :username", {"username": username})

        print(usernames)
        # check if username taken
        #if usernames:
            #return apology("sorry username unavialble; choose a user name", 400)

        for name in rows:
            if request.form.get("username") == name:
                return apology("username exists choose a new one", 400)

        if not request.form.get("password"):
            return apology("make a password", 400)

        if not request.form.get("confirmation"):
            return apology("confirm password", 400)

        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords dont match", 400)

        hash = generate_password_hash(request.form.get("password"),  "sha256")

        username = request.form.get("username")
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                   {"username": username, "hash": hash})
        db.commit()


        session.get("user_id")

        return redirect("/login")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


if __name__ == "__main__":
 port = int(os.environ.get("PORT", 8080))
 app.run(host="0.0.0.0", port=port)
