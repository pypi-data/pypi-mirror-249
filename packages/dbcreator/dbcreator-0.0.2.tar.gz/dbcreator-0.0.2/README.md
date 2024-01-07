# dbcreator

The `dbcreator` library provides an interface for creating lightweight databases from files.  It currently supports duckdb and s3 parquet files, though there are plans to add sqlite and other source file locations and types in the future.

## Usage

### Creating DuckDB Database from Parquet Files

```python
from flexpath import create_duckdb_database_from_local_parquet

# Example for creating database from S3 Parquet files
create_duckdb_database_from_s3_parquet('target_db.duckdb', FlexPath("s3://bucket-name/prefix"), create_tables=True)
```
> The library assumes a specific file naming convention for schema and table name extraction.
> For example, a file named `s3://bucket-name/prefix/folder/schemaname_table_name.parquet` will be parsed as a table named `table_name` in a schema named `schemaname`.

### DuckDBConnection

```python
from flexpath import DuckDBConnection

with DuckDBConnection('my_database.duckdb') as con:
    # Perform database operations using 'con'
```

### FlexPath

```python
from flexpath import FlexPath

# Example for local path
local_path = FlexPath("/local/path/to/file.parquet")

# Example for S3 path
s3_path = FlexPath("s3://bucket-name/prefix/to/file.parquet")
```

## Installation

`pip install dbcreator`