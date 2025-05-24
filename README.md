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

- **Backend**: Python, Flask, Pandas, NumPy, scikit-learn
- **Frontend**: HTML5, CSS3 (Dark Theme), JavaScript (vanilla)
- **Data Handling**: TF-IDF Vectorizer, Cosine Similarity, Pivot Tables

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system 

###2. Install Dependencies

pip install -r requirements.txt
Flask
pandas
numpy
scikit-learn

3. Place the Dataset
Download and place the following datasets in the project root:

rotten_tomatoes_movies.csv
rotten_tomatoes_movie_reviews.csv

4. Run the App
bash
Copy
Edit
python app.py
Then open your browser and go to:
http://127.0.0.1:5000/

📁 Project Structure
MOVIE RECOMMENDER SYSTEM/
│
├── .gradio/                         # (Optional) Folder for Gradio certificate
│   └── certificate.pem             # SSL certificate file (if used for secure serving)
│
├── myenv/                           # Python virtual environment
│   ├── etc/
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   ├── share/
│   └── pyvenv.cfg
│
├── templates/                       # Folder for Flask HTML templates
│   └── index.html                   # Main UI HTML file
│
├── .gitattributes                   # Git settings for file handling
├── .gitignore                       # Specifies files/folders to ignore in Git
│
├── app.py                           # Flask web application
├── Main_code.ipynb                  # Jupyter Notebook for main development and testing
├── model.pkl                        # Pickle file (if you save/load ML models)
├── requirements.txt                 # Project dependencies
├── rotten_tomatoes_movies.csv       # Movie metadata
├── rotten_tomatoes_movie_reviews.csv # Review metadata
└── README.md                        # [Recommended] Project overview (to be added)


📌 Future Enhancements

Add user login & personalized history
Incorporate real-time rating feedback
Deploy on Heroku / Render / AWS


## 📂 Download the Dataset and Project Files

You can download the dataset and project files from the following Google Drive links:

- 📊 **CSV Dataset**: [Download CSV files](https://drive.google.com/drive/folders/1oiSvHvO3J0yNMrXomYOwby_SDnVS0mLl?usp=sharing)  
- 🗂️ **Complete Project Files**: [Download Full Project](https://drive.google.com/drive/folders/1n1e6lXZOvXWUby6ojdpzkFJTOnSZLHho?usp=sharing)



