from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import gc
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
# === Load and preprocess the data ===
movies_df = pd.read_csv('rotten_tomatoes_movies.csv', encoding='latin')
reviews_df = pd.read_csv('rotten_tomatoes_movie_reviews.csv', encoding='latin')

reviews_df = reviews_df.fillna(0)
reviews_df = reviews_df.loc[:, ~reviews_df.columns.str.contains('^Unnamed')]

movies_df['genre'] = movies_df['genre'].astype('category')
movies_df['title'] = movies_df['title'].astype('category')

movies_df = movies_df.head(80000)
reviews_df = reviews_df.head(80000)

merged_df = pd.merge(movies_df, reviews_df, on='id')
merged_df = merged_df.drop_duplicates()

merged_df = merged_df[['id', 'title', 'audienceScore', 'tomatoMeter', 'genre', 'rating',
                       'director', 'originalLanguage', 'releaseDateTheaters', 'runtimeMinutes',
                       'reviewId', 'criticName', 'isTopCritic', 'originalScore', 'reviewText', 'scoreSentiment']]

merged_df = merged_df.drop_duplicates(subset=['title', 'genre', 'director'])

numeric_cols = ['audienceScore', 'tomatoMeter']
for col in numeric_cols:
    merged_df[col].fillna(merged_df[col].median(), inplace=True)

categorical_cols = merged_df.select_dtypes(include='object').columns
for col in categorical_cols:
    merged_df[col].fillna(merged_df[col].mode()[0], inplace=True)

def min_max_normalize(column):
    return (column - column.min()) / (column.max() - column.min())

merged_df.dropna(subset=['audienceScore', 'tomatoMeter'], inplace=True)
merged_df['audienceScore'] = min_max_normalize(merged_df['audienceScore'])
merged_df['tomatoMeter'] = min_max_normalize(merged_df['tomatoMeter'])

def parse_score(score):
    if isinstance(score, str):
        score = score.strip()
        if '/' in score:
            try:
                num, denom = score.split('/')
                return float(num) / float(denom) * 10
            except:
                return np.nan
        elif score.replace('.', '', 1).isdigit():
            return float(score)
        else:
            return np.nan
    return score

merged_df['numeric_score'] = merged_df['originalScore'].apply(parse_score)

# Extract release year
if 'releaseDateTheaters' in merged_df.columns:
    merged_df['releaseYear'] = pd.to_datetime(merged_df['releaseDateTheaters'], errors='coerce').dt.year

# === Step 1: Content-Based Filtering ===
def build_content_similarity(df):
    df = df.reset_index(drop=True).copy()
    df['combined_features'] = (
        df['title'].astype(str) + " " +
        df['genre'].astype(str) + " " +
        df['director'].astype(str) + " " +
        df['rating'].astype(str)
    ).fillna("")

    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    feature_matrix = vectorizer.fit_transform(df['combined_features'])

    content_sim = cosine_similarity(feature_matrix)

    del feature_matrix
    gc.collect()

    return content_sim, df

# === Step 2: Collaborative Filtering ===
def build_collaborative_similarity(df):
    pivot = df.pivot_table(index='title', columns='criticName', values='numeric_score', aggfunc='mean').fillna(0)
    collab_sim = cosine_similarity(pivot)
    title_to_index = {title: i for i, title in enumerate(pivot.index)}
    return collab_sim, title_to_index, list(pivot.index)

# === Step 3: Hybrid Recommendation ===
def hybrid_recommend(keyword, df, content_sim, collab_sim, title_to_collab_index, collab_titles, top_n=10, sort_by='audienceScore', sort_order='asc'):
    filtered = df[
        df['title'].str.contains(keyword, case=False, na=False) |
        df['genre'].str.contains(keyword, case=False, na=False) |
        df['director'].str.contains(keyword, case=False, na=False) |
        df['rating'].astype(str).str.contains(keyword, case=False, na=False)
    ]

    if filtered.empty:
        return []

    filtered_idx = filtered.index.tolist()
    hybrid_scores = np.zeros(len(df))

    for idx in filtered_idx:
        content_scores = content_sim[idx]
        title = df.iloc[idx]['title']
        collab_idx = title_to_collab_index.get(title, None)

        if collab_idx is not None:
            collab_scores = collab_sim[collab_idx]
            collab_scores_resized = np.zeros(len(df))
            for i, t in enumerate(df['title']):
                if t in title_to_collab_index:
                    collab_scores_resized[i] = collab_scores[title_to_collab_index[t]]
            combined = 0.5 * content_scores + 0.5 * collab_scores_resized
        else:
            combined = content_scores

        hybrid_scores += combined

    recommended_indices = hybrid_scores.argsort()[::-1][:top_n*3]
    recommendations = df.iloc[recommended_indices].copy()

    if 'releaseYear' not in recommendations.columns and 'releaseYear' in df.columns:
        recommendations = recommendations.merge(df[['title', 'releaseYear']], on='title', how='left')

    ascending = True if sort_order == 'asc' else False
    if sort_by == 'Release Year' and 'releaseYear' in recommendations.columns:
        recommendations = recommendations.sort_values(by='releaseYear', ascending=ascending)
    elif sort_by in recommendations.columns:
        recommendations = recommendations.sort_values(by=sort_by, ascending=ascending)

    return recommendations.head(top_n)[[
        'title', 'genre', 'director', 'rating',
        'audienceScore', 'tomatoMeter', 'originalLanguage',
        'releaseDateTheaters', 'runtimeMinutes'
    ]].to_dict(orient='records')

# === Build models on startup ===
content_sim, content_df = build_content_similarity(merged_df)
collab_sim, title_to_index, collab_titles = build_collaborative_similarity(merged_df)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    top_n = 10
    sort_by = 'audienceScore'
    sort_order = 'asc'

    if request.method == 'POST':
        keyword = request.form['keyword']
        top_n = int(request.form.get('top_n', 10))
        sort_by = request.form.get('sort_by', 'audienceScore')
        sort_order = request.form.get('sort_order', 'asc')

        recommendations = hybrid_recommend(
            keyword, content_df, content_sim, collab_sim,
            title_to_index, collab_titles,
            top_n=top_n, sort_by=sort_by, sort_order=sort_order
        )

    titles = merged_df['title'].dropna().unique().tolist()
    genres = merged_df['genre'].dropna().unique().tolist()
    directors = merged_df['director'].dropna().unique().tolist()
    keyword_list = sorted(set(titles + genres + directors))

    return render_template('index.html', recommendations=recommendations,
                           keyword_list=keyword_list, top_n=top_n,
                           sort_by=sort_by, sort_order=sort_order)

if __name__ == '__main__':
    app.run(debug=True)
