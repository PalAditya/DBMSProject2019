from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_file
from flask_session import Session
from tempfile import mkdtemp
import smtplib
import pygal
import json
import numpy as np
import os
import datetime
import time
import atexit
import pdfkit
from bokeh.embed import components
from bokeh.plotting import figure
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import apology, login_required, lookup, usd, liveUpdate, getSeries, predictHelper, allowed_file, random_ads
from sklearn import linear_model
from apscheduler.schedulers.background import BackgroundScheduler

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters['zip'] = zip
app.jinja_env.globals.update(zip=zip)
#Configure images
UPLOAD_FOLDER = 'static/images'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("postgres://nbijlhjpeekddf:f375c34ecc857deef29fa138f22255f09cd8dc838cb00484d0a77c210ac3ddf7@ec2-75-101-131-79.compute-1.amazonaws.com:5432/de9nhilj3vjb53")

def sendmail(message,sender,receiver,password):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender, password)
    #s.login(os.environ.get("id"), os.environ.get("pass"))
    s.sendmail(sender, receiver, message)
    s.quit()
    #print("Sent")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    try:
        # look up the current user
        users = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        stocks = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])
        quotes = {}
        predictedPrices=db.execute("SELECT symbol, price FROM predictions WHERE symbol IN (SELECT symbol FROM transactions WHERE user_id=:user_id)",
                                    user_id=session["user_id"])
        spmap={}
        a=0
        for val in predictedPrices:
            spmap[val["symbol"]]=a
            a=a+1
        for stock in stocks:
            quotes[stock["symbol"]] = lookup(stock["symbol"])
            if quotes[stock["symbol"]] is None:
                continue
            print(stock["symbol"])
            if stock["symbol"] in spmap:
                quotes[stock["symbol"]+"p"]=predictedPrices[spmap[stock["symbol"]]]["price"]
            else:
                quotes[stock["symbol"]+"p"]=0
        #print(quotes)
        cash_remaining = users[0]["cash"]
        total = cash_remaining
        #sendmail()
        x=db.execute("SELECT Symbol,SUM(ABS(shares)) as t FROM transactions WHERE created_at >= date('now','-1 day') GROUP BY symbol ORDER BY t DESC LIMIT 3")
        t="Today's most trending shares are: "+x[0]["symbol"]+" with "+str(x[0]["t"])+" transactions, "+x[1]["symbol"]+" wi"\
        "th "+str(x[1]["t"])+" transactions and "+x[2]["symbol"]+" with "+str(x[2]["t"])+" transactions"
        flash(t)
        if quotes is None or stocks is None:
            return apology("Something went wrong, please access the page a little later")
        return render_template("portfolio.html", quotes=quotes, stocks=stocks, total=total, cash_remaining=cash_remaining)
    except Exception as e:
        print(e)
        val=random_ads()
        ads1=dict(list(val.items())[0:2])
        ads2=dict(list(val.items())[2:4])
        ads3=dict(list(val.items())[4:6])
        return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)


