from flask import Flask, render_template, flash, request, Markup
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import sys
import json
import os
import shutil
from os import path
from os import urandom
import urllib.request
from bs4 import BeautifulSoup
import operation as o
path = path.dirname(path.realpath(__file__))
app = Flask(__name__,template_folder=path+'')

#app.config['SECRET_KEY'] = '3d441f27u331c27333d331k2f3333a'
app.config['SECRET_KEY'] = urandom(24)


import tweepy
consumer_key = "klc9lTZuJfxAalGGOIXFjTbhr"
consumer_secret = "gPhGZE1j6egZSXTkyw5p3mZdem2VhNb8aHxfCae7PtPggJKF8q"
access_token = "1112587571622637568-BR4xHHlqA7L0e58zp0bKB9U6I5AFfj"
access_token_secret = "GrcusxoUGerHchMsbmdTFRw6ZHbnCcI7NTa85GL2LjDLu"


class ReusableForm(Form):
    inp1 = TextField("How many days of monitoring?")
    inp2 = TextField("AVG(PM2.5) µg/m3")
    inp3 = TextField("%Exceedance(24h)")


    twitter = TextField("What's your Twitter handle?")
    github = TextField("What's your Github handle?")

@app.route("/air", methods=['GET', 'POST'])
def hello():
    #form=ReusableForm()
    form= ReusableForm(request.form)
    #if len(form.errors) != 0:
       #print(form.errors)
    if request.method == 'POST':
        inp1=request.form['inp1']
        inp2=request.form['inp2']
        inp3=request.form['inp3']
        github=request.form['git']
        twitter=request.form['twitter']
        name=inp1+" "+inp2+" "+inp3
        print(name, " ", twitter, " ", github)
        try:
            if len(name) != 0:
                flash(o.input(name))
                if len(github) and len(twitter) != 0:
                 url = 'https://github.com/' + github
                 data = urllib.request.urlopen(url).read()
                 soup = BeautifulSoup(data, features='lxml')
                 fullname = soup.find('span', {'class' : 'vcard-fullname'}).string
                 username = soup.find('span', {'class' : 'vcard-username'}).string
                 flash("Github Profile: " +fullname+" (@"+username+")")

##Tweepy Tweeps
                 auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                 auth.set_access_token(access_token, access_token_secret)
                 api = tweepy.API(auth)
                 #search=request.args.get('twitter')
                 public_tweets = api.user_timeline(twitter,count=10,page=1)
                 status_list=public_tweets[0]
                 status=json.dumps(status_list._json)
                 texty_text=json.loads(status)
                 flash(texty_text['text'])
##TT Ends
            else:
                flash('Error: `inp1` in the form field is required.')
        except tweepy.error.TweepError:
                flash(Markup('Something went wrong while looking for tweets, pls ask the admin. <a href="http://ankesh.ml/contact" class="alert-link">here</a>'))
    return render_template('index.html',form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
