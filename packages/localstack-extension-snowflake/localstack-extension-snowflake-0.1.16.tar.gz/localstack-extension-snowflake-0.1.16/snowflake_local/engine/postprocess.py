_T='already exists'
_S='status'
_R='VARCHAR'
_Q='COLUMN_DEFAULT'
_P='DATA_TYPE'
_O='COLUMN_NAME'
_N='FUNCTION'
_M='default'
_L='TABLE'
_K='length'
_J='nullable'
_I='scale'
_H='precision'
_G='integer'
_F=True
_E='kind'
_D=None
_C='type'
_B='name'
_A='text'
import calendar,datetime,json,re
from abc import ABC,abstractmethod
from localstack.utils.objects import get_all_subclasses
from sqlglot import exp,parse_one
from snowflake_local.engine.extension_functions import VARIANT_MARKER_PREFIX,_unwrap_variant_type
from snowflake_local.engine.models import Query
from snowflake_local.engine.postgres.db_state import State
from snowflake_local.engine.query_processors import QueryProcessor
from snowflake_local.server.conversions import to_pyarrow_table_bytes_b64
from snowflake_local.server.models import QueryResponse
class QueryResultPostprocessor(ABC):
	def should_apply(A,query,result):return _F
	@abstractmethod
	def apply(self,query,result):0