@app.route("/ads",methods=["GET", "POST"])
@login_required
def ads():
    if request.method == 'POST':
        symbol=request.form.get("symbol").upper()
        image=request.files["image"]
        if image.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        alttext=request.form.get("alttext")
        desc=request.form.get("desc")
        link=request.form.get("link")
        priority=request.form.get("priority")
        duration=request.form.get("duration")
        imagesource="/static/images/"+image.filename
        try:
            db.execute("DELETE FROM advertisement WHERE symbol=:symbol",symbol=symbol)
            db.execute("INSERT INTO advertisement(symbol,imagesource,alttext,description,link,priority,duration) VALUES (:symbol,:imagesource,:alttext,:description,:link,:priority,:duration)",
                    symbol=symbol,imagesource=imagesource,alttext=alttext,description=desc,link=link,priority=priority,duration=duration)

            #Cost formula=300*priority+100*duration
            rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
            money=rows[0]["cash"]#check balance
            if money<priority*300+duration*100:
                flash("Not enough money!")
                return render_template("ads.html")
            else:
                new_cash=money-(priority*300+duration*100)
                db.execute("UPDATE users SET cash=:cash WHERE id=:user_id",cash=new_cash,user_id=session["user_id"])
        except Exception as e:
            print(e)
        val=random_ads()
        ads1=dict(list(val.items())[0:2])
        ads2=dict(list(val.items())[2:4])
        ads3=dict(list(val.items())[4:6])
        return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
    return render_template("ads.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    val=random_ads()
    ads1=dict(list(val.items())[0:2])
    ads2=dict(list(val.items())[2:4])
    ads3=dict(list(val.items())[4:6])
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        # Check if the symbol exists
        if quote == None:
            return apology("invalid symbol", 400)

        # Check if shares was a positive integer
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)

        # Check if # of shares requested was 0
        if shares <= 0:
            return apology("can't buy less than or 0 shares", 400)

        # Query database for username
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # How much $$$ the user still has in her account
        cash_remaining = rows[0]["cash"]
        price_per_share = quote["price"]

        # Calculate the price of requested shares
        total_price = price_per_share * shares

        if total_price > cash_remaining:
            return apology("not enough funds")

        # Book keeping (TODO: should be wrapped with a transaction)
        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share) VALUES(:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"],
                   symbol=request.form.get("symbol"),
                   shares=shares,
                   price=price_per_share)

        flash("Bought!")
        return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
    else:
        return render_template("buy.html",ads1=ads1,ads2=ads2,ads3=ads3)


@app.route("/addFriend",methods=["GET", "POST"])
@login_required
def addFriend():
    """Allows to add a friend"""
    val=random_ads()
    ads1=dict(list(val.items())[0:2])
    ads2=dict(list(val.items())[2:4])
    ads3=dict(list(val.items())[4:6])
    if request.method == "POST":
        newid=request.form.get("friend")
        newid=int(newid,10)
        all_users=db.execute("SELECT id FROM users")
        present=0
        for user in all_users:
            #print(user["id"])
            #print(newid)
            if user["id"]==newid:
                present=1
                break;
        if present==0:
            return apology("Sorry, we can't find that user");
        val=db.execute("SELECT * FROM friends WHERE uid=:user_id",user_id=session["user_id"])
        #print(val);
        if not val:
            db.execute("INSERT INTO friends VALUES (:uid,:f1,:f2,:f3,:f4,:f5)",uid=session["user_id"]
            ,f1=newid,f2=None,f3=None,f4=None,f5=None)
            return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
        else:
            if val[0]["f1"] is None:
                db.execute("UPDATE friends SET f1=:f1 WHERE uid=:user_id",f1=newid,user_id=session["user_id"])
                return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
            elif val[0]["f2"] is None:
                if val[0]["f1"]==newid:
                    flash("Already Added")
                    return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
                db.execute("UPDATE friends SET f2=:f1 WHERE uid=:user_id",f1=newid,user_id=session["user_id"])
                return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
            elif val[0]["f3"] is None:
                if val[0]["f2"]==newid or val[0]["f1"]==newid:
                    flash("Already Added")
                    return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
                db.execute("UPDATE friends SET f3=:f1 WHERE uid=:user_id",f1=newid,user_id=session["user_id"])
                return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
            elif val[0]["f4"] is None:
                if val[0]["f3"]==newid or val[0]["f2"]==newid or val[0]["f1"]==newid:
                    flash("Already Added")
                    return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
                db.execute("UPDATE friends SET f4=:f1 WHERE uid=:user_id",f1=newid,user_id=session["user_id"])
                return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
            elif val[0]["f5"] is None:
                if val[0]["f4"]==newid or val[0]["f3"]==newid or val[0]["f2"]==newid or val[0]["f1"]==newid:
                    flash("Already Added")
                    return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
                db.execute("UPDATE friends SET f5=:f1 WHERE uid=:user_id",f1=newid,user_id=session["user_id"])
                return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
        return apology("You exceeded maximum number of friends", 400)
    return render_template("addFriend.html",ads1=ads1,ads2=ads2,ads3=ads3)

