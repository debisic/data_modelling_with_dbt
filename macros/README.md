# Macros

This directory contains reusable Jinja macros that extend dbt's functionality and provide custom logic for data transformations.

## Available Macros

### `get_trip_duration_minutes.sql`
**Purpose:** Calculate trip duration in minutes from pickup and dropoff timestamps.

**Usage:**
```sql
{{ get_trip_duration_minutes('pickup_datetime', 'dropoff_datetime') }}
```

**Returns:** Trip duration in minutes as a numeric value

**Example:**
```sql
SELECT
    trip_id,
    {{ get_trip_duration_minutes('lpep_pickup_datetime', 'lpep_dropoff_datetime') }} as trip_duration_min
FROM {{ ref('stg_green_tripdata') }}
```

---

### `get_vendor_data.sql`
**Purpose:** Map vendor IDs to company names.

**Usage:**
```sql
{{ get_vendor_data('vendor_id') }}
```

**Mappings:**
- `1` → Creative Mobile Technologies, LLC
- `2` → VeriFone Inc.

**Example:**
```sql
SELECT
    vendor_id,
    {{ get_vendor_data('vendor_id') }} as vendor_name
FROM {{ ref('fct_trips') }}
```

---

### `safe_cast.sql`
**Purpose:** Safely cast data types with null handling to prevent errors during transformation.

**Usage:**
```sql
{{ safe_cast('column_name', 'target_type') }}
```

**Example:**
```sql
SELECT
    {{ safe_cast('passenger_count', 'INTEGER') }} as passenger_count,
    {{ safe_cast('fare_amount', 'DOUBLE') }} as fare_amount
FROM raw_tripdata
```

---

## Configuration

### `macros_properties.yml`
Defines macro metadata, documentation, and configuration properties.



## Best Practices

- Keep macros focused on a single responsibility
- Document parameters and return values
- Test macros thoroughly in development
- Consider performance implications for complex macros
