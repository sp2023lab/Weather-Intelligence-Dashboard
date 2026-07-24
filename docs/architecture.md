# Weather Intelligence Dashboard Architecture

## System overview

The Weather Intelligence Dashboard uses a layered architecture to retrieve weather data, validate and process requests, cache and persist results, and present information through a frontend dashboard and CSV exports.

```mermaid
flowchart LR
    User[User]

    subgraph Frontend["Frontend"]
        Dashboard[Weather Dashboard]
        Search[Search and Filters]
        ExportUI[CSV Export Controls]
    end

    subgraph API["FastAPI Backend"]
        Main[Application Entry Point]
        Router[API Router]
        WeatherRoute[Weather Endpoints]
        ExportRoute[Export Endpoints]
        HealthRoute[Health Endpoint]
    end

    subgraph Services["Service Layer"]
        WeatherService[Weather Service]
        ExportService[Export Service]
        Validators[Validators]
    end

    subgraph Integration["External Integration"]
        WeatherClient[WeatherAPI Client]
        WeatherAPI[External Weather API]
    end

    subgraph Data["Data and Caching"]
        Repository[Weather Repository]
        Database[(Database)]
        Cache[(Cache)]
    end

    User --> Dashboard
    Dashboard --> Search
    Dashboard --> ExportUI

    Search --> WeatherRoute
    ExportUI --> ExportRoute

    Main --> Router
    Router --> WeatherRoute
    Router --> ExportRoute
    Router --> HealthRoute

    WeatherRoute --> Validators
    WeatherRoute --> WeatherService
    ExportRoute --> ExportService

    WeatherService --> Cache
    WeatherService --> WeatherClient
    WeatherClient --> WeatherAPI
    WeatherService --> Repository
    Repository --> Database

    ExportService --> Repository

    WeatherRoute --> Dashboard
    ExportRoute --> ExportUI
```