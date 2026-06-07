# ===  Import Libraries ===

# General Data Handling
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Content-Based Filtering
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import linear_kernel  # Faster than cosine_similarity for TF-IDF


# Collaborative Filtering
# Import the full module so you can check its version
import surprise  
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split


# Hybrid Logic
# (Usually custom code to combine scores from the above two)

import warnings
import gc
import pickle

import re

#  Load Datasets

movies_df = pd.read_csv(r"C:\Users\Admin\Desktop\PROJECTS\movie-recommendation-system\data\rotten_tomatoes_movies.csv",encoding="latin-1")

reviews_df = pd.read_csv(r"C:\Users\Admin\Desktop\PROJECTS\movie-recommendation-system\data\rotten_tomatoes_movie_reviews.csv",encoding="latin-1",low_memory=False)

# =========================================================
# DATA CLEANING + PREPROCESSING + FEATURE ENGINEERING
# =========================================================

# =========================================================
# REMOVE UNNAMED COLUMNS
# =========================================================

movies_df = movies_df.loc[
    :,
    ~movies_df.columns.str.contains("^Unnamed")
]

reviews_df = reviews_df.loc[
    :,
    ~reviews_df.columns.str.contains("^Unnamed")
]

# =========================================================
# REMOVE DUPLICATES
# =========================================================

movies_df = movies_df.drop_duplicates(
    subset=["id"]
)

reviews_df = reviews_df.drop_duplicates(
    subset=["reviewId"]
)

# =========================================================
# MERGE DATASETS
# =========================================================

df = pd.merge(
    movies_df,
    reviews_df,
    on="id",
    how="inner"
)

# =========================================================
# KEEP REQUIRED COLUMNS
# =========================================================

essential_cols = [

    "id",
    "title",
    "genre",
    "director",
    "rating",
    "originalLanguage",
    "releaseDateTheaters",
    "audienceScore",
    "tomatoMeter",
    "runtimeMinutes",
    "reviewId",
    "criticName",
    "isTopCritic",
    "originalScore",
    "scoreSentiment"
]

df = df[essential_cols].copy()

# =========================================================
# ID CLEANING
# =========================================================

df["id"] = (
    df["id"]
    .astype(str)
    .str.strip()
)

df = df[
    df["id"] != "nan"
]

# =========================================================
# HANDLE MISSING VALUES
# =========================================================

categorical_cols = [

    "genre",
    "director",
    "rating",
    "originalLanguage",
    "scoreSentiment"
]

df[categorical_cols] = (
    df[categorical_cols]
    .fillna("Unknown")
)

# =========================================================
# TITLE CLEANING
# =========================================================

df["title"] = (
    df["title"]
    .astype(str)
    .str.lower()
    .str.strip()
)

# =========================================================
# GENRE CLEANING
# =========================================================

df["genre"] = (
    df["genre"]
    .astype(str)
    .str.lower()
    .str.replace("|", ",", regex=False)
    .str.strip()
)

# =========================================================
# DIRECTOR CLEANING
# =========================================================

df["director"] = (
    df["director"]
    .astype(str)
    .str.lower()
    .str.replace(" ", "", regex=False)
)

# =========================================================
# LANGUAGE NORMALIZATION
# =========================================================

lang_map = {

    "en": "english",
    "fr": "french",
    "es": "spanish",
    "ja": "japanese"
}

df["originalLanguage"] = (
    df["originalLanguage"]
    .replace(lang_map)
    .astype(str)
    .str.lower()
)

# =========================================================
# CLEAN CRITIC SCORES
# =========================================================

df["originalScore"] = df["originalScore"].replace(

    [
        "fresh",
        "rotten",
        "",
        "NA",
        "N/A"
    ],

    np.nan
)

# =========================================================
# LETTER GRADE CONVERSION
# =========================================================

grade_map = {

    "A+": 100,
    "A": 95,
    "A-": 90,
    "B+": 85,
    "B": 80,
    "B-": 75,
    "C+": 70,
    "C": 65,
    "C-": 60,
    "D+": 55,
    "D": 50,
    "D-": 45,
    "F": 30
}

df["originalScore"] = (
    df["originalScore"]
    .replace(grade_map)
)

# =========================================================
# FRACTION SCORE CONVERTER
# =========================================================

def convert_fraction(val):

    if isinstance(val, str) and "/" in val:

        try:

            num, den = val.split("/")

            return (
                float(num)
                /
                float(den)
            ) * 100

        except:

            return np.nan

    return val

df["originalScore"] = (
    df["originalScore"]
    .apply(convert_fraction)
)

# =========================================================
# NUMERIC COLUMNS
# =========================================================

num_cols = [

    "audienceScore",
    "tomatoMeter",
    "runtimeMinutes",
    "originalScore"
]

