import os
from dotenv import load_dotenv

load_dotenv()


INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")


MONGODB_URI = os.getenv("MONGODB_URI")
MONGO_DB = os.getenv("MONGO_DB")
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

#fetching the list of offensive words from a seperate file. We can later fetch this from some online repository or API readily available
def offensive_list(file_path='offensive.txt'):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"Error reading offensive file: {e}")
        return []