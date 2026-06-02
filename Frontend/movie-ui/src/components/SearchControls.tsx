import React from 'react'

import {
  FaSearch,
  FaStar,
  FaCalendar,
  FaFilter,
} from 'react-icons/fa'

type Filters = {
  rating: string
  language: string
  director: string
  yearMin: number
  yearMax: number
  sortBy: string
  ascending: boolean
  topN: number
}

type Props = {
  search: string
  setSearch: React.Dispatch<React.SetStateAction<string>>
  filters: Filters
  setFilters: React.Dispatch<React.SetStateAction<Filters>>
  onSearch: () => void
}

const SearchControls = ({
  search,
  setSearch,
  filters,
  setFilters,
  onSearch,
}: Props) => {
  return (
    <div className="bg-slate-900/70 backdrop-blur-xl rounded-3xl p-8 border border-cyan-500/30 shadow-[0_0_20px_rgba(0,255,255,0.2)]">

      <div className="flex flex-col lg:flex-row gap-4">
        
        <div className="flex-1 relative">
          <FaSearch className="absolute left-4 top-4 text-gray-400" />

          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search title, genre or director"
            className="w-full bg-slate-950 border border-slate-700 rounded-xl py-3 pl-12 pr-4 text-white outline-none focus:border-cyan-400"
          />
        </div>

        <button
          onClick={() => setSearch('')}
          className="px-6 py-3 rounded-xl bg-gray-700 hover:bg-gray-600"
        >
          Clear
        </button>

        <button
          onClick={onSearch}
          className="px-6 py-3 rounded-xl bg-cyan-400 text-black font-semibold hover:bg-cyan-300 flex items-center gap-2"
        >
          <FaSearch />
          Search
        </button>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-5 mt-8">

        <div>
          <label className="text-sm text-gray-300">
            Rating
          </label>

          <select
            value={filters.rating}
            onChange={(e) =>
              setFilters({
                ...filters,
                rating: e.target.value,
              })
            }
            className="mt-2 w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"
          >
            <option>All</option>
            <option>PG</option>
            <option>PG-13</option>
            <option>R</option>
          </select>
        </div>

        <div>
          <label className="text-sm text-gray-300">
            Language
          </label>

          <select
            value={filters.language}
            onChange={(e) =>
              setFilters({
                ...filters,
                language: e.target.value,
              })
            }
            className="mt-2 w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"
          >
            <option>All</option>
            <option>english</option>
            <option>french</option>
            <option>spanish</option>
          </select>
        </div>

        <div>
          <label className="text-sm text-gray-300">
            Sort By
          </label>

          <select
            value={filters.sortBy}
            onChange={(e) =>
              setFilters({
                ...filters,
                sortBy: e.target.value,
              })
            }
            className="mt-2 w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"
          >
            <option>Release Year</option>
            <option>Audience Score</option>
            <option>Tomato Meter</option>
          </select>
        </div>

        <div>
          <label className="text-sm text-gray-300">
            Director
          </label>

          <input
            type="text"
            value={filters.director}
            onChange={(e) =>
              setFilters({
                ...filters,
                director: e.target.value,
              })
            }
            placeholder="Director"
            className="mt-2 w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"
          />
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-5 mt-8">

        <div>
          <label className="text-sm text-gray-300">
            Min Year
          </label>

          <input
            type="number"
            value={filters.yearMin}
            onChange={(e) =>
              setFilters({
                ...filters,
                yearMin: Number(e.target.value),
              })
            }
            className="mt-2 w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"
          />
        </div>

        <div>
          <label className="text-sm text-gray-300">
            Max Year
          </label>

          <input
            type="number"
            value={filters.yearMax}
            onChange={(e) =>
              setFilters({
                ...filters,
                yearMax: Number(e.target.value),
              })
            }
            className="mt-2 w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"
          />
        </div>

        <div>
          <label className="text-sm text-gray-300">
            Recommendation Count
          </label>

          <input
            type="number"
            value={filters.topN}
            onChange={(e) =>
              setFilters({
                ...filters,
                topN: Number(e.target.value),
              })
            }
            className="mt-2 w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"
          />
        </div>
      </div>
    </div>
  )
}

export default SearchControls