import requests
from db import insert_comments, insert_post,insert_dm
from config import INSTAGRAM_ACCESS_TOKEN

INSTAGRAM_API_URL = "https://graph.instagram.com"

def fetch_instagram_post(user_id):
    url = f"{INSTAGRAM_API_URL}/{user_id}/media"
    params = {
        "access_token": INSTAGRAM_ACCESS_TOKEN,
        "fields":"id,caption,media_type,media_url"
    }
    response = requests.get(url,params=params)
    response.raise_for_status()
    
    posts = response.json().get("data",[])
    
    for post in posts:
        insert_post(post)
    return response.json()

def fetch_instagram_comments(post_id):
    url = f"{INSTAGRAM_API_URL}/{post_id}/comments"
    params = {
        "access_token": INSTAGRAM_ACCESS_TOKEN,
        "fields":"id,text,username"
    }
    response = requests.get(url,params=params)
    response.raise_for_status()
    comments = response.json().get("data",[])
    
    for comment in comments:
        insert_comments(comment)
    return comments


def fetch_instagram_dms(user_id):
    url = f"{INSTAGRAM_API_URL}/{user_id}/inbox"
    params = {
        "access_token": INSTAGRAM_ACCESS_TOKEN,
        "fields": "id,thread,participants,message"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    dms = response.json().get("data", [])
    
    # Insert each DM into MongoDB
    for dm in dms:
        insert_dm(dm)
    return dms