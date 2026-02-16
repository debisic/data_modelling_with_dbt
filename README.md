# NYC Taxi Rides Analytics with dbt & DuckDB

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-1.7+-FF694B?style=flat&logo=dbt&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-Latest-FFF000?style=flat&logo=duckdb&logoColor=black)
![SQL](https://img.shields.io/badge/SQL-Parquet-4479A1?style=flat&logo=postgresql&logoColor=white)

A dbt (data build tool) project for analyzing NYC TLC taxi trip data using DuckDB as the data warehouse. This project transforms raw taxi trip records into analytical models for business intelligence and reporting.

##  Project Overview

This project processes NYC taxi trip data from three taxi types:
- **Yellow Taxi**: Traditional street-hail taxis
- **Green Taxi**: Street-hail taxis authorized for specific areas  
- **FHV (For-Hire Vehicles)**: App-based ride services

The data pipeline follows a layered medallion architecture transforming raw data into clean, analytics-ready models.


##  Architecture

```
Raw Data → Staging → Intermediate → Marts → Reporting
```

### Data Layers

1. **Staging** (`models/staging/`)
   - `stg_yellow_tripdata.sql`: semi Cleaned yellow taxi trips
   - `stg_green_tripdata.sql`: semi Cleaned green taxi trips
   - `stg_fhv_tripdata.sql`: semi Cleaned for-hire vehicle trips

2. **Intermediate** (`models/intermediate/`)
   - `int_trips_unioned.sql`: Union of all taxi trip types
   - `int_trips.sql`: Unified trip model with business logic

3. **Marts** (`models/marts/`)
   - `fct_trips.sql`: Fact table with trip metrics
   - `dim_vendors.sql`: Vendor dimension
   - `dim_zones.sql`: NYC taxi zone dimension

4. **Reporting** (`models/marts/reporting/`)
   - `fct_monthly_zone_revenue.sql`: Monthly revenue by zone
   - `fct_best_performing_zone_for_green-taxi_2020.sql`: Top zones analysis
   - `green_trips_count_oct_2019.sql`: Specific period analysis

##  Getting Started

### Prerequisites

- Python 3.8+
- dbt-core 1.7.0+
- dbt-duckdb adapter
- DuckDB

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/debisic/data_modelling_with_dbt.git
   cd data_modelling_with_dbt
   ```

2. **Install Python dependencies**
   ```bash
   pip install dbt-core dbt-duckdb requests
   ```

3. **Install dbt packages**
   ```bash
   dbt deps
   ```

4. **Configure your dbt profile**
   
   Create or update `~/.dbt/profiles.yml`:
   ```yaml
    taxi_rides_ny:
    target: prod
    outputs:
    # DuckDB Development profile
    dev:
        type: duckdb
        path: taxi_rides_ny.duckdb
        schema: dev
        threads: 1
        extensions:
        - parquet
        settings:
        memory_limit: '4GB'
        preserve_insertion_order: false

    # DuckDB Production profile
    prod:
        type: duckdb
        path: taxi_rides_ny.duckdb
        schema: prod
        threads: 1
        extensions:
        - parquet
        settings:
        memory_limit: '4GB'
        preserve_insertion_order: false
   ```

### Data Ingestion

Run the data ingestion script to download and prepare NYC taxi data:

```bash
python ingest.py
```

This script will:
- Download taxi trip data from NYC TLC (2019-2020)
- Convert CSV files to Parquet format
- Create raw tables in DuckDB (`prod` schema)
- Data types: Yellow (2019-2020), Green (2019-2020), FHV (2019)


### Build All Models
```bash
dbt run
```

### Generate Documentation
```bash
dbt docs generate
dbt docs serve
```

### Seed Reference Data
```bash
dbt seed
```

Seeds included:
- `taxi_zone_lookup.csv`: NYC taxi zone reference data
- `payment_type_lookup.csv`: Payment type descriptions


## Custom Macros

The project includes several custom macros in `macros/`:

- **`get_trip_duration_minutes`**: Calculate trip duration from pickup/dropoff timestamps
- **`get_vendor_data`**: Map vendor IDs to company names
- **`safe_cast`**: Safely cast data types with null handling

## 📁 Project Structure

```
taxi_rides_ny/
├── analyses/                   # Ad-hoc analysis queries
├── data/                       # Raw parquet files (gitignored)
│   ├── yellow/
│   ├── green/
│   └── fhv/
├── macros/                     # Reusable dbt macros
├── models/
│   ├── staging/               # Source data cleaning
│   ├── intermediate/          # Business logic transformations
│   └── marts/                 # Analytics-ready models
│       └── reporting/         # Reporting views
├── seeds/                     # Reference data CSV files
├── snapshots/                 # Slowly changing dimensions
├── tests/                     # Custom data tests
├── dbt_project.yml            # dbt project configuration
├── ingest.py                  # Data ingestion script
├── packages.yml               # dbt package dependencies
└── README.md                  # This file
```

## 🔗 Resources

- [dbt Documentation](https://docs.getdbt.com/)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

# Queries to tasks:
 ## NB
 - Queries to tasks can be found in this path: [models/marts/reporting](models/marts/reporting/)
 - Deduplication statistics is found in [analyses](analyses/)