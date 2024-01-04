import base64,logging,re,uuid
from typing import Any
from localstack.utils.strings import to_bytes,to_str,truncate
from pg8000.dbapi import ProgrammingError
from sqlglot import parse_one
from snowflake_local import config
from snowflake_local.engine.db_engine import get_db_engine
from snowflake_local.engine.models import Query,QueryResult,QueryState,Session
from snowflake_local.engine.postprocess import apply_post_processors
from snowflake_local.engine.session import APP_STATE,handle_use_query
from snowflake_local.engine.transforms import remove_comments
from snowflake_local.files.file_ops import handle_copy_into_query,handle_put_file_query
from snowflake_local.server.models import QueryResponse,QueryResponseData
LOG=logging.getLogger(__name__)
REGEX_FILE_FORMAT='\\s*(CREATE|DROP)\\s+.*FILE\\s+FORMAT\\s+(?:IF\\s+NOT\\s+EXISTS\\s+)?(.+)(\\s+TYPE\\s+=(.+))?'
def cleanup_query(query):
	C='/\\*.*?\\*/';B='snowflake';A=query.strip(' ;')
	try:D=parse_one(A,read=B);E=D.transform(remove_comments);A=str(E.sql(dialect=B));A=re.sub(C,'',A,flags=re.I)
	except Exception:A=re.sub(C,'',A,flags=re.I);A=re.sub('^\\s*--.*','',A,flags=re.M)
	return A
def execute_query(query):A=query;B=get_db_engine();A=prepare_query(A);C=B.execute_query(A);return C
def prepare_query(query_obj):A=query_obj;A.original_query=A.query;A.query=_create_tmp_table_for_file_queries(A.query);B=get_db_engine();A=B.prepare_query(A);return A
def insert_rows_into_table(table,rows,schema=None,database=None):
	I=database;H=schema;G=table;F=', ';A=rows;J=f'"{H}"."{G}"'if H else G
	if A and isinstance(A[0],dict):
		B=set()
		for C in A:B.update(C.keys())
		B=list(B);K=F.join(B);E=F.join(['?'for A in B]);L=f"INSERT INTO {J} ({K}) VALUES ({E})"
		for C in A:M=[C.get(A)for A in B];D=Query(query=L,params=list(M),database=I);execute_query(D)
	elif A and isinstance(A[0],(list,tuple)):
		for C in A:N=len(C);E=F.join(['?'for A in range(N)]);D=f"INSERT INTO {J} VALUES ({E})";D=Query(query=D,params=list(C),database=I);execute_query(D)
	elif A:raise Exception(f"Unexpected values when storing list of rows to table: {truncate(str(A))}")
def handle_query_request(query,params,session):
	N='type';M='002002';L=False;K='name';E=session;B=query;A=QueryResponse();A.data.parameters.append({K:'TIMEZONE','value':'UTC'});B=cleanup_query(B);I=A.data.queryId=str(uuid.uuid4());F=Query(query=B,params=params,session=E);APP_STATE.queries[I]=O=QueryState(query=F,query_state='RUNNING');P=re.match('^\\s*PUT\\s+.+',B,flags=re.I)
	if P:return handle_put_file_query(B,A)
	Q=re.match('^\\s*COPY\\s+INTO\\s.+',B,flags=re.I)
	if Q:return handle_copy_into_query(B,A)
	R=re.match('^\\s*USE\\s.+',B,flags=re.I)
	if R:return handle_use_query(B,A,E)
	if(S:=re.match('^\\s*CREATE.*\\s+WAREHOUSE(\\s+IF\\s+NOT\\s+EXISTS)?\\s+(\\S+)',B,flags=re.I)):E.warehouse=S.group(2);return A
	if re.match('^\\s*DROP.*\\s+WAREHOUSE',B,flags=re.I):E.warehouse=None;return A
	T=re.match('^\\s*CREATE\\s+STORAGE\\s.+',B,flags=re.I)
	if T:return A
	U=re.match(REGEX_FILE_FORMAT,B,flags=re.I)
	if U:return A
	try:C=execute_query(F)
	except Exception as D:
		V=LOG.exception if config.TRACE_LOG else LOG.warning;V('Error executing query: %s',D);C=QueryResult();A.success=L;A.message=str(D)
		if isinstance(D,ProgrammingError)and D.args:A.code=M;A.data=QueryResponseData(**{'internalError':L,'errorCode':M,'age':0,'sqlState':'42710','queryId':I,'line':-1,'pos':-1,N:'COMPILATION'});A.message=D.args[0].get('M')or str(D)
	O.result=C
	if C and C.columns:
		G=[];W=C.columns
		for X in C.rows:G.append(list(X))
		J=[]
		for H in W:J.append({K:H.name,N:H.type_name,'length':H.type_size,'precision':0,'scale':0,'nullable':True})
		A.data.rowset=G;A.data.rowtype=J;A.data.total=len(G)
	apply_post_processors(F,A);return A
def _create_tmp_table_for_file_queries(query):
	A=query;C='(\\s*SELECT\\s+.+\\sFROM\\s+)(@[^\\(\\s]+)(\\s*\\([^\\)]+\\))?';F=re.match(C,A)
	if not F:return A
	G=re.findall('\\$\\d+',A);D='_col1 TEXT';B=[int(A.removeprefix('$'))for A in G]
	if B:H=list(range(1,max(B)+1));D=','.join([f"_col{A} TEXT"for A in H])
	def I(match):A=match;B=to_str(base64.b64encode(to_bytes(A.group(3)or'')));return f"{A.group(1)} load_data('{A.group(2)}', '{B}') as _tmp({D})"
	A=re.sub(C,I,A)
	if B:
		for E in range(max(B),0,-1):A=A.replace(f"${E}",f"_col{E}")
	return A