from dbcreator.duck_db import get_table_name_from_path, \
    create_target_duckdb_query, \
    FlexPath, \
    get_duckdb_schemas, \
    create_duckdb_database_from_s3_parquet
import duckdb
import os


class Test_get_table_name_from_path:
    def test_one(self):
        inp = FlexPath("curated/s1chema_table1.csv")
        assert get_table_name_from_path(inp) == ('s1chema', 'table1')

    def test_two(self):
        inp = FlexPath("curated/s1chema_table1_blah.parquet")
        assert get_table_name_from_path(inp) == ('s1chema', 'table1_blah')

    def test_three(self):
        inp = FlexPath("s3://bucket/curated/s1chema_table2_blah.parquet")
        assert get_table_name_from_path(inp) == ('s1chema', 'table2_blah')


class Test_create_target_duckdb_query:
    def test_one(self):
        inp = FlexPath("curated/s1chema_table1.csv")
        res = "create or replace view s1chema.table1 as from read_parquet('curated/s1chema_table1.csv')"
        assert create_target_duckdb_query(inp) == res
        assert create_target_duckdb_query(inp, True) == res.replace('view', 'table')

    def test_two(self):
        inp = FlexPath("curated/s1chema_table1_blah.parquet")
        res = "create or replace view s1chema.table1_blah as from read_parquet('curated/s1chema_table1_blah.parquet')"
        assert create_target_duckdb_query(inp) == res
        assert create_target_duckdb_query(inp, True) == res.replace('view', 'table')

    def test_three(self):
        inp = FlexPath("s3://bucket/curated/s1chema_table2_blah.parquet")
        res = "create or replace view s1chema.table2_blah as from read_parquet('s3://bucket/curated/s1chema_table2_blah.parquet')"
        assert create_target_duckdb_query(inp) == res
        assert create_target_duckdb_query(inp, True) == res.replace('view', 'table')


def test_get_duckdb_schemas():
    db = duckdb.connect(":memory:")
    assert sorted(get_duckdb_schemas(db)) == ['information_schema', 'main', 'pg_catalog']


class Test_create_duckdb_database_from_s3_parquet:
    aws_profile = 'codenym'

    def clear(self, db_fpath):
        if os.path.exists(db_fpath):
            os.remove(db_fpath)

    def test_one(self):
        db_fpath = 'duckdb1.db'
        self.clear(db_fpath)
        create_duckdb_database_from_s3_parquet(db_fpath,
                                               FlexPath('s3://codenym-automated-testing/dbcreator/parquet/'),
                                               create_tables=False,
                                               aws_profile=self.aws_profile)

        db = duckdb.connect("duckdb1.db")
        schemas = sorted(get_duckdb_schemas(db))
        tables = sorted(tuple((o[1], o[2]) for o in db.query('show all tables')))
        db.close()
        assert schemas == ['information_schema', 'main', 'pg_catalog', 'schema1', 'schema2']
        assert tables == [('schema1', 'table1'), ('schema2', 'table2')]
        self.clear(db_fpath)
