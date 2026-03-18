function SearchBar({ value, onChange }) {
  return (
    <div className="search-bar-wrap">
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        type="text"
        placeholder="Search inside chat..."
        className="search-input"
      />
    </div>
  );
}

export default SearchBar;