class FixShowEntitiesResult(QueryResultPostprocessor):
	def should_apply(A,query,result):B=query;return A._is_show_tables(B)or A._is_show_schemas(B)or A._is_show_objects(B)or A._is_show_columns(B)or A._is_show_primary_keys(B)or A._is_show_procedures(B)or A._is_show_imported_keys(B)
	def _is_show_tables(B,query):A=query.original_query;return bool(re.match('^\\s*SHOW\\s+.*TABLES',A,flags=re.I)or re.search('\\s+FROM\\s+information_schema\\s*\\.\\s*tables\\s+',A,flags=re.I))
	def _is_show_schemas(B,query):A=query.original_query;return bool(re.match('^\\s*SHOW\\s+.*SCHEMAS',A,flags=re.I)or re.search('\\s+FROM\\s+information_schema\\s*\\.\\s*schemata\\s+',A,flags=re.I))
	def _is_show_objects(A,query):return bool(re.match('^\\s*SHOW\\s+.*OBJECTS',query.original_query,flags=re.I))
	def _is_show_columns(B,query):A=query.original_query;return bool(re.match('^\\s*SHOW\\s+.*COLUMNS',A,flags=re.I)or re.search('\\s+FROM\\s+information_schema\\s*\\.\\s*columns\\s+',A,flags=re.I))
	def _is_show_primary_keys(A,query):return bool(re.match('^\\s*SHOW\\s+.*PRIMARY\\s+KEYS',query.original_query,flags=re.I))
	def _is_show_imported_keys(A,query):return bool(re.match('^\\s*SHOW\\s+IMPORTED\\s+KEYS',query.original_query,flags=re.I))
	def _is_show_procedures(A,query):return bool(re.match('^\\s*SHOW\\s+PROCEDURES',query.original_query,flags=re.I))
	def apply(I,query,result):
		m='rely';l='key_sequence';k='options';j='catalog_name';i='TABLE_NAME';X='bytes';W='rows';V='cluster_by';S='budget';R='owner_role_type';Q='retention_time';P='owner';O='column_name';N='table_name';L='data_type';J='comment';H='created_on';G='timestamp_ltz';F=query;D='database_name';C='schema_name';B=result;from snowflake_local.engine.postgres.db_engine_postgres import State,convert_pg_to_snowflake_type as n;Y=I._is_show_objects(F);Z=I._is_show_tables(F);o=I._is_show_schemas(F);p=I._is_show_columns(F);q=I._is_show_procedures(F);r=I._is_show_primary_keys(F);s=I._is_show_imported_keys(F);t=re.match('.+\\sTERSE\\s',F.original_query,flags=re.I);_replace_dict_value(B.data.rowtype,_B,'TABLE_SCHEMA',C);_replace_dict_value(B.data.rowtype,_B,'SCHEMA_NAME',_B)
		if Z or Y:_replace_dict_value(B.data.rowtype,_B,i,_B)
		else:_replace_dict_value(B.data.rowtype,_B,i,N)
		_replace_dict_value(B.data.rowtype,_B,_O,O);_replace_dict_value(B.data.rowtype,_B,'TABLE_TYPE',_E);_replace_dict_value(B.data.rowtype,_B,'TABLE_CATALOG',D);_replace_dict_value(B.data.rowtype,_B,'CATALOG_NAME',D);_replace_dict_value(B.data.rowtype,_B,_P,L);_replace_dict_value(B.data.rowtype,_B,_Q,_M);_replace_dict_value(B.data.rowtype,_B,'SPECIFIC_CATALOG',j);_replace_dict_value(B.data.rowtype,_B,'SPECIFIC_SCHEMA',C);_replace_dict_value(B.data.rowtype,_B,'SPECIFIC_NAME',_B);M=[];K=[A[_B]for A in B.data.rowtype]
		for T in B.data.rowset:A=dict(zip(K,T));M.append(A)
		def u(_name,_type):A=_type;return{_B:_name,_H:_D,_I:3 if A==G else _D,_C:A,_J:_F,_K:_D}
		v={H:G,_B:_A,_E:_A,D:_A,C:_A};w={H:G,_B:_A,D:_A,C:_A,_E:_A,J:_A,V:_A,W:_G,X:_G,P:_A,Q:_A,R:_A,S:_A};x={H:G,_B:_A,D:_A,C:_A,_E:_A,J:_A,V:_A,W:_G,X:_G,P:_A,Q:_A,'automatic_clustering':_A,'change_tracking':_A,'is_external':_A,'enable_schema_evolution':_A,R:_A,'is_event':_A,S:_A};y={H:G,_B:_A,'is_default':_A,'is_current':_A,D:_A,P:_A,J:_A,k:_A,Q:_A,R:_A,S:_A};z={N:_A,C:_A,O:_A,L:_A,'null?':_A,_M:_A,_E:_A,'expression':_A,J:_A,D:_A,'autoincrement':_A};A0={H:G,D:_A,C:_A,N:_A,O:_A,l:_A,'constraint_name':_A,m:_A,J:_A};A1={H:G,'pk_database_name':_A,'pk_schema_name':_A,'pk_table_name':_A,'pk_column_name':_A,'fk_database_name':_A,'fk_schema_name':_A,'fk_table_name':_A,'fk_column_name':_A,l:_A,'update_rule':_A,'delete_rule':_A,'fk_name':_A,'pk_name':_A,'deferrability':_A,m:_A,J:_A};A2={H:G,_B:_A,C:_A,'is_builtin':_A,'is_aggregate':_A,'is_ansi':_A,'min_num_arguments':_G,'max_num_arguments':_G,'arguments':_A,'description':_A,j:_A,'is_table_function':_A,'valid_for_clustering':_A,'is_secure':_A};E=_D
		if r:E=A0
		elif t:E=v
		elif o:E=y
		elif Y:E=w
		elif Z:E=x
		elif p:E=z
		elif q:E=A2
		elif s:E=A1
		del B.data.rowtype[:];K=[A[_B]for A in B.data.rowtype]
		for(a,A3)in E.items():
			if a in K:continue
			B.data.rowtype.append(u(a,A3))
		for A in M:
			A.setdefault(V,'');A.setdefault(W,0);A.setdefault(X,0);A.setdefault(k,'')
			if A.get(_M)is _D:A[_M]=''
			if A.get(L):A4=n(A[L]);A[L]=json.dumps({_C:A4})
			A.setdefault(J,'');A.setdefault(P,'PUBLIC');A.setdefault(Q,'1');A.setdefault(R,'ROLE');A.setdefault(S,_D)
			if A.get(_E)=='BASE TABLE':A[_E]=_L
			A.setdefault(H,'0')
		for A in M:
			for U in(_B,C,D,N,O):
				if A.get(U):A[U]=A[U].upper()
			b=A.get(D);c=A.get(C);d=A.get(_B)
			if any((b,c,d)):
				e=State.identifier_overrides.find_match(b,schema=c,obj_name=d)
				if e:
					f,g,h=e
					if h:A[_B]=h
					elif g:A[C]=g
					elif f:A[D]=f
		K=[A[_B]for A in B.data.rowtype];B.data.rowset=[]
		for A in M:T=[A.get(B)for B in K];B.data.rowset.append(T)
class ConvertDescribeTableResultColumns(QueryResultPostprocessor):
	DESCRIBE_TABLE_COL_ATTRS={_B:_O,_C:_P,_E:"'COLUMN'",'null?':'IS_NULLABLE',_M:_Q}
	def should_apply(D,query,result):A=query.original_query;B=re.match('^DESC(RIBE)?\\s+(TABLE\\s+)?.+',A,flags=re.I);C=re.match('\\s+information_schema\\s*\\.\\s*columns\\s+',A,flags=re.I);return bool(B or C)
	def apply(E,query,result):
		A=result;G=[A[_B]for A in A.data.rowtype];F=list(E.DESCRIBE_TABLE_COL_ATTRS);A.data.rowtype=[]
		for H in F:A.data.rowtype.append({_B:H,_H:_D,_I:_D,_C:_R,_J:_F,_K:_D})
		for(I,J)in enumerate(A.data.rowset):
			C=[]
			for K in F:
				D=E.DESCRIBE_TABLE_COL_ATTRS[K]
				if D.startswith("'"):C.append(D.strip("'"))
				else:L=dict(zip(G,J));B=L[D];B={'YES':'Y','NO':'N'}.get(B)or B;C.append(B)
			A.data.rowset[I]=C
