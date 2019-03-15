from flask import Flask,render_template,request,redirect,url_for
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

#keys and token access twitter Account
consumer_key='XXXXXXXXXXXXXXXXXXXXXXXXX'
consumer_secret_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
access_token='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
access_token_secret='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

#authenticating the twitter Account
auth = OAuthHandler(consumer_key, consumer_secret_key) 
auth.set_access_token(access_token, access_token_secret) 
api = tweepy.API(auth) 
 

#creating the flask object and getting searchQuerry from user
app=Flask(__name__)
@app.route("/",methods=["GET","POST"])
def index():
     if request.method=="POST":
          searchQuerry=request.form['searchValue']
          return redirect(url_for('search_index',SV=searchQuerry))#directing to the searchContent page
         
     return render_template('search.html')

         

@app.route("/search_index/<SV>")
def search_index(SV):
     public_tweets = api.search(SV,count=10)#getting the tweets from twitter Account
     #initialising the necessary variables and lists to store data 
     positiveTweetsCount=0
     positiveTweets=[]
     neutralTweetsCount=0
     neutralTweets=[]
     negativeTweetsCount=0
     negativeTweets=[]
     
     #removing the unwanted characters from tweets
     def clean_tweet(tweets):
          return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())   
     
     #analysing the polarities of tweets          
     for tweet in public_tweets:
          analysis=TextBlob(clean_tweet(tweet.text))
          if analysis.sentiment.polarity > 0:
               positiveTweetsCount+=1
               positiveTweets.append(clean_tweet(tweet.text))
               positiveTweets.append(", ")
          if analysis.sentiment.polarity==0:
               neutralTweetsCount+=1
               neutralTweets.append(clean_tweet(tweet.text))
               neutralTweets.append(", ")
          else:
               negativeTweetsCount+=1
               negativeTweets.append(clean_tweet(tweet.text))
               negativeTweets.append(", ")
     return render_template('searchContent.html',s=SV,pc=positiveTweetsCount,nc=neutralTweetsCount,ngc=negativeTweetsCount,pt=positiveTweets,nt=neutralTweets,ngt=negativeTweets)
     #returning the data from backend to the frontend     
if __name__ =="__main__":
     app.run(debug=True)




   