@app.route("/deleteFriend",methods=["GET", "POST"])
@login_required
def deleteFriend():
    val=random_ads()
    ads1=dict(list(val.items())[0:2])
    ads2=dict(list(val.items())[2:4])
    ads3=dict(list(val.items())[4:6])
    if request.method == "POST":
        newid=request.form.get("friend")
        newid=int(newid,10)
        val=db.execute("SELECT * FROM friends WHERE uid=:user_id",user_id=session["user_id"])
        if not val:
            return apology("You haven't added any friends yet");
        else:
            if newid==val[0]["f1"]:
                db.execute("UPDATE friends SET f1=:f1 WHERE uid=:user_id",f1=None,user_id=session["user_id"])
                return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
            if newid==val[0]["f2"]:
                db.execute("UPDATE friends SET f2=:f1 WHERE uid=:user_id",f1=None,user_id=session["user_id"])
                return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
            if newid==val[0]["f3"]:
                db.execute("UPDATE friends SET f3=:f1 WHERE uid=:user_id",f1=None,user_id=session["user_id"])
                return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
            if newid==val[0]["f4"]:
                db.execute("UPDATE friends SET f4=:f1 WHERE uid=:user_id",f1=None,user_id=session["user_id"])
                return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
            if newid==val[0]["f5"]:
                db.execute("UPDATE friends SET f5=:f1 WHERE uid=:user_id",f1=None,user_id=session["user_id"])
                return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
        return apology("Sorry, that person was not in your friend list")
    return render_template("deleteFriend.html",ads1=ads1,ads2=ads2,ads3=ads3)

@app.route("/messageFriend",methods=["GET", "POST"])
@login_required
def messageFriend():
    val=random_ads()
    ads1=dict(list(val.items())[0:2])
    ads2=dict(list(val.items())[2:4])
    ads3=dict(list(val.items())[4:6])
    if request.method == "POST":
        message=request.form.get("friend")
        password=request.form.get("password")
        val=db.execute("SELECT * FROM friends WHERE uid=:user_id",user_id=session["user_id"])
        set1=set()
        list1=[]
        myEmail=""
        if val[0]["f1"] is not None:
            set1.add(val[0]["f1"]);
        if val[0]["f2"] is not None:
            set1.add(val[0]["f2"]);
        if val[0]["f3"] is not None:
            set1.add(val[0]["f3"]);
        if val[0]["f4"] is not None:
            set1.add(val[0]["f4"]);
        if val[0]["f5"] is not None:
            set1.add(val[0]["f5"]);
        val=db.execute("SELECT id, email FROM users");
        for user in val:
            if user["id"] in set1:
                list1.append(user["email"])
            if user["id"]==session["user_id"]:
                myEmail=user["email"];
        #print(list1)
        for a in list1:
            sendmail(message,myEmail,a,password)
        return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)
    return render_template("messageFriend.html",ads1=ads1,ads2=ads2,ads3=ads3)

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute(
        "SELECT symbol, shares, price_per_share, created_at FROM transactions WHERE user_id = :user_id ORDER BY created_at ASC", user_id=session["user_id"])
    try:
        #print(request.url)
        x=render_template("history.html", transactions=transactions)
        print(x)
        x=x.split()
        x=x[:len(x)-39]
        x.append('</main>')
        x.append("</body>")
        x.append("</html>")
        x=" ".join(x)
        config=pdfkit.configuration(wkhtmltopdf='../../wkhtmltox/bin/wkhtmltopdf')
        pdfkit.from_string(x,'out.pdf',configuration=config)
        #pdfkit.from_url(request.url,'out.pdf',configuration=config)
    except Exception as e:
        print(e)
    return render_template("history.html", transactions=transactions)


