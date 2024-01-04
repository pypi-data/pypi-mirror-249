_D='TIMESTAMP WITH TIME ZONE'
_C='TIMESTAMP WITHOUT TIME ZONE'
_B='test'
_A='TEXT'
import atexit,json,logging,time
from localstack import config
from localstack.utils.net import get_free_tcp_port,wait_for_port_open
from localstack_ext.services.rds.engine_postgres import get_type_name
from localstack_ext.utils.postgresql import Postgresql
from snowflake_local.engine.db_engine import DBEngine
from snowflake_local.engine.models import Query,QueryResult,TableColumn
from snowflake_local.engine.packages import postgres_plv8_package
from snowflake_local.engine.postgres.db_state import State
from snowflake_local.engine.postprocess import _get_database_from_drop_query
from snowflake_local.engine.transforms import QueryTransformsPostgres
LOG=logging.getLogger(__name__)
PG_VARIANT_TYPE=_A
PG_VARIANT_COMPATIBLE_TYPES='JSONB','FLOAT','BIGINT','BOOLEAN',_A
PG_VARIANT_TYPES_AND_ARRAYS=PG_VARIANT_COMPATIBLE_TYPES+('FLOAT[]','INTEGER[]','BOOLEAN[]','TEXT[]')
BASIC_TYPES=_A,'DECIMAL','INTEGER'
DEFAULT_DATABASE=_B
class DBEnginePostgres(DBEngine):
	def execute_query(G,query):
		A=_execute_query(query)
		if isinstance(A,list):return QueryResult(rows=A)
		if not A._context.columns:return QueryResult()
		B=list(A);B=[tuple(A)for A in B];D=QueryResult(rows=B)
		for C in A._context.columns:E=C['name'].upper();F=TableColumn(name=E,type_name=get_pg_type_name(C['type_oid']),type_size=C['type_size']);D.columns.append(F)
		return D
	def prepare_query(B,query):A=QueryTransformsPostgres();return A.apply(query)
def _execute_query(query):
	A=query;G=_start_postgres();E=bool(_get_database_from_drop_query(A.original_query));C=A.query;B=None
	if A.session:
		if A.session.database:B=A.session.database
		if A.session.schema and A.session.schema!='public'and not E:
			D=A.session.schema
			if'.'in D:B,D=D.split('.')
			C=f"SET search_path TO {D}, public; \n{C}"
	B=A.database or B or DEFAULT_DATABASE
	if E:B=None
	else:
		B=B.lower()
		try:_define_util_functions(B)
		except Exception as H:LOG.warning('Unable to define Postgres util functions: %s',H);raise
	F=A.params or[];LOG.debug('Running query (DB %s): %s - %s',B,C,F);return G.run_query(C,*F,database=B)
def _start_postgres(user=_B,password=_B,database=_B):
	if not State.server:
		A=get_free_tcp_port();State.server=Postgresql(port=A,user=user,password=password,database=database,boot_timeout=30,include_python_venv_libs=True);time.sleep(1)
		try:B=20;wait_for_port_open(A,retries=B,sleep_time=.8)
		except Exception:raise Exception('Unable to start up Postgres process (health check failed after 10 secs)')
		def C():State.server.terminate()
		atexit.register(C)
	return State.server