class FixCreateEntityResult(QueryResultPostprocessor):
	def should_apply(A,query,result):B=A._get_created_entity_type(query.original_query);return B in(_L,_N)
	def apply(E,query,result):
		D=result;B=query;C=E._get_created_entity_type(B.original_query);F={_L:'Table',_N:'Function'};G=F.get(C)
		if C==_L:A=_get_table_from_creation_query(B.original_query);A=A and A.upper()
		elif C==_N:H=_parse_snowflake_query(B.original_query);I=H.this;A=str(I.this).upper()
		else:A='test'
		D.data.rowset.append([f"{G} {A} successfully created."]);D.data.rowtype.append({_B:_S,_C:_A,_K:-1,_H:0,_I:0,_J:_F})
	def _get_created_entity_type(B,query):
		A=_parse_snowflake_query(query)
		if isinstance(A,exp.Create):return A.args.get(_E)
class FixDropTableResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(_get_table_from_drop_query(query.original_query))
	def apply(C,query,result):A=result;B=_get_table_from_drop_query(query.original_query);A.data.rowset.append([f"{B} successfully dropped."]);A.data.rowtype.append({_B:_S,_C:_A,_K:-1,_H:0,_I:0,_J:_F})
class HandleDropDatabase(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(_get_database_from_drop_query(query.original_query))
	def apply(C,query,result):A=query;B=_get_database_from_drop_query(A.original_query);State.initialized_dbs=[A for A in State.initialized_dbs if A.lower()!=B.lower()];A.session.database=_D;A.session.schema=_D
class FixAlreadyExistsErrorResponse(QueryResultPostprocessor):
	def should_apply(B,query,result):A=result;return not A.success and _T in(A.message or'')
	def apply(C,query,result):
		A=result
		def B(match):return f"SQL compilation error:\nObject '{match.group(1).upper()}' already exists."
		A.message=re.sub('.*database \\"(\\S+)\\".+',B,A.message);A.message=re.sub('.*relation \\"(\\S+)\\".+',B,A.message);A.message=re.sub('.*function \\"(\\S+)\\".+',B,A.message)
class FixInsertQueryResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(re.match('^\\s*INSERT\\s+.+',query.original_query,flags=re.I))
	def apply(B,query,result):A=result;A.data.rowset=[[len(A.data.rowset)]];A.data.rowtype=[{_B:'count',_C:_G,_K:-1,_H:0,_I:0,_J:_F}]
class UpdateSessionAfterCreatingDatabase(QueryResultPostprocessor):
	REGEX=re.compile('^\\s*CREATE.*\\s+DATABASE(\\s+IF\\s+NOT\\s+EXISTS)?\\s+(\\S+)',flags=re.I)
	def should_apply(A,query,result):return bool(A.REGEX.match(query.original_query))
	def apply(B,query,result):A=query;C=B.REGEX.match(A.original_query);A.session.database=C.group(2);A.session.schema=_D
class UpdateSessionAfterCreatingSchema(QueryResultPostprocessor):
	REGEX=re.compile('^\\s*CREATE.*\\s+SCHEMA(\\s+IF\\s+NOT\\s+EXISTS)?\\s+(\\S+)',flags=re.I)
	def should_apply(A,query,result):return bool(A.REGEX.match(query.original_query))
	def apply(B,query,result):A=query;C=B.REGEX.match(A.original_query);A.session.schema=C.group(2)
class AdjustQueryResultFormat(QueryResultPostprocessor):
	def apply(C,query,result):
		A=result;B=re.match('.+FROM\\s+@',query.original_query,flags=re.I);A.data.queryResultFormat='arrow'if B else'json'
		if B:A.data.rowsetBase64=to_pyarrow_table_bytes_b64(A);A.data.rowset=[];A.data.rowtype=[]
class AdjustColumnTypes(QueryResultPostprocessor):
	TYPE_MAPPINGS={'UNKNOWN':'TEXT',_R:'TEXT'}
	def apply(C,query,result):
		for A in result.data.rowtype:
			D=A.get(_C,'');B=C.TYPE_MAPPINGS.get(D)
			if B:A[_C]=B
class FixBooleanResultValues(QueryResultPostprocessor):
	def apply(F,query,result):
		A=result
		for(B,D)in enumerate(A.data.rowtype):
			E=D.get(_C,'')
			if E.upper()not in('BOOL','BOOLEAN'):continue
			for C in A.data.rowset:C[B]='TRUE'if str(C[B]).lower()=='true'else'FALSE'
class ReturnDescribeTableError(QueryResultPostprocessor):
	def apply(C,query,result):
		A=result;B=re.match('desc(?:ribe)?\\s+.+',query.original_query,flags=re.I)
		if B and not A.data.rowset:A.success=False
class IgnoreErrorForExistingEntity(QueryResultPostprocessor):
	REGEX=re.compile('^\\s*CREATE.*\\s+(\\S+)(\\s+IF\\s+NOT\\s+EXISTS)\\s+(\\S+)',flags=re.I)
	def should_apply(A,query,result):return bool(A.REGEX.match(query.original_query))
	def apply(B,query,result):
		A=result
		if not A.success and _T in(A.message or''):A.success=_F;A.data.rowtype=[];A.data.rowset=[]
class AddDefaultResultIfEmpty(QueryResultPostprocessor):
	def should_apply(B,query,result):
		A=_parse_snowflake_query(query.original_query)
		if isinstance(A,exp.AlterTable):return _F
		return isinstance(A,exp.Command)and str(A.this).upper()=='ALTER'
	def apply(B,query,result):
		A=result
		if not A.data.rowtype:A.data.rowtype=[{_B:'?column?',_C:_A,_K:-1,_H:0,_I:0,_J:_F}]
		A.data.rowset=[('Statement executed successfully.',)]
class EncodeComplexTypesInResults(QueryResultPostprocessor):
	def apply(D,query,result):
		for A in result.data.rowset:
			for(C,B)in enumerate(A):
				if isinstance(B,(dict,list)):A[C]=json.dumps(B)
class ConvertTimestampResults(QueryResultPostprocessor):
	def apply(L,query,result):
		D=result
		for(E,C)in enumerate(D.data.rowtype):
			B=str(C.get(_C)).upper();F='TIMESTAMP','TIMESTAMP WITHOUT TIME ZONE';G='TIMESTAMP WITH TIME ZONE',;H='DATE',
			if B in F:C[_C]='TIMESTAMP_NTZ'
			if B in G:C[_C]='TIMESTAMP_TZ'
			I=B in H
			if B not in F+G+H:continue
			for J in D.data.rowset:
				A=J[E]
				if I:K=calendar.timegm(A.timetuple());A=datetime.datetime.utcfromtimestamp(K)
				if isinstance(A,datetime.datetime):A=A.replace(tzinfo=datetime.timezone.utc)
				if A is _D:continue
				A=int(A.timestamp())
				if I:A=A/24/60/60
				J[E]=str(int(A))
class UnwrapVariantTypes(QueryResultPostprocessor):
	def apply(E,query,result):
		A=result
		for C in A.data.rowset:
			for(D,B)in enumerate(C):
				if isinstance(B,str)and B.startswith(VARIANT_MARKER_PREFIX):
					A=_unwrap_variant_type(B)
					if isinstance(A,(list,dict)):A=B.removeprefix(VARIANT_MARKER_PREFIX)
					C[D]=A
def apply_post_processors(query,result):
	C=result;B=query
	for D in get_all_subclasses(QueryResultPostprocessor):
		A=D()
		if A.should_apply(B,result=C):A.apply(B,result=C)
	for A in QueryProcessor.get_instances():
		if A.should_apply(B):A.postprocess_result(B,result=C)
def _replace_dict_value(values,attr_key,attr_value,attr_value_replace):
	A=attr_key;B=[B for B in values if B[A]==attr_value]
	if B:B[0][A]=attr_value_replace
def _get_table_from_creation_query(query):
	A=_parse_snowflake_query(query)
	if not isinstance(A,exp.Create)or A.args.get(_E)!=_L:return
	B=A.this;C=B.this;D=C.this;E=getattr(D,'this',_D);return E
def _get_table_from_drop_query(query):
	A=_parse_snowflake_query(query)
	if not isinstance(A,exp.Drop)or A.args.get(_E)!=_L:return
	B=A.this;C=B.this;D=C.this;return D
def _get_database_from_drop_query(query):
	A=_parse_snowflake_query(query)
	if not isinstance(A,exp.Drop)or A.args.get(_E)!='DATABASE':return
	B=A.this;C=B.this;D=C.this;return D
def _parse_snowflake_query(query):
	try:return parse_one(query,read='snowflake')
	except Exception:return