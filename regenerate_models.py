import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import nltk

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    nltk.download('wordnet')

# Load and process data
print("Loading CSV...")
df = pd.read_csv('movies_metadata.csv')

# Select columns
df = df[['title', 'overview', 'genres', 'tagline', 'vote_average', 'popularity']]

# Handle missing values
df = df.dropna(subset=['title'])
df['overview'] = df['overview'].fillna('')
df['tagline'] = df['tagline'].fillna('')

# Extract genres
import ast
df['genres'] = df['genres'].apply(lambda x: " ".join([i['name'] for i in ast.literal_eval(x) if isinstance(x, str)]) if pd.notna(x) else "")

# Combine features
df['tags'] = df['overview'] + " " + df['genres'] + " " + df['tagline']

# Text preprocessing
print("Processing text...")
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)

df['tags'] = df['tags'].apply(preprocess_text)
df = df.reset_index(drop=True)

# Create indices
print("Creating indices...")
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

# TF-IDF vectorization
print("Creating TF-IDF matrix...")
tfidf = TfidfVectorizer(max_features=50000, ngram_range=(1, 2), stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['tags'])

# Save with joblib (more reliable than pickle for pandas/sklearn objects)
print("Saving models...")
import joblib
joblib.dump(tfidf_matrix, 'tfidf_matrix.pkl', compress=3)
joblib.dump(indices, 'indices.pkl', compress=3)
joblib.dump(df, 'df.pkl', compress=3)
joblib.dump(tfidf, 'tfidf.pkl', compress=3)

print("✓ Models saved successfully!")
print(f"  - {len(df)} movies loaded")
print(f"  - TF-IDF matrix shape: {tfidf_matrix.shape}")