for col in num_cols:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

    median_value = df[col].median()

    df[col] = (
        df[col]
        .fillna(median_value)
    )

# =========================================================
# DATE FEATURES
# =========================================================

df["releaseDateTheaters"] = pd.to_datetime(
    df["releaseDateTheaters"],
    format="%d-%m-%Y",
    errors="coerce"
)

df["Year"] = (
    df["releaseDateTheaters"]
    .dt.year
)

df["Year"] = (
    df["Year"]
    .fillna(1900)
    .astype(int)
)

df["Decade"] = (
    (df["Year"] // 10) * 10
)



# =========================================================
# REVIEW COUNT
# =========================================================

review_counts = (

    df.groupby("id")
      .size()
      .reset_index(name="review_count")

)

df = pd.merge(

    df,

    review_counts,

    on="id",

    how="left"
)

# =========================================================
# SENTIMENT FEATURE
# =========================================================

sentiment_map = {

    "POSITIVE": 1.0,
    "Positive": 1.0,

    "NEUTRAL": 0.5,
    "Neutral": 0.5,

    "NEGATIVE": 0.0,
    "Negative": 0.0
}

df["sentimentWeight"] = (

    df["scoreSentiment"]
    .map(sentiment_map)
    .fillna(0.5)
)

# =========================================================
# METADATA SOUP
# =========================================================

def create_soup(row):

    return (

        str(row["genre"]) + " " +
        str(row["director"]) + " " +
        str(row["rating"]) + " " +
        str(row["originalLanguage"])

    )

df["soup"] = df.apply(
    create_soup,
    axis=1
)

# =========================================================
# BAYESIAN FUNCTION
# =========================================================

def calculate_bayesian_score(
    scores,
    review_counts,
    percentile=0.60
):

    C = scores.mean()

    m = review_counts.quantile(
        percentile
    )

    return (

        (
            review_counts
            /
            (review_counts + m)
        )
        * scores

        +

        (
            m
            /
            (review_counts + m)
        )
        * C

    )

# =========================================================
# CONTENT DATASET
# =========================================================

content_df = (

    df.groupby(
        "id",
        as_index=False
    )
    .agg({

        "title": "first",

        "genre": "first",

        "director": "first",

        "rating": "first",

        "originalLanguage": "first",

        "releaseDateTheaters": "first",

        "runtimeMinutes": "mean",

        "audienceScore": "mean",

        "tomatoMeter": "mean",

        "review_count": "max",

        "Year": "first",

        "Decade": "first",

        "sentimentWeight": "mean",

        "soup": "first"

    })

)

content_df = (
    content_df
    .drop_duplicates(subset=["title"])
    .reset_index(drop=True)
)

# Release year used by recommender

content_df["releaseYear"] = (
    content_df["Year"]
)

     

# =========================================================
# REMOVE DUPLICATE TITLES
# =========================================================

content_df = (
    content_df
    .drop_duplicates(
        subset=["title"]
    )
    .reset_index(drop=True)
)

# =========================================================
# BAYESIAN SCORES
# =========================================================

content_df["bayesianAudienceScore"] = (

    calculate_bayesian_score(

        content_df["audienceScore"],

        content_df["review_count"]

    )
)

content_df["bayesianTomatoMeter"] = (

    calculate_bayesian_score(

        content_df["tomatoMeter"],

        content_df["review_count"]

    )
)

# =========================================================
# FINAL SCORE
# =========================================================

content_df["finalScore"] = (

    0.6
    *
    content_df["bayesianAudienceScore"]

    +

    0.4
    *
    content_df["bayesianTomatoMeter"]

)

#=================================================
#  Quality Score
#=================================================

content_df["quality_score"] = (
    0.4 * content_df["bayesianAudienceScore"]
    +
    0.4 * content_df["bayesianTomatoMeter"]
    +
    0.2 * (content_df["sentimentWeight"] * 100)
)  

# Convert raw float quality_scores into whole integers (e.g., 77.334 -> 77)
content_df["quality_score"] = content_df["quality_score"].round().astype(int)


# =========================================================
# TF-IDF VECTORIZATION
# =========================================================

tfidf = TfidfVectorizer(

    stop_words='english',

    max_features=5000,

    dtype=np.float32

)

tfidf_matrix = tfidf.fit_transform(

    content_df['soup']

)


# =========================================================
# COLLABORATIVE DATASET
# =========================================================

collab_df = df[
    [
        'criticName',
        'title',
        'originalScore'
    ]
].copy()

# Remove missing values

collab_df = collab_df.dropna(
    subset=[
        'criticName',
        'title',
        'originalScore'
    ]
)


# ========================================================= 
# HYBRID MOVIE RECOMMENDATION SYSTEM
# TITLE + GENRE + DIRECTOR SEARCH
# WITH FILTERS + SORTING
# =========================================================


# =========================================================
# DATA PREPROCESSING
# =========================================================

# Convert columns to string
text_cols = [
    'title',
    'genre',
    'director',
    'rating',
    'originalLanguage'
]

for col in text_cols:
    content_df[col] = content_df[col].astype(str)

# Lowercase important columns
content_df['title'] = content_df['title'].str.lower()
content_df['genre'] = content_df['genre'].str.lower()
content_df['director'] = content_df['director'].str.lower()
content_df['originalLanguage'] = content_df['originalLanguage'].str.lower()

# =========================================================
# RELEASE YEAR
# =========================================================

content_df['releaseYear'] = pd.to_datetime(
    content_df['releaseDateTheaters'],
    errors='coerce'
).dt.year

content_df['releaseYear'] = (
    content_df['releaseYear']
    .fillna(1900)
    .astype(int)
)

# =========================================================
# RATING MAPPING
# =========================================================

rating_map = {
    'G': 0,
    'TVG': 0,
    'PG': 1,
    'TVPG': 1,
    'PG-13': 2,
    'TV-14': 2,
    'R': 3,
    'TVMA': 3,
    'NC-17': 4,
    'TUY7': 5
}

content_df['rating_numeric'] = (
    content_df['rating']
    .str.upper()
    .map(rating_map)
)

content_df['rating_numeric'] = (
    content_df['rating_numeric']
    .fillna(-1)
)

content_df['rating_label'] = (
    content_df['rating']
    .fillna('Unknown')
)

# =========================================================
# DROPDOWN VALUES
# =========================================================

rating_dropdown = sorted(
    content_df['rating_label']
    .dropna()
    .unique()
    .tolist()
)

language_dropdown = sorted(
    content_df['originalLanguage']
    .dropna()
    .unique()
    .tolist()
)

director_dropdown = sorted(
    content_df['director']
    .dropna()
    .unique()
    .tolist()
)

# =========================================================
# COMBINED FEATURES
# =========================================================

content_df['combined_features'] = (
    content_df['genre'].astype(str) + ' ' +
    content_df['director'].astype(str) + ' ' +
    content_df['rating'].astype(str) + ' ' +
    content_df['originalLanguage'].astype(str) + ' ' +
    content_df['title'].astype(str)
)

# =========================================================
# TF-IDF MATRIX
# =========================================================

tfidf = TfidfVectorizer(
    stop_words='english',
    dtype=np.float32
)

tfidf_matrix = tfidf.fit_transform(
    content_df['combined_features']
)

# =========================================================
# COLLABORATIVE FILTERING
# =========================================================

reader = Reader(rating_scale=(0, 100))

data = Dataset.load_from_df(
    collab_df[['criticName', 'title', 'originalScore']],
    reader
)

trainset = data.build_full_trainset()

svd_model = SVD(
    n_factors=50,
    random_state=42
)

svd_model.fit(trainset)

#===========================
#Filter Function
#=======================
def apply_filters(
    df,
    rating=None,
    language=None,
    year_min=1900,
    year_max=2025,
    director=None
):

    filtered_df = df.copy()

    if rating and rating != "All":

        filtered_df = filtered_df[
            filtered_df["rating"]
            .str.upper()
            == rating.upper()
        ]

    if language and language != "All":

        filtered_df = filtered_df[
            filtered_df["originalLanguage"]
            .str.contains(
                language,
                case=False,
                na=False
            )
        ]

    filtered_df = filtered_df[
        (filtered_df["releaseYear"] >= year_min)
        &
        (filtered_df["releaseYear"] <= year_max)
    ]

    if director and director != "All":

       director = (
        str(director)
        .lower()
        .replace(" ", "")
        .strip()
       )

       filtered_df = filtered_df[
        filtered_df["director"]
        .str.contains(
            director,
            case=False,
            na=False
        )
    ]

    return filtered_df

# =========================================================
# SORT RESULTS
# =========================================================

def sort_results(
    df,
    sort_by=None,
    ascending=False
):

    result = df.copy()

    if sort_by == "Audience Score":

        result = result.sort_values(
            by="bayesianAudienceScore",
            ascending=ascending
        )

    elif sort_by == "Tomato Meter":

        result = result.sort_values(
            by="bayesianTomatoMeter",
            ascending=ascending
        )

    elif sort_by == "Release Year":

        result = result.sort_values(
            by="releaseYear",
            ascending=ascending
        )

    elif sort_by == "Hybrid Score":

        result = result.sort_values(
            by="hybrid_score",
            ascending=ascending
        )
        
    elif    sort_by == "Quality Score":

        result = result.sort_values(
            by="quality_score",
            ascending=ascending
        )
        

    return result.reset_index(drop=True)

# =========================================================
# HYBRID RECOMMENDER FUNCTION
# =========================================================

def integrated_movie_recommender(
    search_input,
    top_n=10,
    rating=None,
    language=None,
    year_min=1900,
    year_max=2025,
    director_filter=None,
    sort_by=None,
    ascending=False
):

    query_clean = str(search_input).lower().strip()

    candidates = content_df.copy()

    # =====================================================
    # APPLY FILTERS FIRST
    # =====================================================

    candidates = apply_filters(
        df=candidates,
        rating=rating,
        language=language,
        year_min=year_min,
        year_max=year_max,
        director=director_filter
    )

    # =====================================================
    # SEARCH TYPE DETECTION
    # =====================================================

    is_title = query_clean in candidates["title"].values

    is_genre = candidates["genre"].str.contains(
        query_clean,
        case=False,
        na=False
    ).any()

    print("\n" + "=" * 70)
    print(f"🔍 SEARCH QUERY : {search_input}")

    top_result = None

    # =====================================================
    # TITLE SEARCH
    # =====================================================

    if is_title:

        print("📌 SEARCH TYPE : TITLE")

        top_result = candidates[
            candidates["title"] == query_clean
        ].head(1)

        idx = content_df[
            content_df["title"] == query_clean
        ].index[0]

        target_vector = tfidf_matrix[idx]

        sim_scores = linear_kernel(
            target_vector,
            tfidf_matrix
        ).flatten()

        candidates["content_score"] = sim_scores[
            candidates.index
        ]

        candidates = candidates[
            candidates["title"] != query_clean
        ]

    # =====================================================
    # GENRE SEARCH
    # =====================================================

    elif is_genre:

        print("📌 SEARCH TYPE : GENRE")

        candidates["content_score"] = candidates["genre"].apply(
            lambda x:
            1.0 if query_clean in str(x).lower()
            else 0.0
        )


    # =====================================================
    # FALLBACK
    # =====================================================

    else:

        print("⚠️ NO EXACT MATCH FOUND")

        candidates["content_score"] = 0.1

    # =====================================================
    # COLLABORATIVE SCORE
    # =====================================================

    target_profile = "Top Critic"

    candidates["svd_score"] = candidates["title"].apply(
        lambda movie:
        svd_model.predict(
            target_profile,
            movie
        ).est
    )

    min_score = candidates["svd_score"].min()
    max_score = candidates["svd_score"].max()

    if max_score != min_score:

        candidates["svd_score_norm"] = (
            candidates["svd_score"] - min_score
        ) / (
            max_score - min_score
        )

    else:

        candidates["svd_score_norm"] = 1.0

    # =====================================================
    # HYBRID SCORE
    # =====================================================

    candidates["hybrid_score"] = (
        0.6 * candidates["content_score"]
        +
        0.4 * candidates["svd_score_norm"]
    )

    # =====================================================
    # TOP-N BEST RECOMMENDATIONS
    # =====================================================

    final_output = (
        candidates
        .sort_values(
            "hybrid_score",
            ascending=False
        )
        .head(top_n)
        .copy()
    )

    # =====================================================
    # DISPLAY SORTING ONLY
    # =====================================================

    final_output = sort_results(
        final_output,
        sort_by=sort_by,
        ascending=ascending
    )

    # =====================================================
    # DISPLAY
    # =====================================================

    if is_title:

        print("\n🎬 TOP RESULT")
        print("-" * 70)

        print(
            top_result[
                [
                    "title",
                    "genre",
                    "director",
                    "rating",
                    "originalLanguage",
                    "releaseYear"
                ]
            ].to_string(index=False)
        )

        print("\n🔥 HYBRID FILTERED RESULTS ONLY")
        print("-" * 70)

    else:

        print("\n🔥 HYBRID FILTERED RESULTS ONLY")
        print("-" * 70)

    print(
        final_output[
            [
                "title",
                "genre",
                "director",
                "rating",
                "originalLanguage",
                "releaseYear",
                "audienceScore",
                "tomatoMeter",
                "hybrid_score",
                "quality_score"
            ]
        ].to_string(index=False)
    )

    # ============================================
    # SEARCH TYPE
    # ============================================

    if is_title:
        search_type = "TITLE"

    elif is_genre:
        search_type = "GENRE"

    else:
        search_type = "UNKNOWN"

    # ============================================
    # TOP RESULT JSON
    # ============================================

    if top_result is not None and not top_result.empty:

        top_result_json = top_result.to_dict(
            orient="records"
        )

    else:

        top_result_json = []

    # ============================================
    # RETURN FOR FLASK API
    # ============================================

    return {

        "search_type": search_type,

        "top_result": top_result_json,

        "results": final_output

    }
    
