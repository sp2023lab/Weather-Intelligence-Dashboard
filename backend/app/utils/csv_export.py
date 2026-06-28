import csv
import io


def records_to_csv(records):
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Location",
        "Latitude",
        "Longitude",
        "Start Date",
        "End Date",
        "Temperature",
        "Feels Like",
        "Humidity",
        "Wind Speed",
        "Condition",
        "Created At",
    ])

    for record in records:
        writer.writerow([
            record.id,
            record.location,
            record.latitude,
            record.longitude,
            record.start_date,
            record.end_date,
            record.temperature,
            record.feels_like,
            record.humidity,
            record.wind_speed,
            record.condition,
            record.created_at,
        ])

    output.seek(0)
    return output