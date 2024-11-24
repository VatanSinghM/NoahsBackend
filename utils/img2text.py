from transformers import BlipProcessor,BlipForConditionalGeneration
from PIL import Image
from botocore.exceptions import ClientError
from db import posts_collection
import boto3
from config import AWS_S3_BUCKET
from io import BytesIO
import requests


# Using salesforce Bootstrap Language Image Pretraining as backup of AWS Rekognition as we realized, it is used to detect object and not for image captioning mainly which we need here

# need to fetch the image from S3 

# getting the image name of the latest post. 

def fetch_image_name():
    latest_post = posts_collection.find_one(sort=[("_id", -1)]) 
    if latest_post and "id" in latest_post:
        media_id = latest_post["id"]
        img_name = f"{media_id}.jpg"
        return img_name
    
bucket_name = AWS_S3_BUCKET

s3 = boto3.client("s3")

# searched for one of the best image 2 text pre_trained model in hugging face
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def get_image_if_available():
    # corner case, check if image exists in S3
    image_name = fetch_image_name()
    if image_name:
        try:
            s3_object = s3.get_object(Bucket=bucket_name, Key=image_name)
            image_data = s3_object["Body"].read()
            image = Image.open(BytesIO(image_data))
            return image
        except ClientError as e:
            if e.response['Error']['Code'] == "NoSuchKey":
                print(f"Image does not exists.")
            else:
                raise

    # if not in S3, check from DB
    if image_name:
        try:
            latest_post = posts_collection.find_one(sort=[("_id", -1)]) 
            if latest_post and "media_url" in latest_post:
                media_url = latest_post["media_url"]
                response = requests.get(media_url)
                image = Image.open(BytesIO(response.content))
                return image
        except Exception as e:
            print("Error fetching details from DB for img2Text")
            
    print("No image found in S3 or DB. Proceeding without image.")
    return None 

def generate_caption():
    image = get_image_if_available()
    if image:
        inputs = processor(images=image, return_tensors="pt")
        output = model.generate(**inputs)
        caption = processor.decode(output[0], skip_special_tokens=True)
        return caption
    else:
        return "No image available"
