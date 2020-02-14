import os


from flask import Flask, session, jsonify, redirect, render_template, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash



from helpers import apology, login_required
from datetime import datetime, date

import requests
#from goodreads import *


"""
# set DATABASE_URL postgres://cdrljlpkrqgdal:ac57ec3da706c0b5958d7132cb40b44f2473249664d7e1c746400a7520c406b9@ec2-174-129-43-40.compute-1.amazonaws.com:
5432/dfihju0alucdaq

host ec2-174-129-43-40.compute-1.amazonaws.com
Database dfihju0alucdaq
User cdrljlpkrqgdal
Port 5432
Password  ac57ec3da706c0b5958d7132cb40b44f2473249664d7e1c746400a7520c406b
Heroku CLI heroku pg:psql postgresql-pointy-42116 --app jobookap
FLASK_APP=application.py

"""
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

    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("index.html", books=books)

#    if session.user_id:
#        return render_template('booksearch.html')



@app.route("/check", methods=["GET"])
def check():

    username = request.args.get("username")

    usernames = db.execute("SELECT username FROM users WHERE username = :username", {"username": username}).fetchall()

    if not usernames and username:
        print("what the heck")
        return jsonify(True)
    else:
        return jsonify(False)

@app.route("/booksearch", methods=["GET", "POST"])


#@login_required
def booksearch():

    if request.method == "POST":

        books = db.execute("SELECT * FROM books").fetchall()

        print(books[1])

        isbn = request.form.get("isbn")

        title = request.form.get("title")
        author = request.form.get("author")

        #book_id= db.execute("SELECT book_id, isbn, title, author, year FROM books WHERE \
        #isbn= :isbn", { "isbn": isbn}).fetchall()

        isbn_matches = db.execute("SELECT book_id, isbn, title, author, year FROM books WHERE \
        isbn= :isbn", { "isbn": isbn}).fetchall()

        #isbn=isbn_matches

        print(isbn_matches)
        print(f"this is the number: {isbn}")



        title_matches = db.execute("SELECT book_id, title, isbn, author, year FROM books WHERE \
            title= :title",{ "title": title}).fetchall()

        author_matches = db.execute("SELECT book_id, author, title, isbn, year FROM books WHERE \
             author= :author ",{ "author": author}).fetchall()

        book_id = db.execute("SELECT book_id FROM books WHERE \
            title= :title", { "title": title}).fetchall()



    #{Outside_Counsel_Defendant_Attorney} {Opposing_Counsel_Plaintiff_Attorney}")
    #

        key = 'BXNCOXAo2IEQ56qLvIrow'

        data=requests.get("https://www.goodreads.com/book/review_counts.json", params={'key': key, 'isbns': isbn})

        data=data.json()

        print(data)
        print(f"this is the id: {data['books'][0]['id']}")
        print("working?")
        return render_template("booksearchresult.html", book_id=book_id, title_matches=title_matches,author_matches=author_matches, isbn=isbn, isbn_matches=isbn_matches, data=data)
    else:
        return render_template("booksearch.html")


    #rows = = db.execute("SELECT username FROM users")  # Query database for username



@app.route("/booksearchresult", methods=["GET", "POST"])
#@login_required
def booksearchresult():

    if request.method == "POST":

        isbn=isbn

        print(isbn)

        print(isbn_matches)

        #book_id=db.execute("SELECT book_id FROM books WHERE book_id = :book_id ", {"book_id": book_id}).fetchone()
        #print(book_id)

    #    isbn = db.execute("SELECT isbn FROM books WHERE book_id = :book_id ", {"book_id": book_id}).fetchone()
        #print(isbn)


        #isbns = isbn[0].strip(',')

    #title=titles[0]

    #isbn.append(isbns)

    #    print(isbns)
        #print(isbn)



    #KEY = 'cV3D4w3DRDPIeWOqgHZ20g' old

    #    key = 'BXNCOXAo2IEQ56qLvIrow'

    #res=requests.get(f"https://www.goodreads.com/book/title.json", params={'key':  'key', 'title': title})


        #data=requests.get("https://www.goodreads.com/book/review_counts.json", params={'key': key, 'isbns': isbn})

        #print(key)
    #{'key': 'KEY', 'isbns': isbns})

    #res=requests.get(f"https://www.goodreads.com/book/review_counts.json?isbns={isbns}&key={KEY}")

    #https://www.goodreads.com/book/review_counts.json

        #print(data)
        #if res.status_code != 200:
            #raise Exception("ERROR: API request unsuccessful")

    #data=res.json()


        books = db.execute("SELECT * FROM books").fetchall()

        print(isbn)

        print(f"this is the second isbn number in BOOK search is {isbn}")

        for item in isbn:
            print(item)



    #isbn = db.execute("SELECT isbn FROM books WHERE isbn = :isbn ", {"isbn": isbn}).fetchone()
        print(isbn)

        key = 'BXNCOXAo2IEQ56qLvIrow'

        data=requests.get("https://www.goodreads.com/book/review_counts.json", params={'key': key, 'isbns': isbn})

        data=data.json()

        print(data)
        print(f"this is {data.ratings_count}")
        print("working?")


        return render_template("book.html", book_id=book_id,  title_matches=title_matches, author_matches=author_matches, isbn=isbn, isbn_matches=isbn_matches, data=data)
    else:
        return render_template("booksearchresult.html")


# key: BXNCOXAo2IEQ56qLvIrow      new
# secret: kYXsLWtrfcva8ebbwoJHiQb7AzRa33rQaZFoq7Ecx0   new

#key: cV3D4w3DRDPIeWOqgHZ20g old
#secret: OC64ecQZBHhItgDe2xYq9ZnfeE4wDkt7hPS1z4VKo old


@app.route("/book/<isbn>",  methods=["GET", "POST"])
#@login_required
def book(isbn):

    if request.method=="GET":
        books = db.execute("SELECT * FROM books").fetchall()

        print(isbn)

        print(f"this is the second isbn number is {isbn}")

        for item in isbn:
            print(item)



        #isbn = db.execute("SELECT isbn FROM books WHERE isbn = :isbn ", {"isbn": isbn}).fetchone()
        print(isbn)

        key = 'BXNCOXAo2IEQ56qLvIrow'

        data=requests.get("https://www.goodreads.com/book/review_counts.json", params={'key': key, 'isbns': isbn})

        print(data)

        data=data.json()

        print(data)
        return render_template('book.html', data=data)


    if request.method=="POST":

        books = db.execute("SELECT * FROM books").fetchall()

        print(isbn)

        print(f"this is the second isbn number is {isbn}")

        for item in isbn:
            print(item)



        #isbn = db.execute("SELECT isbn FROM books WHERE isbn = :isbn ", {"isbn": isbn}).fetchone()
        print(isbn)

        key = 'BXNCOXAo2IEQ56qLvIrow'

        data=requests.get("https://www.goodreads.com/book/review_counts.json", params={'key': key, 'isbns': isbn})

        print(data.json())


        return render_template('book.html', data=data)






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
        return redirect("/booksearch")

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
    main()
 #port = int(os.environ.get("PORT", 8080))
 #app.run(host="0.0.0.0", port=port)
