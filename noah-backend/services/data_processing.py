import pandas as pd
import spacy
from config import offensive_list

# Keeping the offensive words list for later use
def load_offensive_words():
    offensive_words = offensive_list('offensive.txt')
    if not offensive_words:
        print("The offensive list is empty or not loaded.")
        return None
    return set(offensive_words) #avoid duplicates and storing unique values using set


# using small model of spacy for basic keyword extraction
# We may also use RAKE but as of now for my MVP, we will proceed with spacy
nlp = spacy.load("en_core_web_sm")


def cleaned_caption(caption):
    caption_raw = pd.Series([caption])
    #removing unwanted characters using regex
    cleaned_caption = caption_raw.str.replace("[^a-zA-Z\s]", "", regex=True).str.strip().values[0]
    cleaned_caption = cleaned_caption.lower()
    
    # Removing common stopwords and any single-character words
    cleaned_caption = " ".join(word for word in cleaned_caption.split() if len(word) > 1)
    
    return cleaned_caption

# extracting keywords using the nlp as initialized
def extract_keywords(caption):
    doc = nlp(caption)
    
    keywords = [ent.text for ent in doc.ents if ent.label_ in 
                ["PRODUCT", "GPE", "ORG"]]  # Named entities
    keywords += [token.text for token in doc if token.pos_ in 
                 ['NOUN', 'ADJ'] and not token.is_stop]  # Nouns and adjectives (excluding stopwords)
    
    return keywords if keywords else None

# Function to check if the caption contains offensive words
def check_offensive(caption, offensive_words):
    words = set(caption.split())
    return any(word in offensive_words for word in words)

# Main function to process the caption
def process_caption(caption):
    offensive_words = load_offensive_words()
    if not offensive_words:
        return None, "Error: Offensive word list could not be loaded."
    
    # Clean the caption
    clean_caption = cleaned_caption(caption)
    
    # Check for offensive words in the cleaned caption
    if check_offensive(clean_caption, offensive_words):
        print("Caption contains inappropriate language.")
        return None, "Caption contains inappropriate language."
    
    # final step to extract keywords
    keywords = extract_keywords(clean_caption)
    if keywords:
        print(f"Keywords extracted: {keywords}")
    else:
        print("No product-related keywords found.")
    
    return clean_caption, keywords



# test = process_caption("Apple is launching a new iPhone next month in the UK.")
# print(f"{test}")