import { useEffect, useState } from "react";
import api from "../services/api";
import type { ForecastResponse, WeatherRecord } from "../types/weather";

import Navbar from "../components/Navbar";
import SearchBar from "../components/SearchBar";
import WeatherCard from "../components/WeatherCard";
import ForecastList from "../components/ForecastList";
import SavedRecords from "../components/SavedRecords";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import AboutPMAccelerator from "../components/AboutPMAccelerator";

export default function Home() {
  const [location, setLocation] = useState("London");
  const [startDate, setStartDate] = useState("2026-06-28");
  const [endDate, setEndDate] = useState("2026-07-03");

  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [records, setRecords] = useState<WeatherRecord[]>([]);

  const [editingId, setEditingId] = useState<number | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function fetchRecords() {
    const response = await api.get<WeatherRecord[]>("/weather/");
    setRecords(response.data);
  }

  async function getForecast() {
    try {
      setLoading(true);
      setError("");

      const response = await api.get<ForecastResponse>(
        `/weather/forecast/${encodeURIComponent(location)}?days=5`
      );

      setForecast(response.data);
    } catch {
      setError("Could not fetch forecast. Please check the location and try again.");
    } finally {
      setLoading(false);
    }
  }

  async function saveWeatherRecord() {
    try {
      setLoading(true);
      setError("");

      if (editingId !== null) {
        await api.put(`/weather/${editingId}`, {
          location,
          start_date: startDate,
          end_date: endDate,
        });

        setEditingId(null);
      } else {
        await api.post("/weather/", {
          location,
          start_date: startDate,
          end_date: endDate,
        });
      }

      await fetchRecords();
    } catch {
      setError("Could not save weather record. Check the location and date range.");
    } finally {
      setLoading(false);
    }
  }

  function editRecord(record: WeatherRecord) {
    setEditingId(record.id);
    setLocation(record.location);
    setStartDate(record.start_date);
    setEndDate(record.end_date);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function cancelEdit() {
    setEditingId(null);
    setLocation("London");
    setStartDate("2026-06-28");
    setEndDate("2026-07-03");
  }

  async function deleteRecord(id: number) {
    try {
      setError("");
      await api.delete(`/weather/${id}`);
      await fetchRecords();
      await getForecast();

      if (editingId === id) {
        cancelEdit();
      }
    } catch {
      setError("Could not delete the selected record.");
    }
  }

  function useCurrentLocation() {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported by this browser.");
      return;
    }

    setLoading(true);
    setError("");

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const coords = `${position.coords.latitude},${position.coords.longitude}`;
        setLocation(coords);

        try {
          const response = await api.get<ForecastResponse>(
            `/weather/forecast/${encodeURIComponent(coords)}?days=5`
          );
          setForecast(response.data);
        } catch {
          setError("Could not fetch weather for your current location.");
        } finally {
          setLoading(false);
        }
      },
      () => {
        setError("Could not access your current location. Please allow location permission or enter a location manually.");
        setLoading(false);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
      }
    );
  }

  function exportCsv() {
    window.open("http://localhost:8001/export/csv", "_blank");
  }

  function exportJson() {
    window.open("http://localhost:8001/export/json", "_blank");
  }

  useEffect(() => {
    fetchRecords().catch(() => {
      setError("Could not load saved records.");
    });
  }, []);

  return (
    <>
      <Navbar />

      <main className="container">
        <SearchBar
          location={location}
          setLocation={setLocation}
          startDate={startDate}
          setStartDate={setStartDate}
          endDate={endDate}
          setEndDate={setEndDate}
          onSearch={getForecast}
          onSave={saveWeatherRecord}
          onUseCurrentLocation={useCurrentLocation}
        />

        {editingId !== null && (
          <section className="card edit-banner">
            <p>
              Editing record #{editingId}. Update the fields above, then click
              <strong> Save Weather Record</strong>.
            </p>
            <button className="secondary" onClick={cancelEdit}>
              Cancel Edit
            </button>
          </section>
        )}

        <ErrorMessage message={error} />
        {loading && <Loading />}

        <WeatherCard forecast={forecast} />

        <ForecastList days={forecast?.forecast.forecastday ?? []} />

        <section className="card">
          <h2>Export Data</h2>
          <div className="button-row">
            <button onClick={exportCsv}>Export CSV</button>
            <button onClick={exportJson}>Export JSON</button>
          </div>
        </section>

        <SavedRecords
          records={records}
          onEdit={editRecord}
          onDelete={deleteRecord}
        />

        <AboutPMAccelerator />
      </main>
    </>
  );
}