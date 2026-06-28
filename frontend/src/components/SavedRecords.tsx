import type { WeatherRecord } from "../types/weather";

interface SavedRecordsProps {
  records: WeatherRecord[];
  onEdit: (record: WeatherRecord) => void;
  onDelete: (id: number) => void;
}

export default function SavedRecords({
  records,
  onEdit,
  onDelete,
}: SavedRecordsProps) {
  return (
    <section className="card">
      <h2>Saved Weather Records</h2>

      {records.length === 0 ? (
        <p>No saved records yet.</p>
      ) : (
        <div className="records-grid">
          {records.map((record) => (
            <div className="record-card" key={record.id}>
              <h3>{record.location}</h3>
              <p>{record.condition}</p>
              <p>{record.temperature}°C</p>
              <p>
                {record.start_date} → {record.end_date}
              </p>
              <p>Humidity: {record.humidity}%</p>
              <p>Wind: {record.wind_speed} kph</p>

              <div className="button-row">
                <button className="secondary" onClick={() => onEdit(record)}>
                  Edit
                </button>

                <button className="danger" onClick={() => onDelete(record.id)}>
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}