from faker import Faker
import pandas as pd
import spacy
import re
from utils.translation import get_latest_caption
#from large_language_model import optimized_caption

fake = Faker()
nlp = spacy.load("en_core_web_sm")

# test masking
# data = {
#     "caption": [
#         "I sell clothes, my name is Shrutik 9988776655", 
#         "You can also call my assistant at 1122334455"
#     ]
# }

latest_caption = get_latest_caption()

# checking if there is a latest caption
if latest_caption:
    df = pd.DataFrame([{"caption": latest_caption}])
    print(df)
else:
    print("No latest caption found.")

def mask_personal_data(text):
    doc = nlp(text)
    anonymized_text = text
    
    for ent in doc.ents:
        if ent.label == "PERSON":
            anonymized_text = anonymized_text.replace(ent.text, "XXX")
    
    #usin regular expression to search for phone number and masking it in next step
    phone = r'\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    anonymized_text = re.sub(phone, "XXX", anonymized_text) 
    
    return anonymized_text

# df["caption"] = df["caption"].apply(mask_personal_data)

#print(df.to_string())