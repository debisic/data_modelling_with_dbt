# Analyses

This are reusable SQL queries for exploratory data analysis and investigations. Unlike models, these queries are **compiled but not executed** by dbt.

## Purpose

Analyses are used for:
- Data quality investigations
- Exploratory analysis
- One-time queries that don't need to be materialized
- Documentation of findings

## Files

### `analysis_dedup_stats.sql`
Statistical analysis of duplicate record removal across taxi trip datasets.

**What it does:**
- Compares record counts before and after deduplication
- Calculates duplicate percentages for green and yellow taxi trips
- Helps validate data cleaning effectiveness

**Usage:**
```bash
# Compile the analysis
dbt compile --select analysis_dedup_stats

# Run manually using DuckDB
duckdb taxi_rides_ny.duckdb < target/compiled/taxi_rides_ny/analyses/analysis_dedup_stats.sql
```

## Running Analyses

To compile all analyses:
```bash
dbt compile --select analyses.*
```

Compiled queries are available in:
```
target/compiled/taxi_rides_ny/analyses/
```

## Adding New Analyses

1. Create a new `.sql` file in this directory
2. Write your SQL query (can reference models using `{{ ref('model_name') }}`)
3. Compile with `dbt compile`
4. Execute the compiled SQL manually as needed
