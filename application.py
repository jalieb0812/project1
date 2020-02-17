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
    if request.method == "GET":
        return render_template("booksearch.html")

    if request.method == "POST":

        books = db.execute("SELECT * FROM books").fetchall()



        isbn = request.form.get("isbn")

        title = request.form.get("title")
        author = request.form.get("author")

        #book_id= db.execute("SELECT book_id, isbn, title, author, year FROM books WHERE \
        #isbn= :isbn", { "isbn": isbn}).fetchall()

        matches= db.execute("SELECT book_id, isbn, title, author, year FROM books WHERE \
        isbn= :isbn OR title= :title OR author= :author" , { "isbn": isbn, "title": title, "author": author} ).fetchall()

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
        print(f"this is the id: {data['books'][0]['id']}")
        print("working?")



        return redirect("booksearchresult.html", book_id=book_id, title_matches=title_matches, matches=matches, author_matches=author_matches, isbn=isbn, isbn_matches=isbn_matches, data=data)

@app.route("/booksearchresult", methods=["POST"])
#@login_required
def booksearchresult():

        isbn = request.form.get("isbn")
        title = request.form.get("title")
        author = request.form.get("author")



        #book_id= db.execute("SELECT book_id, isbn, title, author, year FROM books WHERE \
        #isbn= :isbn", { "isbn": isbn}).fetchall()

        matches= db.execute("SELECT book_id, isbn, title, author, year FROM books WHERE \
        isbn= :isbn OR title= :title OR author= :author" , { "isbn": isbn, "title": title, "author": author} ).fetchall()

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



        return render_template("booksearchresult.html", book_id=book_id, title_matches=title_matches, matches=matches, author_matches=author_matches, isbn=isbn, isbn_matches=isbn_matches)
@app.route("/book/<isbn>",  methods=["GET", "POST"])
#@login_required
def book(isbn):



    if request.method=="GET":

        #isbn=request.args.get('isbn')
        books = db.execute("SELECT * FROM books").fetchall()


        print(isbn)

        print(f"this is the second isbn number in get is {isbn}")

        bookinfo= db.execute("SELECT book_id, isbn, title, author, year FROM books WHERE \
            isbn= :isbn ", { "isbn": isbn} ).fetchall()

        print(f"this is book info 1 {bookinfo[0]}")




        #isbn = db.execute("SELECT isbn FROM books WHERE isbn = :isbn ", {"isbn": isbn}).fetchone()
        print(isbn)

        key = 'BXNCOXAo2IEQ56qLvIrow'

        data=requests.get("https://www.goodreads.com/book/review_counts.json", params={'key': key, 'isbns': isbn})

        if data.status_code != 200:
            return apology("ERROR: invalid isbn number, please try another entry", 422)
        print(data)

        data=data.json()

        print(data)

        review_data = db.execute("SELECT review_text, book_rating, username FROM reviews WHERE \
            isbn= :isbn ", { "isbn": isbn} ).fetchall()



        ratings_data= db.execute("SELECT num_ratings, average_ratings FROM review_stats WHERE \
            isbn= :isbn ", { "isbn": isbn} ).fetchall()
        return render_template('book.html', data=data, isbn=isbn, bookinfo=bookinfo, review_data=review_data, ratings_data=ratings_data)




    if request.method=="POST":



        print(f"this is the isbn number in books post is {isbn}")


        book_info=db.execute("SELECT book_id, isbn, title, author, year FROM books WHERE isbn= :isbn ", { "isbn": isbn} ).fetchall()


        print(f"book info is {book_info}")

        review_text = request.form.get("book_review")
        book_rating = request.form.get("book_rating")
        book_id= book_info[0][0]
        isbn=book_info[0][1]
        title=book_info[0][2]
        author=book_info[0][3]
        year=book_info[0][4]
        id=session["user_id"]

        username=db.execute("SELECT username from users WHERE id = :id", {"id": session["user_id"]}).fetchall()
        username=str(username[0])


        db.execute("INSERT INTO reviews ( review_text, isbn, book_rating, username, id, book_id, title, author, year) VALUES( :review_text, :isbn, :book_rating, :username,  :id, :book_id, :title, :author, :year)",
        { "review_text": review_text, "isbn": isbn, "book_rating": book_rating, "username": username,  "id": id, "book_id": book_id, "title": title, "author": author, "year": year})

        db.commit()

        books = db.execute("SELECT * FROM books").fetchall()

        print(isbn)

        print(f"this is the second isbn number is {isbn}")

        for item in isbn:
            print(item)

        usernames = db.execute("SELECT username FROM users WHERE username = :username", {"username": username})

        #isbn = db.execute("SELECT isbn FROM books WHERE isbn = :isbn ", {"isbn": isbn}).fetchone()



        bookinfo= db.execute("SELECT book_id, isbn, title, author, year FROM books WHERE \
        isbn= :isbn ", { "isbn": isbn} ).fetchall()
        key = 'BXNCOXAo2IEQ56qLvIrow'

        data=requests.get("https://www.goodreads.com/book/review_counts.json", params={'key': key, 'isbns': isbn})

        review_data = db.execute("SELECT review_text, book_rating, username FROM reviews WHERE \
        isbn= :isbn ", { "isbn": isbn} ).fetchall()



        ratings_data= db.execute("SELECT num_ratings, average_ratings FROM review_stats WHERE \
        isbn= :isbn ", { "isbn": isbn} ).fetchall()

        key = 'BXNCOXAo2IEQ56qLvIrow'

        data=requests.get("https://www.goodreads.com/book/review_counts.json", params={'key': key, 'isbns': isbn})

        if data.status_code != 200:
            return apology("ERROR: invalid isbn number, please try another entry", 422)

        data=data.json()

        print(f"this is the data as of the end of book post {data}")


        return render_template('book.html', data=data, isbn=isbn, bookinfo=bookinfo, review_data=review_data, ratings_data=ratings_data)






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
    main()
 #port = int(os.environ.get("PORT", 8080))
 #app.run(host="0.0.0.0", port=port)
