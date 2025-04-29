# 🎬 Movie Recommendation API (Backend)
This is the **backend** for a Movie Recommendation Web App built with **Python + Flask**. It uses **content-based filtering** (NLP + cosine similarity) on the TMDB 5000 dataset to generate movie recommendations.

## 🧠 Features
- 🧾 Content-based recommendation using genres, cast, keywords, overview, and crew
- 🔍 Cosine similarity on NLP-preprocessed movie metadata
- 📦 Simple REST API for integration with any frontend
- 🚀 CORS enabled for frontend-backend communication

## 📁 Project Structure
/
├── app.py                   # Main Flask app
├── tmdb_5000_movies.csv     # Movie dataset
├── tmdb_5000_credits.csv    # Credits dataset
├── requirements.txt         # Python dependencies
```

## 🚀 API Endpoints

### 🔹 Health Check

```http
GET /
```

**Response:**
```
Movie Recommendation API is Running! 🎥🚀

### 🔹 Get Movie Recommendations

```http
POST /recommend
Content-Type: application/json
```

**Request Body:**

```json
{
  "title": "Avatar"
}
```

**Response:**

```json
[
  { "movie_id": 19995, "title": "John Carter" },
  { "movie_id": 49529, "title": "The Last Airbender" },
  ...
]
```

Returns `404` if the movie is not in the dataset.

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/movie-recommender-backend.git
cd movie-recommender-backend
```

### 2. Install Dependencies

Make sure you have Python 3.8+ and pip installed.

```bash
pip install -r requirements.txt
```

You may need to install NLTK data as well:

```python
import nltk
nltk.download('punkt')
```

### 3. Run the Server

```bash
python app.py
```

Server will run by default on:

```
http://localhost:5000
```

## ⚙️ Deployment Suggestions

- 🔁 **Render**, **Railway**, or **Fly.io** for backend hosting
- ✅ Make sure CORS is enabled (`CORS(app)`) for frontend communication

## 📄 License

MIT License. Use, modify, and distribute freely.

---

Built with ❤️ using Flask and pandas.
```

---

Let me know if you want a **combined README** for full-stack deployment (frontend + backend in one repo).
