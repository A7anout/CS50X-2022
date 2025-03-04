import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    stocks = db.execute("SELECT symbol, price, SUM(shares) as totalshares FROM trans WHERE user_id == ? GROUP BY  symbol", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    total = int(cash)
    for stock in stocks:
        total += int(stock["price"]) * int(stock["totalshares"])
    return render_template("index.html", stocks=stocks, cash=(cash), total=(total), usd=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if (request.method == "POST"):
        symbol = request.form.get("symbol")
        results = lookup(symbol)
        shares = request.form.get("shares")
        if (symbol == "") or (results == None):
            return apology("invalid symbol")
        elif (not shares.isnumeric()) or (int(shares) <= 0):
            return apology("invalid share")
        else:
            user_id = session["user_id"]
            cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
            price = results["price"]
            total = price * int(shares)
            if (int(cash) < total):
                return apology("baby no money")
            else:
                new_cash = cash - total
                date = datetime.datetime.now()
                db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)
                db.execute("INSERT INTO trans (user_id, symbol, status, price, shares, date) VALUES (?, ?, 'buy', ?, ?, ?)",
                           user_id, results["symbol"], price, shares, date)
                return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    stocks = db.execute("SELECT symbol, status, price, shares, date FROM trans WHERE user_id = ?", user_id)
    return render_template("history.html", stocks=stocks, usd=usd)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        results = lookup(symbol)
        if (results == None):
            return apology("invalid symbol")
        else:
            return render_template("quoted.html", name=results["name"], price=usd(results["price"]), symbol=results["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        if request.form.get("username") == "":
            return apology("inavlid unsername")
        elif request.form.get("password") == "" or request.form.get("password") != request.form.get("confirmation"):
            return apology("invalid password")
        else:
            username = request.form.get("username")
            hash = generate_password_hash(request.form.get("password"))
            try:
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
                return render_template("login.html")
            except:
                return apology("username taken")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    symbols = db.execute("SELECT symbol FROM trans WHERE user_id = ? GROUP BY symbol", user_id)
    if request.method == "POST":
        shares = request.form.get("shares")
        neg_shares = 0 - int((shares))
        symbol = request.form.get("symbol")
        price = lookup(symbol)["price"]
        date = datetime.datetime.now()
        owned = db.execute("SELECT SUM(shares) FROM trans WHERE user_id = ? AND symbol = ? GROUP BY symbol",
                           user_id, symbol)[0]["SUM(shares)"]
        if (not shares.isnumeric()) or (int(shares) <= 0) or (int(shares) > owned):
            return apology("invalid share")
        else:
            db.execute("INSERT INTO trans (user_id, symbol, status, price, shares, date) VALUES (?, ?, ?, ?, ?, ?)",
                       user_id, symbol, 'sell', price, neg_shares, date)
            cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
            new_cash = cash + (price * int(shares))
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)
            return redirect("/")
    else:
        return render_template("sell.html", symbols=symbols)