def _define_util_functions(database):
	B=database
	if B in State.initialized_dbs:return
	State.initialized_dbs.append(B);D=State.server;D.run_query('CREATE EXTENSION IF NOT EXISTS plpython3u',database=B);_install_plv8_extension();D.run_query('CREATE EXTENSION IF NOT EXISTS plv8',database=B);A=[];A.append('\n        CREATE OR REPLACE FUNCTION load_data (\n           file_ref text,\n           file_format text\n        ) RETURNS SETOF RECORD\n        LANGUAGE plpython3u IMMUTABLE AS $$\n            from snowflake_local.engine.extension_functions import load_data\n            return load_data(file_ref, file_format)\n        $$\n    ')
	for E in range(10):F=', '.join([f"k{A} TEXT, v{A} TEXT"for A in range(E)]);G=', '.join([f"k{A}, v{A}"for A in range(E)]);A.append(f"""
            CREATE OR REPLACE FUNCTION object_construct ({F}) RETURNS {PG_VARIANT_TYPE}
            LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import object_construct
                return object_construct({G})
            $$
        """)
	for C in PG_VARIANT_TYPES_AND_ARRAYS:A.append(f"""
            CREATE OR REPLACE FUNCTION to_variant (obj {C}) RETURNS {PG_VARIANT_TYPE}
            LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import to_variant
                return to_variant(obj)
            $$
        """)
	A.append(f"""
        CREATE OR REPLACE FUNCTION get_path (obj {PG_VARIANT_TYPE}, path TEXT) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import get_path
            return get_path(obj, path)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION parse_json (obj TEXT) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import parse_json
            return parse_json(obj)
        $$
    """)
	for C in PG_VARIANT_COMPATIBLE_TYPES+('BYTEA',):A.append(f"""
            CREATE OR REPLACE FUNCTION to_char (obj {C}) RETURNS TEXT
            LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import to_char
                return to_char(obj)
            $$
        """)
	for C in PG_VARIANT_COMPATIBLE_TYPES:A.append(f"""
            CREATE OR REPLACE FUNCTION to_boolean (obj {C}) RETURNS BOOLEAN
            LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import to_boolean
                return to_boolean(obj)
            $$
        """)
	A.append('\n        CREATE OR REPLACE FUNCTION result_scan (results_file TEXT) RETURNS SETOF RECORD\n        LANGUAGE plpython3u IMMUTABLE\n        AS $$\n            from snowflake_local.engine.extension_functions import result_scan\n            return result_scan(results_file)\n        $$\n    ');A.append(f"""
        CREATE OR REPLACE FUNCTION array_append (_array {PG_VARIANT_TYPE}, _entry TEXT) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_append
            return array_append(_array, _entry)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION array_cat (_array1 {PG_VARIANT_TYPE}, _array2 {PG_VARIANT_TYPE}) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_concat
            return array_concat(_array1, _array2)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION array_construct (VARIADIC _values {PG_VARIANT_TYPE}[]) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_construct
            return array_construct(*_values)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION array_compact (_array {PG_VARIANT_TYPE}) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_compact
            return array_compact(_array)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION array_construct_compact (VARIADIC _values {PG_VARIANT_TYPE}[]) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_construct_compact
            return array_construct_compact(*_values)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION array_distinct (_array {PG_VARIANT_TYPE}) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_distinct
            return array_distinct(_array)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION array_contains (_value {PG_VARIANT_TYPE}, _array {PG_VARIANT_TYPE}) RETURNS BOOLEAN
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_contains
            return array_contains(_value, _array)
        $$
    """);A.append('\n        CREATE OR REPLACE FUNCTION to_binary (_obj TEXT) RETURNS BYTEA\n        LANGUAGE plpython3u IMMUTABLE AS $$\n            from snowflake_local.engine.extension_functions import to_binary\n            return to_binary(_obj)\n        $$;\n        CREATE OR REPLACE FUNCTION to_binary (_obj TEXT, _format TEXT) RETURNS BYTEA\n        LANGUAGE plpython3u IMMUTABLE AS $$\n            from snowflake_local.engine.extension_functions import to_binary\n            return to_binary(_obj, _format)\n        $$\n    ');A.append('\n        CREATE OR REPLACE FUNCTION "system$snowpipe_streaming_migrate_channel_offset_token" (\n            tableName TEXT, channelName TEXT, offsetToken TEXT) RETURNS TEXT\n        LANGUAGE plpython3u IMMUTABLE AS $$\n            # TODO: simply returning hardcoded value for now - may need to get adjusted over time\n            return \'{"responseMessage":"Success","responseCode":50}\'\n        $$\n    ');A.append(f'''
        CREATE OR REPLACE FUNCTION "system$cancel_all_queries" (session TEXT) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import cancel_all_queries
            return cancel_all_queries(session)
        $$
    ''');H=';\n'.join(A);D.run_query(H,database=B);_define_hardcoded_return_value_functions(database=B);_define_aggregate_functions(database=B)
