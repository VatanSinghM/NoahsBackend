from langdetect import detect
from googletrans import Translator
from pymongo import MongoClient
from config import MONGO_DB,MONGODB_URI
import os

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
client.server_info()
db = client[MONGO_DB]
post_collections = db["instagram_posts"] if db is not None else None

translator = Translator()

def get_latest_caption():
    latest_post = post_collections.find_one(sort=[('_id',-1)])
    return latest_post.get("caption") if latest_post else None

def detect_translate_caption():
    caption = get_latest_caption()
    if caption:
        try:
            detected_lan = detect(caption)
            
            if detected_lan != "en":
                translation = translator.translate(caption, src=detected_lan,dest="en")
                return translation.text
            else:
                return caption
        except Exception as e:
            print(f"Unable to translate due to {e}")
            return None
        
    else:
        print(f"Caption unavailable")
        return None
    
        
        