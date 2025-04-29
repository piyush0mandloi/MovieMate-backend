from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer

app = Flask(__name__)
CORS(app)  # Allow React frontend to access backend

# Initialize necessary objects
ps = PorterStemmer()

# Load and preprocess data
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits, on='title')
movies = movies[['movie_id', 'title', 'overview', 'cast', 'crew', 'genres', 'keywords']] 
movies.dropna(inplace=True)

# Functions for preprocessing
def convert(obj):
    l = []
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l

def convert3(obj):
    l = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            l.append(i['name'])
            counter += 1
        else:
            break
    return l

def fetch_director(obj):
    l = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            l.append(i['name'])
            break
    return l

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

# Apply preprocessing
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
new_df = movies[['movie_id', 'title', 'tags']]

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
new_df['tags'] = new_df['tags'].apply(stem)

# Vectorization and Similarity
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()
similarity = cosine_similarity(vectors)

# Recommendation function
def recommend(movie):
    movie = movie.lower()
    matches = new_df[new_df['title'].str.lower() == movie]
    if matches.empty:
        return None  # explicitly return None if no match

    movie_index = matches.index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

    recommended = []
    for i in movies_list:
        recommended.append({
            'movie_id': int(new_df.iloc[i[0]].movie_id),
            'title': new_df.iloc[i[0]].title
        })
    return recommended



# 🛤 API Route for Recommendations
@app.route('/recommend', methods=['POST'])
def recommend_movies():
    data = request.get_json()
    movie_name = data.get('title')

    if not movie_name:
        return jsonify({"error": "No movie title provided"}), 400

    recommendations = recommend(movie_name)

    if recommendations is None or len(recommendations) == 0:
        return jsonify({"error": "Movie not found in dataset"}), 404

    return jsonify(recommendations)


# 🛤 Health Check Route
@app.route('/', methods=['GET'])
def index():
    return "Movie Recommendation API is Running! 🎥🚀"

if __name__ == "__main__":
    app.run(debug=True)
