import { FiBell, FiSearch } from "react-icons/fi";

export default function Topbar() {
  return (
    <header className="sticky top-0 z-40 flex h-14 items-center justify-between
                      border-b border-gray-700 bg-gray-800/80 px-4 backdrop-blur">
      <h1 className="text-lg font-semibold text-primary">
        Assistant Médical AI
      </h1>

      <div className="flex items-center gap-4">
        <label className="relative hidden sm:block">
          <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="search"
            placeholder="Rechercher…"
            className="h-9 w-64 rounded-full border border-gray-700 bg-gray-800
                     pl-10 pr-4 text-sm shadow-sm placeholder:text-gray-400
                     focus:border-primary focus:outline-none"
          />
        </label>

        <button className="relative rounded-full p-2 text-gray-400 hover:bg-gray-700">
          <FiBell size={20} />
          <span className="absolute right-1 top-1 inline-flex h-2 w-2
                         rounded-full bg-primary"></span>
        </button>

        <div className="h-9 w-9 rounded-full bg-primary/90 text-center font-medium
                      text-white ring-2 ring-white">
          <span className="leading-9">J</span>
        </div>
      </div>
    </header>
  );
}