def _define_hardcoded_return_value_functions(database):
	E='PUBLIC';C=database;D=State.server;F=['ACCOUNTADMIN','ORGADMIN',E,'SECURITYADMIN','SYSADMIN','USERADMIN'];G={'current_account':'TEST001','current_account_name':'TEST002','current_available_roles':json.dumps(F),'current_client':'test-client','current_ip_address':'127.0.0.1','current_organization_name':'TESTORG','current_region':'TEST_LOCAL','get_current_role':E,'get_current_user':'TEST','current_role_type':'ROLE','current_secondary_roles':json.dumps({'roles':'','value':''}),'current_version':'0.0.0','current_transaction':None}
	for(H,A)in G.items():A=A and f"'{A}'";B=f"\n            CREATE OR REPLACE FUNCTION {H}() RETURNS TEXT LANGUAGE plpython3u IMMUTABLE AS\n            $$ return {A} $$;\n            ";D.run_query(B,database=C)
	B='\n    CREATE OR REPLACE FUNCTION information_schema.CURRENT_TASK_GRAPHS() RETURNS\n    TABLE(\n        ROOT_TASK_NAME TEXT, DATABASE_NAME TEXT, SCHEMA_NAME TEXT, STATE TEXT, SCHEDULED_FROM TEXT,\n        FIRST_ERROR_TASK_NAME TEXT, FIRST_ERROR_CODE NUMERIC, FIRST_ERROR_MESSAGE TEXT,\n        SCHEDULED_TIME TIMESTAMP, QUERY_START_TIME TIMESTAMP, NEXT_SCHEDULED_TIME TIMESTAMP,\n        ROOT_TASK_ID TEXT, GRAPH_VERSION NUMERIC, RUN_ID NUMERIC, ATTEMPT_NUMBER NUMERIC,\n        CONFIG TEXT, GRAPH_RUN_GROUP_ID NUMERIC\n    )\n    LANGUAGE plpython3u IMMUTABLE AS $$ return [] $$;\n    ';D.run_query(B,database=C)
