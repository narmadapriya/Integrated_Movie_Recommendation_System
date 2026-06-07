from flask import Flask, request, jsonify
from flask_cors import CORS

from recommender import (
    integrated_movie_recommender,
    content_df,
    rating_dropdown,
    language_dropdown,
    director_dropdown
)

# =====================================
# FLASK APP
# =====================================

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

CORS(app)

# =====================================
# FILTER OPTIONS
# =====================================

ratings_list = sorted(
    content_df["rating"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

languages_list = sorted(
    content_df["originalLanguage"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

directors_list = sorted(
    content_df["director"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

# =====================================
# HOME
# =====================================

@app.route("/")
def home():

    return jsonify({
        "message":
        "Integrated Movie Recommendation API Running"
    })

# =====================================
# FILTER OPTIONS
# =====================================

@app.route(
    "/api/filter-options",
    methods=["GET"]
)
def get_filter_options():

    return jsonify({

        "ratings": ratings_list,

        "languages": languages_list,

        "directors": directors_list

    })

# =====================================
# RECOMMEND
# =====================================

@app.route(
    "/recommend",
    methods=["POST"]
)
def recommend():

    try:

        data = request.get_json()

        print("\nREQUEST DATA:")
        print(data)

        # =================================
        # INPUTS
        # =================================

        search_input = data.get(
            "search_input",
            ""
        )

        top_n = int(
            data.get(
                "top_n",
                10
            )
        )

        rating = data.get(
            "rating",
            "All"
        )

        language = data.get(
            "language",
            "All"
        )

        director_filter = data.get(
            "director_filter",
            ""
        )
        
        print("\nPARSED INPUTS")
        print("search_input =", search_input)
        print("director_filter =", director_filter)
        print("rating =", rating)
        print("language =", language)

        year_min = int(
            data.get(
                "year_min",
                1900
            )
        )

        year_max = int(
            data.get(
                "year_max",
                2025
            )
        )

        sort_by = data.get(
            "sort_by",
            "Hybrid Score"
        )

        ascending = str(
        data.get("ascending", False)
         ).lower() == "true"
        
        

        # =================================
        # DEFAULT VALUE CLEANUP
        # =================================

        if str(rating).lower() in [
            "select rating",
            "all ratings"
        ]:
            rating = "All"

        if str(language).lower() in [
            "select language",
            "all languages"
        ]:
            language = "All"

        if str(director_filter).lower() in [
            "all directors",
            "select director",
            "e.g. christopher nolan"
        ]:
            director_filter = ""

        # =================================
        # SORT MAPPING
        # =================================

        sort_map = {

    "hybrid score": "Hybrid Score",
    "hybrid_score": "Hybrid Score",

    "audience score": "Audience Score",
    "audiencescore": "Audience Score",
    "audienceScore": "Audience Score",

    "tomato meter": "Tomato Meter",
    "tomatoMeter": "Tomato Meter",
    "bayesianTomatoMeter": "Tomato Meter",

    "release year": "Release Year",
    "releaseYear": "Release Year",

    # NEW
    "quality score": "Quality Score",
    "quality_score": "Quality Score",
    "qualityScore": "Quality Score"
}

        sort_by = sort_map.get(
            str(sort_by).strip(),
            sort_by
        )

        if sort_by == "Relevance":
            sort_by = None

        # =================================
        # RECOMMENDER
        # =================================

        recommendation_data = (
            integrated_movie_recommender(

                search_input=search_input,

                top_n=top_n,

                rating=rating,

                language=language,

                year_min=year_min,

                year_max=year_max,

                director_filter=director_filter,

                sort_by=sort_by,

                ascending=ascending
            )
        )

        search_type = recommendation_data.get(
            "search_type",
            ""
        )

        top_result = recommendation_data.get(
            "top_result",
            []
        )

        results = recommendation_data.get(
            "results",
            None
        )

        # =================================
        # EMPTY RESULTS
        # =================================

        if results is None or results.empty:

            return jsonify({

                "success": True,

                "search_type": search_type,

                "top_result": top_result,

                "count": 0,

                "results": []

            })

        # =================================
        # CLEAN DATAFRAME
        # =================================

        results = results.copy()

        for col in results.columns:

            if "datetime" in str(
                results[col].dtype
            ):

                results[col] = (
                    results[col]
                    .astype(str)
                )

        results = results.replace(

            [
                "NaT",
                "nan",
                "None"
            ],

            ""
        )

        results = results.fillna("")

        # =================================
        # NUMPY TYPES → PYTHON TYPES
        # =================================

        results_json = []

        for row in results.to_dict(
            orient="records"
        ):

            cleaned_row = {}

            for k, v in row.items():

                if hasattr(v, "item"):

                    v = v.item()

                cleaned_row[k] = v

            results_json.append(
                cleaned_row
            )

        print(
            "\nReturned:",
            len(results_json)
        )



        # =================================
        # RESPONSE
        # =================================

        return jsonify({

            "success": True,

            "search_type": search_type,

            "top_result": top_result,

            "count": len(
                results_json
            ),

            "results": results_json

        })

    except Exception as e:

        print(
            "\nRECOMMEND ERROR:",
            str(e)
        )

        return jsonify({

            "success": False,

            "count": 0,

            "results": [],

            "error": str(e)

        }), 500



# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
