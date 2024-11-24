from pymongo import DESCENDING
import requests
import boto3
from botocore.exceptions import NoCredentialsError
import sys
sys.path.append("..")
from config import AWS_ACCESS_KEY_ID,AWS_REGION_NAME,AWS_S3_BUCKET,AWS_SECRET_ACCESS_KEY
from db import posts_collection

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

def fetch_latest_post():
    try:
        latest_post = posts_collection.find_one(sort=[("_id",DESCENDING)])
        if latest_post:
            return latest_post
        else:
            print("No post available in DB")
            return None
        
    except Exception as e:
        print(f"Error occured while fetching post from DB due to {e}")
        return None
    

def upload_to_s3(media_url, file_name):
    try:
        response = requests.get(media_url)
        if response.status_code == 200:
            s3.put_object(
                Bucket=AWS_S3_BUCKET,
                Key=file_name,
                Body=response.content,
                ContentType="image/jpeg"
            )
            return True
        else:
            print(f"Cannot download image as HTTP status code: {response.status_code}")
            return False
    except NoCredentialsError:
        print("AWS credentials not available")
        return False
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return False


def process_latest_post():
    try:
        latest_post = posts_collection.find_one(sort=[("_id", -1)])  # Fetching the latest post
        if latest_post and "media_url" in latest_post and "id" in latest_post:
            media_url = latest_post["media_url"]
            media_id = latest_post["id"]
            file_name = f"{media_id}.jpg" 

            upload_success = upload_to_s3(media_url, file_name)

            if upload_success:
                return True, f"Uploaded media with ID {media_id} to S3"
            else:
                return False, f"Failed to upload media with ID {media_id} to S3"
        else:
            return False, "No media in DB"
    except Exception as e:
        return False, f"Error during processing the latest post: {str(e)}"