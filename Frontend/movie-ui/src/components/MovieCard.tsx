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
  movie: Movie
}

const MovieCard = ({ movie }: Props) => {
  return (
    <div className="bg-slate-900/80 backdrop-blur-xl rounded-2xl p-5 border border-cyan-500/20 hover:border-cyan-400 transition-all hover:scale-[1.02]">

      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-bold capitalize">
          {movie.title}
        </h2>

        <span className="bg-cyan-400 text-black text-xs px-3 py-1 rounded-full font-bold">
          {movie.hybrid_score.toFixed(2)}
        </span>
      </div>

      <div className="space-y-3 text-sm text-gray-300">

        <div>
          🎭 {movie.genre}
        </div>

        <div>
          🎬 {movie.director}
        </div>

        <div>
          ⭐ Rating: {movie.rating}
        </div>

        <div>
          🌍 {movie.originalLanguage}
        </div>

        <div>
          📅 {movie.releaseYear}
        </div>
      </div>

      <div className="flex justify-between mt-6">

        <div className="bg-slate-950 px-3 py-2 rounded-lg">
          Audience: {movie.audienceScore}
        </div>

        <div className="bg-slate-950 px-3 py-2 rounded-lg">
          🍅 {movie.tomatoMeter}
        </div>
      </div>
    </div>
  )
}

export default MovieCard