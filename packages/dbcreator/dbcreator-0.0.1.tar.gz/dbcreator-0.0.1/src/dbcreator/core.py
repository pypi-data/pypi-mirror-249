def get_schema_table_name(key):
    file_name = key.split('/')[1].split('.')[0]
    schema_name = file_name.split('_')[0]
    table_name = file_name.replace(schema_name + '_', '')
    return schema_name, table_name


def get_s3_path(key, s3_bucket):
    return f"s3://{s3_bucket}/{key}"


def create_object_query(key, s3_bucket, table=False):
    schema_name, table_name = get_schema_table_name(key)
    file_path = get_s3_path(key, s3_bucket)
    return f"create or replace {'table' if table else 'view'} {schema_name}.{table_name} as from read_parquet('{file_path}')"


def run_qry(qry, connection):
    print(qry)
    connection.query(qry)