@app.route("/funds/add", methods=["GET", "POST"])
@login_required
def add_funds():

    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
        except:
            return apology("amount must be a real number", 400)

        db.execute("UPDATE users SET cash = cash + :amount WHERE id = :user_id", user_id=session["user_id"], amount=amount)
        return redirect(url_for("index"))
    else:
        return render_template("add_funds.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow user to change her password"""

    if request.method == "POST":

        # Ensure current password is not empty
        if not request.form.get("current_password"):
            return apology("must provide current password", 400)

        # Query database for user_id
        rows = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Ensure current password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("current_password")):
            return apology("invalid password", 400)

        # Ensure new password is not empty
        if not request.form.get("new_password"):
            return apology("must provide new password", 400)

        # Ensure new password confirmation is not empty
        elif not request.form.get("new_password_confirmation"):
            return apology("must provide new password confirmation", 400)

        # Ensure new password and confirmation match
        elif request.form.get("new_password") != request.form.get("new_password_confirmation"):
            return apology("new password and confirmation must match", 400)

        # Update database
        hash = generate_password_hash(request.form.get("new_password"))
        rows = db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", user_id=session["user_id"], hash=hash)

        # Show flash
        flash("Changed!")

    return render_template("change_password.html")


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect(url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/download", methods=["GET", "POST"])
@login_required
def download():
    try:
        return send_file('out.pdf',attachment_filename='transactions.pdf')
    except Exception as e:
        print(e)
    val=random_ads()
    ads1=dict(list(val.items())[0:2])
    ads2=dict(list(val.items())[2:4])
    ads3=dict(list(val.items())[4:6])
    return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("index"))


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("invalid symbol", 400)
        res=liveUpdate(request.form.get("symbol"))
        #print("RES")
        #print(res)
        graph = pygal.Line()
        graph.title = 'Updates of '+request.form.get("symbol")
        graph.x_labels = ['1','2','3','4','5','6','7','8','9','10']
        graph.add(request.form.get("symbol")+":high",res["high"])
        graph.add(request.form.get("symbol")+":low",res["low"])
        graph_data = graph.render_data_uri()
        return render_template("quoted.html", quote=quote,graph_data=graph_data)
    # User reached route via GET (as by clicking a link or via redi)
    else:
        val=random_ads()
        ads1=dict(list(val.items())[0:2])
        ads2=dict(list(val.items())[2:4])
        ads3=dict(list(val.items())[4:6])
        return render_template("quote.html",ads1=ads1,ads2=ads2,ads3=ads3)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        if not request.form.get("email"):
            return apology("must provide email id", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # hash the password and insert a new user in the database
        hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO users (username, hash, email) VALUES(:username, :hash, :email)",
                                 username=request.form.get("username"),
                                 hash=hash, email=request.form.get("email"))

        # unique username constraint violated?
        if not new_user_id:
            return apology("username taken", 400)
        # Remember which user has logged in
        session["user_id"] = new_user_id
        # Display a flash message
        flash("Registered!")
        # Redirect user to home page
        return redirect(url_for("index"))
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/live")
@login_required
def chart():
    val=db.execute("SELECT symbol, count(shares) FROM Transactions WHERE user_id=:user_id GROUP BY symbol ORDER BY count(shares) DESC LIMIT 5",
    user_id=session["user_id"]);
    scripts=[]
    divs=[]
    for value in val:
        res=liveUpdate(value["symbol"]);
        if res is None:
            continue
        p=figure(plot_width=400, plot_height=400, sizing_mode='scale_width')
        p.line(["1","2","3","4","5","6","7","8","9","10"],res["high"],line_width=2, color="navy", alpha=1,legend="High:"+value["symbol"])
        p.line(["1","2","3","4","5","6","7","8","9","10"],res["low"],line_width=2,color="orange",alpha=1,legend="Low:"+value["symbol"])
        script,div=components(p);
        scripts.append(script)
        divs.append(div)
    values=list(zip(scripts, divs))
    if len(scripts)==0:
        return apology("Sorry, we can't seem to connect to server right now")
    return render_template("live.html",values=values,width=100/len(scripts))

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    val=random_ads()
    ads1=dict(list(val.items())[0:2])
    ads2=dict(list(val.items())[2:4])
    ads3=dict(list(val.items())[4:6])
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        # Check if the symbol exists
        if quote == None:
            return apology("invalid symbol", 400)

        # Check if shares was a positive integer
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)

        # Check if # of shares requested was 0
        if shares <= 0:
            return apology("can't sell less than or 0 shares", 400)

        # Check if we have enough shares
        stock = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol GROUP BY symbol",
                           user_id=session["user_id"], symbol=request.form.get("symbol"))

        if len(stock) != 1 or stock[0]["total_shares"] <= 0 or stock[0]["total_shares"] < shares:
            return apology("you can't sell less than 0 or more than you own", 400)

        # Query database for username
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # How much $$$ the user still has in her account
        cash_remaining = rows[0]["cash"]
        price_per_share = quote["price"]

        # Calculate the price of requested shares
        total_price = price_per_share * shares

        # Book keeping (TODO: should be wrapped with a transaction)
        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share) VALUES(:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"],
                   symbol=request.form.get("symbol"),
                   shares=-shares,
                   price=price_per_share)

        flash("Sold!")

        return redirect(url_for("index"))

    else:
        stocks = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])

        return render_template("sell.html",ads1=ads1,ads2=ads2,ads3=ads3)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

