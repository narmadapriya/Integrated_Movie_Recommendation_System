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
 
```bash
git clone https://github.com/narmadapriya/Integrated_Movie_Recommendation_System.git
cd Integrated_Movie_Recommendation_System

2. Install Dependencies
Install required Python packages:
pip install -r requirements.txt

Or manually install:
pip install Flask pandas numpy scikit-learn OR
pip install Flask pandas==2.2.2 numpy==2.0.2 scikit-learn==1.6.1 gunicorn

3. Download and Place the Datasets
🔻 Download the CSV dataset files from the following link:
- 📊 **CSV Dataset**: [Download CSV files] (https://drive.google.com/drive/folders/1oiSvHvO3J0yNMrXomYOwby_SDnVS0mLl?usp=sharing))
Place the following files into the root directory of the project:
 -rotten_tomatoes_movies.csv
 -rotten_tomatoes_movie_reviews.csv

4. Run the Application
bash
python app.py

Then open your browser and go to:
http://127.0.0.1:5000/

📁 Project Structure
  Integrated_Movie_Recommendation_System/
│
├── .gradio/                          # (Optional) Gradio SSL certificate folder
│   └── certificate.pem
│
├── templates/                        # Flask HTML templates
│   └── index.html
│
├── app.py                            # Flask web application
├── Main_code.ipynb                   # Jupyter Notebook for dev/testing
├── model.pkl                         # Serialized ML model (if used)
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignored files
├── .gitattributes                    # Git LFS settings
├── rotten_tomatoes_movies.csv        # Movie metadata
├── rotten_tomatoes_movie_reviews.csv # Movie review metadata
└── README.md                         # Project overview


📌 Future Enhancements

-Add user login and personalized watch history
-Include real-time user rating and feedback
-Deploy on cloud platforms (Heroku, Render, AWS)


## 📂 Download the Dataset and Project Files

You can download the dataset and project files from the following Google Drive links:
🗂️ **Complete Project Files**: [Download Full Project] https://drive.google.com/drive/folders/1Ywbjw1BBRXBQwQPJYKBY4njCcvvRHE62?usp=sharing

