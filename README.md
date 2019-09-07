# DBMS Project for semester 6.  
Inspired by **Pset7**, *CS50-2018*  

The Flask app is configured to run on a CS50 IDE.  
To run it locally, there are a few steps.  
- Use **pip install -r requirements.txt**
- Use **set FLASK_APP=application.py** (Windows) and **export FLASK_APP=application.py** (Linux/MAC)
- Change the line *db = SQL("sqlite:///finance.db")* to make it use your own local/online sqlite instance (Use *sqlite_setup.py* for a local instance, which can be downloaded from [here](https://www.sqlite.org/download.html))
- Set your gmail settings to allow *less secure* apps (only if you want to test the email feature-Explained later)

Now, you're good to go :smile:

The live demo is hosted at [heroku](https://database-lab-app.herokuapp.com/) :grinning:

The various features of the webapp are: 
- Profile creation
- Querying the current price of some share
- Buying and selling the shares directly
- Seeing a graphical overview of the fluctuation in share prices over time
- Predicted prices of shares held by the user
- History of transactions
- Tabular representation of current shares
- Adding friends to maintain a trusted list and sending mails to them 
- Viewing the most trending shares on that particular day
- Companies can place ads for their shares on the platform for a price

|URL|Function|
|---------|------------|
login|Allows user to log in
register|User Registration
download|Downloads history of transactions in PDF format
index|Shows curren shares
addFriend, deleteFriend and messageFriend|Adds, removes and messages a user to/from/on the friend list
quote|See current price of a share
buy, sell| Buy or sell n particular shares
live|See updates of user's most important shares graphically
ads|Allows companies to place ads
funds/add|Allows users to add money to their account
change_password|Password change facilitated

Here are a few images to explain the flow in more detail :smile:

- The user is greeted with a list of his/her available stocks on logging in  

![portfolio_1](https://user-images.githubusercontent.com/25523604/64475106-c95d9400-d19b-11e9-9da4-4691a44f806c.PNG)

- Buying a stock  

![Buying](https://user-images.githubusercontent.com/25523604/64475063-4b00f200-d19b-11e9-98b0-99defd622f8d.PNG)

- You can see that a share of NetFlix was bought on the updated interface

![portfolio_2](https://user-images.githubusercontent.com/25523604/64475169-a1bafb80-d19c-11e9-9c53-4beb5f2abe50.PNG)

- Did I mention that we can get *list of all transactions*? The history tab supports it, alongside providing facility for downloading the report in PDF format

![portfolio_with_pdf_download](https://user-images.githubusercontent.com/25523604/64475188-f2caef80-d19c-11e9-82ef-859054d6074a.PNG)

- The interface for companies to upload ads

![interface](https://user-images.githubusercontent.com/25523604/64475195-0d9d6400-d19d-11e9-9d41-ba5657b5c345.PNG)

- The share prices for a company over the past 10 minutes (can be configured) via Pygal.

![live_updates](https://user-images.githubusercontent.com/25523604/64475217-5c4afe00-d19d-11e9-96db-1d6e765ac82f.PNG)

- The share prices of companies the user holds most shares of over past 10 minutes (can be cofigured) via Bokeh. Can add AjaxDataSource to make it auto-updating

![live_stream](https://user-images.githubusercontent.com/25523604/64475271-37a35600-d19e-11e9-95fd-97cfa105bd4c.PNG)

- Finlly, the error page (classic cat for the *CS50* touch)

![Error](https://user-images.githubusercontent.com/25523604/64475286-7802d400-d19e-11e9-8ddc-72da3565a085.PNG)