def predict():
    shares=db.execute("SELECT DISTINCT symbol FROM transactions")
    d={}
    a=0
    for share in shares:
        d[str(a)]=predictHelper(share["symbol"])
        a=a+1
    #print(d)
    with open('data.json','w') as outfile:
        json.dump(d,outfile)

def regress():
    try:
        db.execute("DELETE FROM predictions");
        with open('data.json') as f:
            c=json.load(f);
        for val in c.values():
            X=[]
            y=[]
            symbol=val["symbol"]
            for data in val["data"]:
                x=[]
                x.append(float(data["open"]))
                x.append(float(data["high"]))
                x.append(float(data["low"]))
                y.append(float(data["close"]))
                #x.append(float(data["volume"]))
                X.append(x)
            #reg = linear_model.LinearRegression()
            b=X[99]
            X=np.array(X)
            y=np.array(y)
            xt=X.transpose()
            X=np.matmul(xt,X);
            X=np.linalg.pinv(X)
            y=np.matmul(xt,y)
            coef=np.matmul(X,y)
            a=np.dot(b,coef)
            a=float(str(a)[0:5])
            db.execute("INSERT INTO predictions (symbol,price) VALUES (:symbol,:price)",symbol=symbol,price=a)
        #print("Done")
    except Exception as e:
        print(e)

def get_ads():
    rows=db.execute("SELECT * FROM advertisement")
    val={}
    for row in rows:
        temp_dict={}
        temp_dict['symbol']=row['symbol']
        temp_dict['img']=row['imagesource']
        temp_dict['alt']=row['alttext']
        temp_dict['desc']=row['description']
        temp_dict['link']=row['link']
        now=datetime.datetime.now()
        creation=datetime.datetime.strptime(row["created"],"%Y-%m-%d %H:%M:%S")
        diff=now-creation
        diff_h=diff.total_seconds()//3600
        if diff_h<row["duration"]:
            val[row['symbol']]=temp_dict
    with open('ads.json','w') as outfile:
        json.dump(val,outfile)

#run cron jobs
scheduler = BackgroundScheduler()
scheduler.add_job(func=predict, trigger="interval", seconds=3600)
scheduler.add_job(func=get_ads, trigger="interval", seconds=3600)
scheduler.add_job(func=regress, trigger="interval", seconds=3720)
scheduler.start()