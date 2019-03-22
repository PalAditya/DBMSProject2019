import csv
import os
import urllib.request
import datetime
import time
import json
import random
from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Reject symbol if it starts with caret
    if symbol.startswith("^"):
        return None

    # Reject symbol if it contains comma
    if "," in symbol:
        return None

    # Query Alpha Vantage for quote
    # https://www.alphavantage.co/documentation/
    try:

        # GET CSV
        url = f"https://www.alphavantage.co/query?apikey={os.getenv('API_KEY')}&datatype=csv&function=TIME_SERIES_INTRADAY&interval=1min&symbol={symbol}"
        webpage = urllib.request.urlopen(url)

        # Parse CSV
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())

        # Ignore first row
        next(datareader)

        # Parse second row
        row = next(datareader)

        # Ensure stock exists
        try:
            price = float(row[4])
        except:
            return None

        # Return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
        return {
            "price": price,
            "symbol": symbol.upper()
        }

    except:
        return None

def liveUpdate(symbol):
    if symbol.startswith("^"):
        return None

    # Reject symbol if it contains comma
    if "," in symbol:
        return None

    # Query Alpha Vantage for quote
    # https://www.alphavantage.co/documentation/
    try:

        # GET CSV
        url = f"https://www.alphavantage.co/query?apikey={os.getenv('API_KEY')}&datatype=csv&function=TIME_SERIES_INTRADAY&interval=1min&symbol={symbol}"
        webpage = urllib.request.urlopen(url)

        # Parse CSV
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())
        # Ignore first row
        next(datareader)
        # Parse second row
        row = next(datareader)
        high=[]
        low=[]
        # Ensure stock exists
        try:
            for a in range(10):
                high.append(float(row[2]))
                low.append(float(row[3]))
                row=next(datareader)
        except:
            return None

        #print(high)
        #print(low)
        # Return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
        return {
            "high": high,
            "low": low,
            "symbol": symbol.upper()
        }

    except:
        return None

def usd(value):
    """Format value as USD."""
    try:
        return f"${value:,.2f}"
    except Exception as e:
        return value

def getSeries():
    t=time.time()
    t=t+19800
    series=[]
    series.append(str(time.strftime("%H:%M:%S",time.localtime(t))))
    for i in range (9):
        t=t-60
        series.append(str(time.strftime("%H:%M:%S",time.localtime(t))))
    print(series)
    return series

def predictHelper(symbol):
    if symbol.startswith("^"):
        return None

    # Reject symbol if it contains comma
    if "," in symbol:
        return None

    # Query Alpha Vantage for quote
    # https://www.alphavantage.co/documentation/
    try:

        # GET CSV
        url = f"https://www.alphavantage.co/query?apikey={os.getenv('API_KEY')}&datatype=csv&function=TIME_SERIES_DAILY&symbol={symbol}"
        webpage = urllib.request.urlopen(url)
        # Parse CSV
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())
        # Ignore first row
        next(datareader)
        # Parse second row
        row = next(datareader)
        data=[]
        try:
            for a in range(100):
                openp=row[1]
                high=row[2]
                low=row[3]
                close=row[4]
                volume=row[5]
                val={"open":openp,"high":high,"low":low,"close": close,"volume":volume}
                data.append(val)
            #print({"symbol":symbol,"data":data})
            return {"symbol":symbol,"data":data};
        except:
            return None

    except:
        return None

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def random_ads():
    a=1
    with open('ads.json') as f:
        data=json.load(f)
    #print(data)
    #p=[random.randint(1,len(data)) for _ in range(6)]
    #p=set(p)
    p=[1,2,3,4,5,6]
    p=set(p)
    ads={}
    for val in data.values():
        #if a in p:
        #    ads[val['symbol']]=val
        ads[val['symbol']]=val
        a=a+1
    return ads