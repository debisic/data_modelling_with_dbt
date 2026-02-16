# Models

This directory contains all dbt models that transform raw taxi trip data into analytics ready tables. Models are organized in layers following the medallion architecture pattern.

##  Directory Structure

```
models/
├── staging/          # Raw data cleaning and standardization
├── intermediate/     # Business logic and joins
└── marts/           # Final analytics-ready models
    └── reporting/   # Specific reporting views
```

##  Layers

### 1. Staging (`staging/`)
**Purpose:** semi Clean and standardize raw source data

**Models:**
- `stg_yellow_tripdata.sql` - Yellow taxi trips (2019-2020)
- `stg_green_tripdata.sql` - Green taxi trips (2019-2020)
- `stg_fhv_tripdata.sql` - For-hire vehicle trips (2019)

**What happens here:**
- Data type casting and standardization
- Column renaming to consistent naming conventions
- Basic filtering (remove nulls, invalid records)
- Date/time parsing

**Materialization:** Views (default)

---

### 2. Intermediate (`intermediate/`)
**Purpose:** Apply business logic and create unified datasets

**Models:**
- `int_trips_unioned.sql` - Union of all taxi types
- `int_trips.sql` - Enriched trip data with calculations

**What happens here:**
- Unions across different source types
- Business calculations (trip duration, revenue, etc.)
- Data enrichment
- Complex transformations

**Materialization:** Views or Tables

---

### 3. Marts (`marts/`)
**Purpose:** Analytics-ready dimensional and fact tables

**Models:**
- `fct_trips.sql` - Fact table with all trip metrics
- `dim_vendors.sql` - Vendor dimension (SCD Type 0)
- `dim_zones.sql` - NYC taxi zone dimension

**What happens here:**
- Final business metrics
- Optimized for query performance
- Denormalization where appropriate
- Ready for BI tools

**Materialization:** Tables (for performance)

---

### 4. Reporting (`marts/reporting/`)
**Purpose:** Pre-aggregated views for specific business questions

**Models:**
- `fct_monthly_zone_revenue.sql` - Revenue by zone and month
- `fct_best_performing_zone_for_green-taxi_2020.sql` - Top zones for green taxis in 2020
- `green_trips_count_oct_2019.sql` - Trip counts for October 2019

**What happens here:**
- Pre-computed aggregations
- Optimized for specific dashboards
- Business-specific metrics

**Materialization:** Tables or Views

---

##  Data Flow

```
Raw Sources (prod schema)
    ↓
Staging Layer (clean data)
    ↓
Intermediate Layer (business logic)
    ↓
Marts Layer (analytics-ready)
    ↓
Reporting Layer (specific metrics)
```
