from pymongo import MongoClient,errors
from config import MONGO_DB,MONGODB_URI

try:
    if not MONGODB_URI or not MONGO_DB:
        raise ValueError("DB configuration missing")
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client[MONGO_DB]
    print(f"Connection to {MONGO_DB} DB success")
except (errors.ServerSelectionTimeoutError, errors.ConnectionFailure) as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None

except Exception as e:
    print(f"Error: {e}")
    db = None

    
posts_collection = db["instagram_posts"] if db is not None else None
comments_collection = db["instagram_comments"] if db is not None else None
dms_collection = db["instagram_dms"] if db is not None else None

# def insert_post(post):
#     if posts_collection is None:
#         print("Error: Posts collection not available.")
#         return None
#     try:
#         print("Post is inserted from db.py")
#         return posts_collection.insert_one(post)
#     except errors.PyMongoError as e:
#         print(f"Error inserting post data into DB: {e}")
#         return None

def insert_post(post):
    existing_post = posts_collection.find_one({"id": post["id"]})
    
    if existing_post:
        print(f"Post with ID {post['id']} already exists")
        return False
    
    posts_collection.insert_one(post)
    print(f"Post with ID {post['id']} inserted successfully.")
    return True 


def insert_comments(comment):
    if comments_collection is None:
        print("Error: Comments collection not available.")
        return None
    try:
        return comments_collection.insert_one(comment)
    except errors.PyMongoError as e:
        print(f"Unable to insert comment: {e}")
        return None

def insert_dm(dm):
    if dms_collection is None:
        print("Error: DMs collection not available.")
        return None
    try:
        return dms_collection.insert_one(dm)
    except errors.PyMongoError as e:
        print(f"Error inserting DM: {e}")
        return None

def fetch_posts():
    if posts_collection is None:
        print("Error: Posts collection not available.")
        return []
    try:
        return list(posts_collection.find())
    except errors.PyMongoError as e:
        print(f"Error fetching post data: {e}")
        return []

def fetch_comments():
    if comments_collection is None:
        print("Error: Comments collection not available.")
        return []
    try:
        return list(comments_collection.find())
    except errors.PyMongoError as e:
        print(f"Error fetching comments: {e}")
        return []

def fetch_dms():
    if dms_collection is None:
        print("Error: DMs collection not available.")
        return []
    try:
        return list(dms_collection.find())
    except errors.PyMongoError as e:
        print(f"Error fetching DMs: {e}")
        return []