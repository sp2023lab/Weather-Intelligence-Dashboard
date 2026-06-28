import type { ForecastResponse } from "../types/weather";

interface WeatherCardProps {
  forecast: ForecastResponse | null;
}

export default function WeatherCard({ forecast }: WeatherCardProps) {
  if (!forecast) return null;

  return (
    <section className="card weather-card">
      <div>
        <h2>
          {forecast.location.name}, {forecast.location.country}
        </h2>
        <p>{forecast.location.localtime}</p>
      </div>

      <div className="weather-main">
        <img src={`https:${forecast.current.condition.icon}`} alt="weather icon" />
        <div>
          <h3>{forecast.current.temp_c}°C</h3>
          <p>{forecast.current.condition.text}</p>
        </div>
      </div>

      <div className="weather-grid">
        <p>Feels like: {forecast.current.feelslike_c}°C</p>
        <p>Humidity: {forecast.current.humidity}%</p>
        <p>Wind: {forecast.current.wind_kph} kph</p>
        <p>UV Index: {forecast.current.uv}</p>
      </div>
    </section>
  );
}