def _define_aggregate_functions(database):
	J='TIMESTAMP';I='NUMERIC';C=database;D=State.server
	for B in('arg_min','arg_max'):
		for(G,F)in enumerate((I,_A,J)):
			E=f"""
            CREATE OR REPLACE FUNCTION {B}_finalize_{G} (
               _result TEXT[]
            ) RETURNS {F}
            LANGUAGE plpython3u IMMUTABLE
            AS $$
                from snowflake_local.engine.extension_functions import arg_min_max_finalize
                return arg_min_max_finalize(_result)
            $$;
            """;D.run_query(E,database=C)
			for H in(I,J):E=f"""
                CREATE OR REPLACE FUNCTION {B}_aggregate (
                   _result TEXT[],
                   _input1 {F},
                   _input2 {H}
                ) RETURNS TEXT[]
                LANGUAGE plpython3u IMMUTABLE
                AS $$
                    from snowflake_local.engine.extension_functions import {B}_aggregate
                    return {B}_aggregate(_result, _input1, _input2)
                $$;
                CREATE AGGREGATE {B}({F}, {H}) (
                    INITCOND = '{{null,null}}',
                    STYPE = TEXT[],
                    SFUNC = {B}_aggregate,
                    FINALFUNC = {B}_finalize_{G}
                );
                """;D.run_query(E,database=C)
	for A in BASIC_TYPES:E=f"""
        CREATE OR REPLACE FUNCTION array_agg_aggregate (_result TEXT, _input1 {A}) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.extension_functions import array_agg_aggregate
            return array_agg_aggregate(_result, _input1)
        $$;
        CREATE AGGREGATE array_agg_ordered(ORDER BY {A}) (
            STYPE = TEXT,
            SFUNC = array_agg_aggregate
        );
        CREATE AGGREGATE array_agg({A}) (
            STYPE = TEXT,
            SFUNC = array_agg_aggregate
        );
        """;D.run_query(E,database=C)
	D.run_query(f"""
    CREATE OR REPLACE FUNCTION string_agg_aggregate_finalize (
       _result {PG_VARIANT_TYPE}, _separator TEXT) RETURNS {PG_VARIANT_TYPE}
    LANGUAGE plpython3u IMMUTABLE AS $$
        from snowflake_local.engine.extension_functions import string_agg_aggregate_finalize
        return string_agg_aggregate_finalize(_result, _separator)
    $$;
    CREATE OR REPLACE FUNCTION string_agg_aggregate_finalize (
       _result {PG_VARIANT_TYPE} ) RETURNS {PG_VARIANT_TYPE}
    LANGUAGE plpython3u IMMUTABLE AS $$
        from snowflake_local.engine.extension_functions import string_agg_aggregate_finalize
        return string_agg_aggregate_finalize(_result)
    $$;
    CREATE OR REPLACE FUNCTION string_agg_aggregate_ordered_finalize (
       _result {PG_VARIANT_TYPE}, _separator TEXT) RETURNS {PG_VARIANT_TYPE}
    LANGUAGE plpython3u IMMUTABLE AS $$
        from snowflake_local.engine.extension_functions import string_agg_aggregate_ordered_finalize
        return string_agg_aggregate_ordered_finalize(_result, _separator)
    $$;
    CREATE OR REPLACE FUNCTION string_agg_aggregate_ordered_finalize (
       _result {PG_VARIANT_TYPE} ) RETURNS {PG_VARIANT_TYPE}
    LANGUAGE plpython3u IMMUTABLE AS $$
        from snowflake_local.engine.extension_functions import string_agg_aggregate_ordered_finalize
        return string_agg_aggregate_ordered_finalize(_result)
    $$;
    """,database=C)
	for A in BASIC_TYPES:D.run_query(f"""
            CREATE OR REPLACE FUNCTION string_agg_aggregate (_result {PG_VARIANT_TYPE}, _input {A})
            RETURNS {PG_VARIANT_TYPE} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import string_agg_aggregate
                return string_agg_aggregate(_result, _input)
            $$;
            CREATE OR REPLACE FUNCTION string_agg_aggregate (_result {PG_VARIANT_TYPE}, _input {A}, _separator TEXT)
            RETURNS {PG_VARIANT_TYPE} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import string_agg_aggregate
                return string_agg_aggregate(_result, _input, _separator)
            $$;
            CREATE OR REPLACE FUNCTION string_agg_aggregate_distinct (_result {PG_VARIANT_TYPE}, _input {A})
            RETURNS {PG_VARIANT_TYPE} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import string_agg_aggregate_distinct
                return string_agg_aggregate_distinct(_result, _input)
            $$;
            CREATE OR REPLACE FUNCTION string_agg_aggregate_distinct (_result {PG_VARIANT_TYPE}, _input {A}, _separator TEXT)
            RETURNS {PG_VARIANT_TYPE} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import string_agg_aggregate_distinct
                return string_agg_aggregate_distinct(_result, _input, _separator)
            $$;
            CREATE AGGREGATE string_agg_ordered(_separator TEXT ORDER BY {A}) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = string_agg_aggregate,
                FINALFUNC = string_agg_aggregate_ordered_finalize
            );
            CREATE AGGREGATE string_agg_ordered(ORDER BY {A}) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = string_agg_aggregate,
                FINALFUNC = string_agg_aggregate_ordered_finalize
            );
            CREATE AGGREGATE string_agg_ordered_distinct(_separator TEXT ORDER BY {A}) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = string_agg_aggregate_distinct,
                FINALFUNC = string_agg_aggregate_ordered_finalize
            );
            CREATE AGGREGATE string_agg_ordered_distinct(ORDER BY {A}) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = string_agg_aggregate_distinct,
                FINALFUNC = string_agg_aggregate_ordered_finalize
            );

            CREATE AGGREGATE string_agg_nogroup(_value {A}) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = string_agg_aggregate,
                FINALFUNC = string_agg_aggregate_finalize
            );
            CREATE AGGREGATE string_agg_nogroup(_value {A}, _separator TEXT) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = string_agg_aggregate,
                FINALFUNC = string_agg_aggregate_finalize
            );
            CREATE AGGREGATE string_agg_nogroup_distinct(_value {A}) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = string_agg_aggregate_distinct,
                FINALFUNC = string_agg_aggregate_finalize
            );
            CREATE AGGREGATE string_agg_nogroup_distinct(_value {A}, _separator TEXT) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = string_agg_aggregate_distinct,
                FINALFUNC = string_agg_aggregate_finalize
            );""",database=C)
def _install_plv8_extension():
	if config.is_in_docker:postgres_plv8_package.install()
def get_pg_type_name(scalar_type):
	C='VARCHAR';A=scalar_type;D={'19':C,'25':C,'1114':_C,'1184':_D};B=D.get(str(A))
	if B:return B
	return get_type_name(A)
def convert_pg_to_snowflake_type(pg_type):
	A=pg_type;A=str(A).upper()
	if A==_C:return'TIMESTAMP_NTZ'
	if A==_D:return'TIMESTAMP_TZ'
	return A