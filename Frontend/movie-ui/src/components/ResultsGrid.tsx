import MovieCard from './MovieCard'

type Movie = {
  title: string
  genre: string
  director: string
  rating: string
  originalLanguage: string
  releaseYear: number
  audienceScore: number
  tomatoMeter: number
  hybrid_score: number
}

type Props = {
  movies: Movie[]
}

const ResultsGrid = ({ movies }: Props) => {
  if (!movies.length) {
    return (
      <div className="text-center mt-20 text-gray-400">
        Search movies to get recommendations
      </div>
    )
  }

  return (
    <div className="mt-14">
      <h2 className="text-3xl font-bold mb-8">
        Hybrid Recommendations
      </h2>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {movies.map((movie, index) => (
          <MovieCard
            key={index}
            movie={movie}
          />
        ))}
      </div>
    </div>
  )
}

export default ResultsGrid