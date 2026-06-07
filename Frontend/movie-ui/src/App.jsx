import React, {
  useState,
  useEffect,
  useRef,
} from "react";

import "remixicon/fonts/remixicon.css";

import {
  Search,
  X,
  User,
  Calendar,
  Globe,
} from "lucide-react";

import "./App.css";

export default function App() {

  // =========================
  // STATE
  // =========================

  const [search, setSearch] =
    useState("");

  const [searched, setSearched] =
    useState(false);

  const [results, setResults] =
    useState([]);

  const [topResult, setTopResult] =
    useState([]);

  const [searchType, setSearchType] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [rating, setRating] =
    useState("Select rating");

  const [language, setLanguage] =
    useState("Select language");

  const [director, setDirector] =
    useState("");

  const [ratingSearch, setRatingSearch] =
    useState("");

  const [languageSearch, setLanguageSearch] =
    useState("");

  const [yearMin, setYearMin] =
    useState("1900");

  const [yearMax, setYearMax] =
    useState("2025");

  const [yearError, setYearError] =
    useState("");

  const [sortBy, setSortBy] =
    useState("");

  const [ascending, setAscending] =
    useState(false);

  const [topN, setTopN] =
    useState(10);

  const resultsRef =
    useRef(null);

  const genreResultsRef =
    useRef(null);

  const [showDirectorDropdown, setShowDirectorDropdown] =
    useState(false);

  const [showRatingDropdown, setShowRatingDropdown] =
    useState(false);

  const [showLanguageDropdown, setShowLanguageDropdown] =
    useState(false);

  const [filteredDirectors, setFilteredDirectors] =
    useState([]);

  const [filteredRatings, setFilteredRatings] =
    useState([]);

  const [filteredLanguages, setFilteredLanguages] =
    useState([]);
  
  const [showTopBtn, setShowTopBtn] = useState(false);

  const [resultCount, setResultCount] =
  useState(0);  

  // =========================
  // BACKEND FILTER OPTIONS
  // =========================

  const [
    backendOptions,
    setBackendOptions,
  ] = useState({

    ratings: [],
    languages: [],
    directors: [],

  });

  // =========================
  // FETCH FILTERS
  // =========================

  useEffect(() => {

    fetch(
      "http://127.0.0.1:5000/api/filter-options"
    )
      .then((res) =>
        res.json()
      )
      .then((data) => {

        setBackendOptions({

          ratings:
            data.ratings || [],

          languages:
            data.languages || [],

          directors:
            data.directors || [],

        });

      })
      .catch((err) =>
        console.log(
          "Filter fetch error:",
          err
        )
      );

  }, []);



  // =========================
  // FILTER DIRECTORS
  // =========================

  useEffect(() => {

    if (!director.trim()) {

      setFilteredDirectors(
        backendOptions.directors.slice(0, 20)
      );

    } else {

      const filtered =
        backendOptions.directors.filter((d) =>
          d.toLowerCase().includes(
            director.toLowerCase()
          )
        );

      setFilteredDirectors(filtered);

    }

  }, [director, backendOptions]);

  // =========================
  // FILTER RATINGS
  // =========================

  useEffect(() => {

    const filtered =
      backendOptions.ratings.filter((r) =>
        r.toLowerCase().includes(
          ratingSearch.toLowerCase()
        )
      );

    setFilteredRatings(filtered);

  }, [ratingSearch, backendOptions]);

  // =========================
  // FILTER LANGUAGES
  // =========================

  useEffect(() => {

    const filtered =
      backendOptions.languages.filter((l) =>
        l.toLowerCase().includes(
          languageSearch.toLowerCase()
        )
      );

    setFilteredLanguages(filtered);

  }, [languageSearch, backendOptions]);

  //------scroll to top button------

  useEffect(() => {
  const handleScroll = () => {
    setShowTopBtn(window.scrollY > 300);
  };

  window.addEventListener("scroll", handleScroll);

  return () => {
    window.removeEventListener("scroll", handleScroll);
  };
}, []);

  // =========================
  // HANDLE SEARCH
  // =========================

  const handleSearch = async () => {

   if (
  !search.trim() &&
  !director.trim()
) {
  alert(
    "Enter a title/genre or select a director"
  );
  return;
}

    const minYear = Number(yearMin);
const maxYear = Number(yearMax);

if (

  !yearMin ||
  !yearMax ||

  isNaN(minYear) ||
  isNaN(maxYear) ||

  minYear < 1900 ||
  maxYear > 2025 ||

  yearMin.length !== 4 ||
  yearMax.length !== 4 ||

  minYear > maxYear

) {

  setYearError(
    "Enter valid years (1900–2025)"
  );

  return;
}

setYearError("");

    setYearError("");

    try {

      setLoading(true);

      setSearched(true);

      const response =
        await fetch(
          "http://127.0.0.1:5000/recommend",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({

              search_input:
                search,

              top_n:
                topN,

              rating:
                !rating
                  ? "All"
                  : rating,

              language:
                !language
                  ? "All"
                  : language,

              director_filter:
                director || "",

              year_min:
                yearMin || 1900,

              year_max:
                yearMax || 2025,

              sort_by:
                sortBy,

              ascending:
                ascending,

            }),
          }
        );

      if (!response.ok) {

        throw new Error(
          "Backend request failed"
        );

      }

      const data = await response.json();

if (!data.success) {
  alert(data.error);
  return;
}

     
      setSearchType(
        data.search_type || ""
      );

      setTopResult(
        data.top_result || []
      );

      setResults(
        data.results || []
      );

      setResultCount(
        data.count || 0
     );

      setTimeout(() => {

        const offset = 30;

        if (
          data.search_type === "TITLE" &&
          resultsRef.current
        ) {

          const elementPosition =
            resultsRef.current
              .getBoundingClientRect()
              .top;

          const offsetPosition =
            elementPosition +
            window.pageYOffset -
            offset;

          window.scrollTo({

            top: offsetPosition,
            behavior: "smooth",

          });

        } else if (
  (data.search_type === "GENRE" ||
   data.search_type === "DIRECTOR") &&
  genreResultsRef.current
) {

          const elementPosition =
            genreResultsRef.current
              .getBoundingClientRect()
              .top;

          const offsetPosition =
            elementPosition +
            window.pageYOffset -
            offset;

          window.scrollTo({

            top: offsetPosition,
            behavior: "smooth",

          });

        }

      }, 200);

    } catch (err) {

      console.log(err);

      alert(
        "Cannot connect to Flask backend"
      );

    } finally {

      setLoading(false);

    }

  };
  // =========================
  // CLEAR
  // =========================
    const handleClear = () => {

  setSearch("");

  setResults([]);
  setTopResult([]);
  setSearchType("");
  setSearched(false);


  // FILTERS
  setRating("Select rating");
  setLanguage("Select language");
  setDirector("");

  // IMPORTANT
  setRatingSearch("");
  setLanguageSearch("");

  // YEAR
  setYearMin("1900");
  setYearMax("2025");
  setYearError("");

  // SORT
  setSortBy("");
  setAscending(false);

  // RESULT COUNT
  setTopN(10);
  setResultCount(0);

  // DROPDOWNS
  setShowDirectorDropdown(false);
  setShowRatingDropdown(false);
  setShowLanguageDropdown(false);
};
  
  // =========================
  // MOVIE CARD
  // =========================

  const MovieCard = ({ movie }) => (

    <div className="movie-card">

      <div className="movie-header">

        <div className="movie-title-row">

          <h2 className="movie-title">
            {movie.title}
          </h2>

          <div className="rating-badge">
            {movie.rating || "NR"}
          </div>

        </div>

        <div className="genre-tags">

          {String(movie.genre || "")
            .split(",")
            .slice(0, 3)
            .map((g, i) => (

              <span
                key={i}
                className="genre-tag"
              >
                {g.trim()}
              </span>

            ))}

        </div>

      </div>

      <div className="movie-info">

        <div className="movie-detail">

          <User size={14} />

          <span>
            {movie.director || "Unknown"}
          </span>

        </div>

        <div className="movie-detail">

          <Calendar size={14} />

          <span>
            {movie.releaseYear || "N/A"}
          </span>

        </div>

        <div className="movie-detail">

          <i className="ri-time-line"></i>

          <span>
            {movie.runtimeMinutes
              ? `${movie.runtimeMinutes} min`
              : "N/A"}
          </span>

        </div>

        <div className="movie-detail">

          <Globe size={14} />

          <span>
            {movie.originalLanguage || "Unknown"}
          </span>

        </div>

        <div className="movie-detail">

          <i className="ri-bar-chart-fill"></i>

          <span>
            {movie.hybrid_score !== undefined
              ? Number(movie.hybrid_score).toFixed(3)
              : "0.000"}
          </span>

        </div>

      </div>

      <div className="scores-section">

        <div className="score-box audience-box">

          <i className="ri-star-fill"></i>

          <span>
            {movie.audienceScore ?? 0}%
          </span>

        </div>

        <div className="score-box tomato-box">

          <i className="ri-fire-line"></i>

          <span>
            {movie.tomatoMeter ?? 0}%
          </span>

        </div>
            <div className="score-box sentiment-box">
  <i className="ri-chat-smile-3-fill"></i>

  <span>
    {movie.quality_score !== undefined &&
     movie.quality_score !== null &&
     movie.quality_score !== ""
      ? `${Math.round(movie.quality_score)}%`
      : "0%"}
  </span>
</div>

      </div>

    </div>

  );

  // =========================
  // UI
  // =========================

  const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
};

  return (

    <div className="app">

      <div className="container">

        {/* HEADER */}

        <div className="header">

          <h1>
            Integrated Movie
            <br />
            Recommendation System
          </h1>

          <p>
            Find your next favorite movie
            using advanced hybrid
            filtering.
          </p>

        </div>

        {/* FILTER CARD */}

        <div className="filter-card">

          {/* SEARCH */}

          <div className="search-section">

            <div className="search-input-wrapper">

              <Search size={18} />

              <input
                className="search-input"
                placeholder="Enter Movie Title or up to 10 Genres (comma-separated)..."
                value={search}
                onChange={(e) =>
                  setSearch(
                    e.target.value
                  )
                }
                onKeyDown={(e) =>
                  e.key === "Enter" &&
                  handleSearch()
                }
              />

               <button
                className="clear-btn"
              onClick={handleClear}
>
                <X size={16} />
              </button>

            </div>

            <button
              className="btn btn-secondary"
              onClick={handleClear}
            >
              Clear
            </button>

            <button
              className="btn btn-primary"
              onClick={handleSearch}
              disabled={loading}
            >
              <i className="ri-equalizer-line"></i>

              {loading
                ? "Searching..."
                : "Get Recommendations"}
            </button>

          </div>

          {/* FILTERS */}

          <div className="filter-grid">

            {/* RATING */}

            <div className="filter-group">

              <label>Rating</label>

              <div className="director-dropdown-wrapper">

                <input
                  type="text"
                  className="custom-director-input"
                  placeholder="Select rating"
                  value={ratingSearch}
                  onChange={(e) => {

                    setRatingSearch(
                      e.target.value
                    );

                    setShowRatingDropdown(true);

                  }}
                  onFocus={() =>
                    setShowRatingDropdown(true)
                  }
                  onBlur={() =>
                    setTimeout(
                      () =>
                        setShowRatingDropdown(false),
                      150
                    )
                  }
                />

                {showRatingDropdown && (

                  <div className="director-dropdown">

                    {filteredRatings.map((item, i) => (

                      <div
                        key={i}
                        className="director-item"
                        onMouseDown={() => {

                          setRating(item);

                          setRatingSearch(item);

                          setShowRatingDropdown(false);

                        }}
                      >
                        {item}
                      </div>

                    ))}

                  </div>

                )}

              </div>

            </div>

            {/* LANGUAGE */}

            <div className="filter-group">

              <label>Language</label>

              <div className="director-dropdown-wrapper">

                <input
                  type="text"
                  className="custom-director-input"
                  placeholder="Select language"
                  value={languageSearch}
                  onChange={(e) => {

                    setLanguageSearch(
                      e.target.value
                    );

                    setShowLanguageDropdown(true);

                  }}
                  onFocus={() =>
                    setShowLanguageDropdown(true)
                  }
                  onBlur={() =>
                    setTimeout(
                      () =>
                        setShowLanguageDropdown(false),
                      150
                    )
                  }
                />

                {showLanguageDropdown && (

                  <div className="director-dropdown">

                    {filteredLanguages.map((item, i) => (

                      <div
                        key={i}
                        className="director-item"
                        onMouseDown={() => {

                          setLanguage(item);

                          setLanguageSearch(item);

                          setShowLanguageDropdown(false);

                        }}
                      >
                        {item}
                      </div>

                    ))}

                  </div>

                )}

              </div>

            </div>

            {/* DIRECTOR */}

            <div className="filter-group">

              <label>Director</label>

              <div className="director-dropdown-wrapper">

                <input
                  type="text"
                  className="custom-director-input"
                  placeholder="e.g. Christopher Nolan"
                  value={director}
                  onChange={(e) =>
                    setDirector(
                      e.target.value
                    )
                  }
                  onFocus={() =>
                    setShowDirectorDropdown(true)
                  }
                  onBlur={() =>
                    setTimeout(
                      () =>
                        setShowDirectorDropdown(false),
                      150
                    )
                  }
                />

                {showDirectorDropdown && (

                  <div className="director-dropdown">

                    {filteredDirectors
                      .slice(0, 20)
                      .map((item, i) => (

                        <div
                          key={i}
                          className="director-item"
                          onMouseDown={() => {

                            setDirector(item);

                            setShowDirectorDropdown(false);

                          }}
                        >
                          {item}
                        </div>

                      ))}

                  </div>

                )}

              </div>

            </div>

            {/* YEAR RANGE */}

  <div className="filter-group">

    <label>Year Range</label>

    <div className="year-range">

      <input
        type="number"
        value={yearMin}
        onChange={(e) => {

          const value =
            e.target.value;

          if (value.length > 4) {

            setYearError(
              "Invalid year"
            );

            return;
          }

          setYearMin(value);

          if (value.length === 4) {

            const year =
              Number(value);

            if (
              year < 1900 ||
              year > 2025
            ) {

              setYearError(
                "Invalid year"
              );

            } else {

              setYearError("");

            }

          } else {

            setYearError("");

          }

        }}
      />

      <span>-</span>

      <input
        type="number"
        value={yearMax}
        onChange={(e) => {

          const value =
            e.target.value;

          if (value.length > 4) {

            setYearError(
              "Invalid year"
            );

            return;
          }

          setYearMax(value);

          if (value.length === 4) {

            const year =
              Number(value);

            if (
              year < 1900 ||
              year > 2025
            ) {

              setYearError(
                "Invalid year"
              );

            } else {

              setYearError("");

            }

          } else {

            setYearError("");

          }

        }}
      />

    </div>

    {yearError && (

      <div className="year-error">

        {yearError}

      </div>

    )}

  </div>
          </div>

      {/* BOTTOM CONTROLS */}
<div className="bottom-controls">

  {/* LEFT + RIGHT BLOCKS */}
  <div className="bottom-row">

    {/* LEFT BLOCK */}
    <div className="control-group">

      {/* LABEL + LINE */}
      <div className="section-title">
        <span className="quick-label">
          <i className="ri-filter-2-line"></i>
          Quick Sort
        </span>
        
      </div>

      {/* BUTTONS + SORT ICON */}
      <div className="bottom-left">

        <div className="quick-sort-buttons">


  <button
    className={`sort-chip hybrid-chip ${
      sortBy === "Hybrid Score"
        ? "active"
        : ""
    }`}
    onClick={() =>
      setSortBy("Hybrid Score")
    }
  >
    <i className="ri-bar-chart-fill"></i>
    Hybrid Score
  </button>        

  <button
    className={`sort-chip audience-chip ${
      sortBy === "Audience Score"
        ? "active"
        : ""
    }`}
    onClick={() =>
      setSortBy("Audience Score")
    }
  >
    <i className="ri-star-fill"></i>
    Audience Score
  </button>

  <button
    className={`sort-chip tomato-chip ${
      sortBy === "Tomato Meter"
        ? "active"
        : ""
    }`}
    onClick={() =>
      setSortBy("Tomato Meter")
    }
  >
    <i className="ri-fire-line"></i>
    Tomato Meter
  </button>

  <button
    className={`sort-chip year-chip ${
      sortBy === "Release Year"
        ? "active"
        : ""
    }`}
    onClick={() =>
      setSortBy("Release Year")
    }
  >
    <i className="ri-calendar-event-fill"></i>
    Release Year
  </button>

  <button
    className={`sort-chip sentiment-chip ${
  sortBy === "Quality Score"
    ? "active"
    : ""
   }`}
    onClick={() =>
      setSortBy("Quality Score")
    }
  >
    <i className="ri-chat-smile-3-fill"></i>
    Critic Sentiment
  </button>

</div>


        {/* SORT BUTTON */}
        <button
          className="sort-btn"
          title={`Sort ${ascending ? "Ascending" : "Descending"}`}
          onClick={() => setAscending(!ascending)}
        >
          {ascending ? (
            <i className="ri-arrow-up-line"></i>
          ) : (
            <i className="ri-arrow-down-line"></i>
          )}
        </button>

      </div>
    </div>

    {/* RIGHT BLOCK */}
    <div className="control-group right-group">

      {/* LABEL + LINE */}
      <div className="section-title">
        <span className="result-label">
          Result Count
        </span>
        
      </div>

      {/* SLIDER */}
      <div className="bottom-right">

        <div className="slider-container">
          <input
            type="range"
            min="1"
            max="20"
            value={topN}
            onChange={(e) => setTopN(Number(e.target.value))}
          />

          <span className="result-count">
            {topN}
          </span>
        </div>

      </div>
    </div>

  </div>
</div>    
      

</div> 


        {/* RESULTS */}

        <div className="results-wrapper">

          {/* TOP RESULT */}

          {searchType === "TITLE" &&
            topResult.length > 0 && (

              <div
                ref={resultsRef}
                className="top-result-section"
              >

                <div className="results-header">

                  <h2>
                    Top Result
                  </h2>

                  <div className="results-line"></div>

                </div>

                <div className="movie-grid">

                  <MovieCard
                    movie={topResult[0]}
                  />

                </div>

              </div>

            )}

          {/* RESULTS */}

          {results.length > 0 && (

            <div
              ref={genreResultsRef}
              className="results-section"
            >

              <div className="results-header">

                <h2>
                  Hybrid Filtered Results
                </h2>

                <div className="results-line"></div>

                <span className="results-count">
                  <span className="results-count">
                    {resultCount} Movies
                  </span>
                </span>

              </div>

              <div className="movie-grid">

                {results.map(
                  (movie, index) => (

                    <MovieCard
                      key={index}
                      movie={movie}
                    />

                  )
                )}

              </div>

            </div>

          )}

          {/* NO RESULTS */}

          {!loading &&
            searched &&
            results.length === 0 &&
            topResult.length === 0 && (

              <div className="no-results">
                No recommendations found
              </div>

            )}

        </div>

      </div>

      {showTopBtn && (
  <button
    className="scroll-top-btn"
    onClick={scrollToTop}
  >
    <i className="ri-arrow-up-line"></i>
  </button>
)}

    </div>

  );

}
