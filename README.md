# 🎬 Integrated Movie Recommendation System

A full-stack integrated movie recommendation system built using **Content-Based Filtering** and **Collaborative Filtering**, wrapped in a Flask-based front-end interface. The system suggests movies based on a user's keyword input — including titles, genres, or directors — and ranks them using hybrid similarity scores.

## 🌟 Features

- 🔍 Search by movie title, genre, or director
- 🎯 Content-Based Filtering using TF-IDF and cosine similarity
- 👥 Collaborative Filtering using critic ratings
- 🧠 Hybrid recommendation logic combining content and collaborative scores
- 📈 Dynamic sorting by:
  - Audience Score
  - Tomato Meter
  - Release Year
- 🎨 Interactive and responsive front-end UI using HTML and CSS

## 🗃️ Datasets(csv files)

- `rotten_tomatoes_movies.csv`
- `rotten_tomatoes_movie_reviews.csv`

These datasets include movie metadata, critic reviews, sentiment scores, and more.

## 🧰 Tech Stack

- **Backend**: Python, Flask, Pandas (v2.2.2), NumPy (v2.0.2), scikit-learn (v1.6.1)
- **Frontend**: HTML5, CSS3 (Dark Theme), JavaScript
- **Data Handling**: TF-IDF Vectorizer, Cosine Similarity, Pivot Tables


## 🚀 Getting Started

### 1. Clone the Repository
<pre> ```bash # Clone the repository git clone https://github.com/your-username/your-repo.git cd your-repo # Install dependencies pip install -r requirements.txt # Run the app python app.py ``` </pre>

