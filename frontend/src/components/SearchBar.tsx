interface SearchBarProps {
  location: string;
  setLocation: (value: string) => void;
  startDate: string;
  setStartDate: (value: string) => void;
  endDate: string;
  setEndDate: (value: string) => void;
  onSearch: () => void;
  onSave: () => void;
  onUseCurrentLocation: () => void;
}

export default function SearchBar({
  location,
  setLocation,
  startDate,
  setStartDate,
  endDate,
  setEndDate,
  onSearch,
  onSave,
  onUseCurrentLocation,
}: SearchBarProps) {
  return (
    <section className="card">
      <h2>Search Weather</h2>

      <div className="form-grid">
        <input
          type="text"
          placeholder="Enter city, postcode, landmark, or coordinates"
          value={location}
          onChange={(event) => setLocation(event.target.value)}
        />

        <input
          type="date"
          value={startDate}
          onChange={(event) => setStartDate(event.target.value)}
        />

        <input
          type="date"
          value={endDate}
          onChange={(event) => setEndDate(event.target.value)}
        />
      </div>

      <div className="button-row">
        <button onClick={onSearch}>Get Forecast</button>
        <button onClick={onSave}>Save Weather Record</button>
        <button className="secondary" onClick={onUseCurrentLocation}>
          Use Current Location
        </button>
      </div>
    </section>
  );
}