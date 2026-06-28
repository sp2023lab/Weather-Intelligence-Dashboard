import type { ForecastDay } from "../types/weather";

interface ForecastListProps {
  days: ForecastDay[];
}

export default function ForecastList({ days }: ForecastListProps) {
  if (!days.length) return null;

  return (
    <section className="card">
      <h2>5-Day Forecast</h2>

      <div className="forecast-grid">
        {days.map((day) => (
          <div className="forecast-card" key={day.date}>
            <h3>{day.date}</h3>
            <img src={`https:${day.day.condition.icon}`} alt="forecast icon" />
            <p>{day.day.condition.text}</p>
            <p>Avg: {day.day.avgtemp_c}°C</p>
            <p>
              {day.day.mintemp_c}°C - {day.day.maxtemp_c}°C
            </p>
            <p>Rain chance: {day.day.daily_chance_of_rain}%</p>
          </div>
        ))}
      </div>
    </section>
  );
}