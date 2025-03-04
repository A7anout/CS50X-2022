from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]["username"]
    return render_template("index.html", username=username)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("invalid password")
        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
            return render_template("login.html")
        except:
            return apology("username taken")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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


@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/list", methods=["GET", "POST"])
@login_required
def lists():
    user_id = session["user_id"]
    lists = db.execute("SELECT id, description, due, importance FROM lists WHERE user_id = ?", user_id)
    # Add a button to let the user delete an event
    if request.method == "POST":
        idd = request.form.get("idd")
        if idd:
            db.execute("DELETE FROM lists WHERE id = ?", idd)
            return redirect("/list")
    else:
        return render_template("list.html", lists=lists)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    user_id = session["user_id"]
    if request.method == "POST":
        description = request.form.get("description")
        due = request.form.get("due")
        importance = request.form.get("importance")
        db.execute("INSERT INTO lists (user_id, description, due, importance) VALUES(?, ?, ?, ?)", user_id, description, due, importance)
        return redirect("/list")
    else:
        return render_template("add.html")