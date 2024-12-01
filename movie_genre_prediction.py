import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load the dataset
try:
    df = pd.read_csv('movie_dataset.csv')
except FileNotFoundError:
    print("Error: movie_dataset.csv not found")
    sys.exit(1)

# Preprocess the text data
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = text.split()  # Use simple splitting instead of word_tokenize
    tokens = [t for t in tokens if t not in stop_words]
    return ' '.join(tokens)

df['processed_plot'] = df['plot'].apply(preprocess_text)

# Convert text to TF-IDF features
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['processed_plot'])

# Prepare the target variables
genres = df['genres'].str.get_dummies(sep=',')
y = genres.values

# Train the model
clf = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
clf.fit(X, y)

def predict_genre(plot):
    processed_plot = preprocess_text(plot)
    tfidf_vector = vectorizer.transform([processed_plot])
    prediction = clf.predict(tfidf_vector)
    predicted_genres = genres.columns[prediction[0].astype(bool)].tolist()
    return predicted_genres

if __name__ == "__main__":
    if len(sys.argv) > 1:
        plot = sys.argv[1]
        predicted_genres = predict_genre(plot)
        print(','.join(predicted_genres))
    else:
        print("Error: No plot provided")

