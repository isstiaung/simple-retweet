# simple-retweet
A simple app to get tweets from the same day last and retweet
This project is quite specific to my requirements, I used to auto tweet through medium and that went out as medium links, which means that traffic doesn't go to my blog, it goes to my medium profile, which I no longer use.

Referred to : [this gist](https://gist.github.com/alexdeloy/fdb36ad251f70855d5d6) to put this together (tbh most of it was already there)

### System Requirements
I built this on OSX but, this is built is with [python2.7](https://www.python.org/download/releases/2.7/), you would also need pip and virtualenv, which should be the fundamental requirements to take care of before going forward.

### Setup
* Clone the directory - In case you can't find the link [here you go](https://github.com/isstiaung/simple-retweet.git)
* Create a virtualenv - [Here's a neat how to](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
* Activate the environment  - use the previous link to find out how
* Get the requirements using pip  - in bash `pip install -r requirements.txt`
* Copy config_skeleton.py to config.py  - in bash `cp config_skeleton.py config.py`
* Fill in the 4 required consumer keys and access tokens
* Fill in your username and the link to a medium blog that you might have had
* Run in bash : `python py/get_last_year_tweets.py`
