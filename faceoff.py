import json
import tweepy
import urllib
import cv2
import wget
import time
import random
import re


def CheckForFace(filename, username):
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = cv2.CascadeClassifier("haarcascade_frontalface_default.xml").detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    if len(faces) == 0:
        print("No face found for user: " + username)
    else:
        print("Face detected for user: " +username)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("Face found for user: "+username, image)
        cv2.waitKey(0)


def DownloadPhoto(profilephoto, username):
    print('Downloading photo')
    url = profilephoto
    filename = 'photo_of_' + username + '.jpg'
    wget.download(url, filename)
    print('\nSaved photo locally as: ' + filename)
    time.sleep(1)
    CheckForFace(filename, username)

def GetTweets():
    # enter your twitter api details here: https://developer.twitter.com/en/apps
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # anything that will return a lot of results
    search = ['the', 'and', 'a', 'but', 'lol']
    term = random.randint(0, len(search)-1)

    # set this for how many results you want to get from Twitter (1-100)
    # Twitter API rate info: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
    results_to_get = 10

    for tweet in tweepy.Cursor(api.search, q=search[term], lang="en").items(results_to_get):
        tweet_json = json.loads(json.dumps(tweet._json))
        username = tweet_json['user']['name']
        username = re.sub('[^A-Za-z0-9]+', '', username)
        profilephoto = tweet_json['user']['profile_image_url_https']
        profilephoto = profilephoto.replace("_normal", "")
        DownloadPhoto(profilephoto, username)

GetTweets()
