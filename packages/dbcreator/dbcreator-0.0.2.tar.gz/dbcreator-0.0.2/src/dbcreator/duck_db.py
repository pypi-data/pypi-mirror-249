import duckdb
import boto3
import os
from pathlib import Path


class FlexPath(type(Path())):

    def is_s3(self):
        return self.parts[0] == 's3:'

    def __str__(self):
        if self.is_s3():
            return f"s3://{super().__str__()[4:]}"
        else:
            return super().__str__()

    def get_s3_bucket(self):
        if self.is_s3():
            return self.parts[1]
        else:
            raise Exception("Not an S3 path")

    def get_s3_prefix(self):
        if self.is_s3():
            return '/'.join(self.parts[2:])
        else:
            raise Exception("Not an S3 path")


def get_table_name_from_path(fpath: FlexPath):
    '''
    Args:
        fpath: Path to the file (e.g. /home/user/data/blah_co.parquet, or s3://duckdb-data/blah_co.parquet)
            - file name must be in the format schemaname_tablename.extension

    Returns:
        schema_name: The schema name (e.g. blah_co)
        table_name: The table name (e.g. 2020-01-01)

    '''
    schema_name = fpath.stem.split('_')[0]
    table_name = fpath.stem[len(schema_name) + 1:]
    return schema_name, table_name


def create_target_duckdb_query(fpath: FlexPath, table=False):
    schema_name, table_name = get_table_name_from_path(fpath)
    return f"create or replace {'table' if table else 'view'} {schema_name}.{table_name} as from read_parquet('{fpath}')"


class DuckDBConnection:
    def __init__(self, filename, s3_storage_used=True, aws_profile='default'):
        self.filename = filename
        self.s3_storage_used = s3_storage_used
        self.aws_profile = aws_profile

    def __enter__(self):
        connection = duckdb.connect(self.filename)
        if self.s3_storage_used:
            connection.query("install httpfs; load httpfs;")
            connection.query("install aws; load aws;")
            connection.query(f"CALL load_aws_credentials('{self.aws_profile}')")
        self.connection = connection
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.connection.close()


def get_duckdb_schemas(con):
    existing_schemas = con.query('select distinct schema_name from information_schema.schemata').fetchall()
    existing_schemas = [x for xs in existing_schemas for x in xs]
    return existing_schemas


def create_duckdb_database_from_local_parquet(db: DuckDBConnection, src_dir_path: FlexPath, create_tables=False):
    raise NotImplementedError("Not implemented yet")


def create_duckdb_database_from_s3_parquet(db_target_file_name: str,
                                           src_dir_path: FlexPath,
                                           create_tables=False,
                                           aws_profile='default'):
    if os.path.exists(db_target_file_name):
        raise Exception(f"File {db_target_file_name} already exists.  Please delete it or choose a different filename.")

    db = DuckDBConnection(filename=db_target_file_name, s3_storage_used=True, aws_profile=aws_profile)
    with db as con:
        s3 = boto3.Session(profile_name=aws_profile).resource('s3')
        bucket = s3.Bucket(src_dir_path.get_s3_bucket())

        for obj in bucket.objects.filter(Prefix=src_dir_path.get_s3_prefix()):
            schema_name, table_name = get_table_name_from_path(FlexPath(obj.key))
            existing_schemas = get_duckdb_schemas(con)
            if schema_name not in existing_schemas:
                con.query(f"CREATE SCHEMA {schema_name};")

            s3_uri = FlexPath(f"s3://{src_dir_path.get_s3_bucket()}/{obj.key}")
            qry = f'''create or replace {'table' if create_tables else 'view'} {schema_name}.{table_name} as from read_parquet('{s3_uri}')'''
            con.query(qry)
