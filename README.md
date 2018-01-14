# Tweet Sentiment Analysis V2
Based on [labeled-tweet-generator by @rhnvrm](https://github.com/rhnvrm/labeled-tweet-generator).

## Instructions

### Twitter API
You need to go [here](https://apps.twitter.com/) and sign in with your Twitter account, create an app to get the Twitter API keys we will be using in this project. Now, create a new file called `.env.json` in the project folder and copy-paste the following contents:
```
{
    "consumer_key": "<YOUR_CONSUMER_KEY>",
    "consumer_secret": "<YOUR_CONSUMER_SECRET_KEY>",
    "access_token": "<YOUR_ACCESS_TOKEN>",
    "access_token_secret": "<YOUR_ACCESS_TOKEN_SECRET>"
}
```
Replace the placeholder values with the keys you obtained from Twitter and save the file.

### Main Steps

1. Get Python 3.x installed. I'm using 3.6. I suggest to install Python using the Anaconda distribution available [here](https://www.continuum.io/downloads).
1. (Optional) Create a new virtual environment using `conda create` and activate that environment.
1. Clone this repo to your computer and change into that directory in your terminal. Note: If you followed (2), make sure you activate the environment before proceeding any further.
1. Do `pip install -r requirements.txt`. This will take a while to download the dependencies for running this project.
1. Since we're using NLTK, you need to download the NTLK datasets. For that, open REPL by typing in `python` and hitting enter. Enter the following:
    ```
    >> import nltk
    >> nltk.download()
    ```
1. The NLTK client app will appear. From here, download all the datasets (This will take a while as some of the datasets are in GBs. You can just download a part of the datasets but then, NLTK might not work well).
1. Follow the instructions above for generating Twitter API keys and to create `.env.json`.
1. Now, from your terminal, type `python app.py` to start the server. Open a browser and go to `http://localhost:5000` to see the visualization.

## Authors
1. Sangeeth Sudheer
2. Amol Suraj Mishra
3. Aadithyavarma

## Screenshots

![](https://i.imgur.com/dqlkcCP.png)

![](https://i.imgur.com/c25PJaW.png)

![](https://i.imgur.com/dPx8M05.png)

![](https://i.imgur.com/jcL2Nyb.png)
