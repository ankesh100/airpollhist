from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import sys
import json
import os
import shutil
from os import path
from os import urandom
import urllib.request
from bs4 import BeautifulSoup
from scraper import AdvancedSearchScraper
import operation as o
path = path.dirname(path.realpath(__file__))
app = Flask(__name__,template_folder=path+'')

#app.config['SECRET_KEY'] = '3d441f27u331c27333d331k2f3333a'
app.config['SECRET_KEY'] = urandom(24)

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
        if len(name) != 0:
            flash(o.input(name))
            if len(github) and len(twitter) != 0:
             url = 'http://github.com/' + github
             data = urllib.request.urlopen(url).read()
             soup = BeautifulSoup(data)
             fullname = soup.find('span', {'class' : 'vcard-fullname'}).string
             username = soup.find('span', {'class' : 'vcard-username'}).string
             twitter_user = AdvancedSearchScraper(twitter, 1)
             tweets = twitter_user.scrape()
             flash("Latest Tweet : "+ json.dumps(tweets[0]["tweet_text"]) + " Retweets : "+json.dumps(tweets[0]["retweets"])+" Likes : "+json.dumps(tweets[0]["favorites"]))
             flash("Github Profile: " +fullname+" (@"+username+")")
        else:
            flash('Error: `inp1` in the form field is required.')

    return render_template('index.html',form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
