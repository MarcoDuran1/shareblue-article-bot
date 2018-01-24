from bs4 import BeautifulSoup
import requests
import re
import praw
import time


def scrape():
    r = requests.get("https://www.shareblue.com")
    soup = BeautifulSoup(r.text, 'html.parser')

    soup = soup.find('body')
    soup = soup.findAll('div', {"class": "ppb_wrapper"})[0].findAll('div', {"class": "shareCount"})

    out = []
    for crap in soup:
        crap = str(crap)
        
        slicey_boi = crap[crap.index('title=')+6:]
        quote = slicey_boi[0]
        slicey_boi = slicey_boi[1:]
        if quote == '"':
            shill_title = slicey_boi[:slicey_boi.index('"')]
        else:
            shill_title = slicey_boi[:slicey_boi.index("'")]

        slicey_boi = crap[crap.index('url="')+5:]
        shill_url = slicey_boi[:slicey_boi.index('"')]
        out.append([shill_title, shill_url])
    return out


bot = praw.Reddit(user_agent='USER_AGENT_HERE',
                  client_id='CLIENT_ID_HERE',
                  client_secret='CLIENT_SECRET_HERE',
                  username='USERNAME_HERE',
                  password='PASSWORD_HERE')

subreddit = bot.subreddit('SUBREDDIT_HERE')

# Assume most recent article has already been submitted at time of running
last_submitted = scrape()[0]

while(True):
    print "Sleeping for another 30 seconds..."
    time.sleep(30)
    try:
        shill_article = scrape()[0]
        if shill_article != last_submitted:
            subreddit.submit(shill_article[0], url = shill_article[1])
            last_submitted = shill_article
            print "Succesfully shilled: ", shill_article[0]
            print "Sleeping for 5 minutes..."
            time.sleep(270)
        else:
            print "No new articles found"
    except:
        "Shit borked."
