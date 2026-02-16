# Seeds

This directory contains CSV files with static reference data that is version controlled and loaded into the database using `dbt seed`.

## Purpose

Seeds are used for:
- Small lookup tables
- Static reference data
- Data that changes infrequently
- Configuration values
- Mapping tables

## Available Seeds

### `taxi_zone_lookup.csv`
**Purpose:** NYC Taxi Zone reference data for geographic analysis

**Columns:**
- `LocationID` - Unique identifier for each taxi zone
- `Borough` - NYC borough (Manhattan, Brooklyn, Queens, Bronx, Staten Island)
- `Zone` - Specific zone name
- `service_zone` - Service classification (Yellow, Green, EWR)

**Usage:**
```sql
SELECT 
    t.trip_id,
    pz.zone as pickup_zone,
    dz.zone as dropoff_zone
FROM {{ ref('fct_trips') }} t
LEFT JOIN {{ ref('taxi_zone_lookup') }} pz 
    ON t.pickup_location_id = pz.locationid
LEFT JOIN {{ ref('taxi_zone_lookup') }} dz 
    ON t.dropoff_location_id = dz.locationid
```

**Source:** [NYC TLC Taxi Zones](https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/d3c5-ddgc)

---

### `payment_type_lookup.csv`
**Purpose:** Decode payment type codes to human-readable descriptions

**Columns:**
- `payment_type` - Numeric payment type code
- `payment_type_description` - Human-readable description

**Mappings:**
- `1` → Credit card
- `2` → Cash
- `3` → No charge
- `4` → Dispute
- `5` → Unknown
- `6` → Voided trip

**Usage:**
```sql
SELECT 
    t.trip_id,
    pt.payment_type_description
FROM {{ ref('fct_trips') }} t
LEFT JOIN {{ ref('payment_type_lookup') }} pt 
    ON t.payment_type = pt.payment_type
```

---

## Configuration

### `seeds_properties.yml`
Defines seed metadata, data types, and configuration properties.

## Loading Seeds

### Load all seeds:
```bash
dbt seed
```