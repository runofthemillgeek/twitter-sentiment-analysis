import os
from flask import Flask, request, render_template, jsonify
from twitter import TwitterClient

app = Flask(__name__)
# Setup the client <query string, retweets_only bool, with_sentiment bool>
api = TwitterClient('Donald Trump')


def strtobool(v):
    return v.lower() in ["yes", "true", "t", "1"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tweets')
def tweets():
    retweets_only = request.args.get('retweets_only')
    api.set_retweet_checking(strtobool(retweets_only.lower()))
    with_sentiment = request.args.get('with_sentiment')
    api.set_with_sentiment(strtobool(with_sentiment.lower()))
    query = request.args.get('query')
    api.set_query(query)
    tweetcount = int(request.args.get('tweetcount'))
    api.set_tweetcount(tweetcount)

    tweets = api.get_tweets()
    print("{} tweets".format(len(tweets)))
    return jsonify({'data': tweets, 'count': len(tweets)})


port = int(os.environ.get('PORT', 5000))
app.run(host="127.0.0.1", port=port, debug=True)
