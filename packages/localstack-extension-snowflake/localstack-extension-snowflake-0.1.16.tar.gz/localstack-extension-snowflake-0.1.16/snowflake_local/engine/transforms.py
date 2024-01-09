_V='TO_VARIANT'
_U='OBJECT_CONSTRUCT'
_T='SELECT NULL'
_S='expression'
_R='javascript'
_Q='FUNCTION'
_P='DATABASE'
_O='quoted'
_N='SCHEMA'
_M='db'
_L='alias'
_K='is_string'
_J='properties'
_I=False
_H='postgres'
_G='TEXT'
_F='TABLE'
_E=None
_D='kind'
_C='expressions'
_B=True
_A='this'
import datetime,json,logging,re,textwrap
from typing import Callable
from aenum import extend_enum
from localstack.utils.collections import ensure_list
from localstack.utils.files import chmod_r,new_tmp_file,save_file
from localstack.utils.strings import short_uid,to_bytes
from localstack.utils.time import timestamp
from sqlglot import TokenType,exp,parse_one,tokens
from sqlglot.dialects import Postgres,Snowflake
from snowflake_local.engine.db_engine import DBEngine,get_db_engine
from snowflake_local.engine.models import Query
from snowflake_local.engine.query_processors import QueryProcessor
from snowflake_local.engine.session import APP_STATE
LOG=logging.getLogger(__name__)
TYPE_MAPPINGS={'VARIANT':_G,'OBJECT':_G,'STRING':_G,'UNKNOWN':_G}
ACCOUNT_ID='TESTACC123'
class QueryTransforms:
	def apply(D,query):
		A=query;B=parse_one(A.query,read='snowflake')
		for E in D.get_transformers():B=B.transform(E,query=A)
		for C in QueryProcessor.get_instances():
			if C.should_apply(A):B=B.transform(C.transform_query,query=A)
		A.query=B.sql(dialect=_H);return A
	def get_transformers(A):return[remove_transient_keyword,remove_if_not_exists,remove_create_or_replace,replace_unknown_types,replace_unknown_user_config_params,replace_create_schema,replace_identifier_function,insert_create_table_placeholder,replace_db_references,replace_current_warehouse,replace_current_account,replace_current_statement,replace_current_time,update_function_language_identifier,convert_function_args_to_lowercase,create_tmp_table_for_result_scan,remove_table_cluster_by,insert_session_id,adjust_casing_of_table_refs]
class QueryTransformsPostgres(QueryTransforms):
	def get_transformers(A):return super().get_transformers()+[pg_replace_describe_table,pg_replace_show_entities,pg_replace_questionmark_placeholder,pg_replace_object_construct,pg_rename_reserved_keyword_functions,pg_return_inserted_items,pg_remove_table_func_wrapper,pg_convert_array_agg_params,pg_convert_array_constructor,pg_convert_array_contains_operators,pg_convert_array_function_arg_types,pg_add_alias_to_subquery,pg_convert_timestamp_types,pg_track_case_sensitive_identifiers,pg_cast_params_for_string_agg,pg_cast_params_for_to_date,pg_get_available_schemas,pg_fix_function_code_escaping]
class QueryTransformsDuckDB(QueryTransforms):
	def get_transformers(A):return super().get_transformers()+[ddb_replace_create_database]
def remove_comments(expression,**B):
	A=expression
	if isinstance(A,exp.Comment):return exp.Literal(this='',is_string=_I)
	if A.comments:A.comments=_E
	return A
def remove_transient_keyword(expression,**E):
	A=expression
	if not _is_create_table_expression(A):return A
	B=A.copy()
	if B.args[_J]:
		C=B.args[_J].expressions;D=exp.TransientProperty()
		if D in C:C.remove(D)
	return B
def remove_if_not_exists(expression,**D):
	C='exists';A=expression
	if not isinstance(A,exp.Create):return A
	B=A.copy()
	if B.args.get(C):B.args[C]=_I
	return B
def remove_create_or_replace(expression,query):
	I='replace';D=query;A=expression
	if not isinstance(A,exp.Create):return A
	E=try_get_db_engine()
	if A.args.get(I):
		B=A.copy();B.args[I]=_I;F=str(B.args.get(_D)).upper()
		if E and F in(_F,_Q):
			G=str(B.this.this);C=Query(query=f"DROP {F} IF EXISTS {G}");C.session=D.session;C.database=D.database;H=G.split('.')
			if len(H)>=3:C.database=H[0]
			E.execute_query(C)
		return B
	return A
def replace_unknown_types(expression,**E):
	B=expression
	for(D,C)in TYPE_MAPPINGS.items():
		C=getattr(exp.DataType.Type,C.upper());A=B
		if isinstance(A,exp.Alias):A=A.this
		if isinstance(A,exp.Cast)and A.to==exp.DataType.build(D):A.args['to']=exp.DataType.build(C)
		if isinstance(B,exp.ColumnDef):
			if B.args.get(_D)==exp.DataType.build(D):B.args[_D]=exp.DataType.build(C)
	return B
def replace_unknown_user_config_params(expression,**E):
	A=expression
	if isinstance(A,exp.Command)and str(A.this).upper()=='ALTER':
		C=str(A.expression).strip();D='\\s*USER\\s+\\w+\\s+SET\\s+\\w+\\s*=\\s*[\'\\"]?(.*?)[\'\\"]?\\s*$';B=re.match(D,C,flags=re.I)
		if B:return parse_one(f"SELECT '{B.group(1)}'")
	return A
def replace_create_schema(expression,query):
	A=expression
	if not isinstance(A,exp.Create):return A
	A=A.copy();B=A.args.get(_D)
	if str(B).upper()==_N:query.database=A.this.db;A.this.args[_M]=_E
	return A
def insert_create_table_placeholder(expression,query):
	A=expression
	if not _is_create_table_expression(A):return A
	if isinstance(A.this.this,exp.Placeholder)or str(A.this.this)=='?':A=A.copy();A.this.args[_A]=query.params.pop(0)
	return A
def replace_identifier_function(expression,**C):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()=='IDENTIFIER'and A.expressions:B=A.expressions[0].copy();B.args[_K]=_I;return B
	return A
def replace_db_references(expression,query):
	E='catalog';C=query;A=expression;D=A.args.get(E)
	if isinstance(A,exp.Table)and A.args.get(_M)and D:C.database=D.this;A.args[E]=_E
	if isinstance(A,exp.UserDefinedFunction):
		B=str(A.this).split('.')
		if len(B)==3:A.this.args[_A]=B[1];C.database=B[0]
	return A
def replace_current_warehouse(expression,query):
	C=query;A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()=='CURRENT_WAREHOUSE':B=exp.Literal();B.args[_A]=C.session and C.session.warehouse or'TEST';B.args[_K]=_B;return B
	return A
def replace_current_account(expression,**D):
	B=expression;C=['CURRENT_ACCOUNT','CURRENT_ACCOUNT_NAME']
	if isinstance(B,exp.Func)and str(B.this).upper()in C:A=exp.Literal();A.args[_A]=ACCOUNT_ID;A.args[_K]=_B;return A
	if isinstance(B,exp.CurrentUser):A=exp.Literal();A.args[_A]='TEST';A.args[_K]=_B;return A
	return B
def replace_current_statement(expression,query):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()=='CURRENT_STATEMENT':B=exp.Literal();B.args[_A]=query.original_query;B.args[_K]=_B;return B
	return A
def replace_current_time(expression,**D):
	A=expression
	if isinstance(A,(exp.CurrentTime,exp.CurrentTimestamp)):
		B=exp.Literal();C=timestamp()
		if isinstance(A,exp.CurrentTime):C=str(datetime.datetime.utcnow().time())
		B.args[_A]=C;B.args[_K]=_B;return B
	return A
def update_function_language_identifier(expression,**Q):
	L='python';A=expression;M={_R:'plv8',L:'plpython3u'}
	if isinstance(A,exp.Create)and isinstance(A.this,exp.UserDefinedFunction):
		E=A.args[_J];C=E.expressions;B=[A for A in C if isinstance(A,exp.LanguageProperty)]
		if not B:F=exp.LanguageProperty();F.args[_A]='SQL';C.append(F);return A
		G=str(B[0].this).lower();N=G==L
		for(O,H)in M.items():
			if G!=O:continue
			if isinstance(B[0].this,exp.Identifier):B[0].this.args[_A]=H
			else:B[0].args[_A]=H
		I=[];J=[A for A in C if str(A.this).lower()=='handler']
		for K in C:
			if isinstance(K,(exp.LanguageProperty,exp.ReturnsProperty)):I.append(K)
		E.args[_C]=I
		if N and J:P=J[0].args['value'].this;D=textwrap.dedent(A.expression.this);D=D+f"\nreturn {P}(*args)";A.expression.args[_A]=D
	return A
def convert_function_args_to_lowercase(expression,**H):
	A=expression
	if isinstance(A,exp.Create)and isinstance(A.this,exp.UserDefinedFunction):
		D=A.args[_J].expressions;B=[A for A in D if isinstance(A,exp.LanguageProperty)];B=str(B[0].this).lower()if B else _E
		if B not in(_R,'plv8'):return A
		E=[A for A in A.this.expressions if isinstance(A,exp.ColumnDef)]
		for F in E:
			if not A.expression:continue
			C=str(F.this);G=A.expression.this;A.expression.args[_A]=G.replace(C.upper(),C.lower())
	return A
def create_tmp_table_for_result_scan(expression,**K):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()=='RESULT_SCAN':
		E=A.expressions[0];F=E.this;B=APP_STATE.queries.get(F)
		if not B:LOG.info("Unable to find state for query ID '%s'",F);return A
		C=new_tmp_file();G=json.dumps(B.result.rows);save_file(C,G);chmod_r(C,511);E.args[_A]=C
		def H(idx,col):B=col;A=B.type_name.upper();A=TYPE_MAPPINGS.get(A)or A;return f"{f'_col{idx+1}'if B.name.lower()=='?column?'else B.name} {A}"
		D=exp.Alias();D.args[_A]=A;I=B.result.columns;J=', '.join([H(A,B)for(A,B)in enumerate(I)]);D.args[_L]=f"({J})";return D
	return A
def remove_table_cluster_by(expression,**F):
	A=expression
	if _is_create_table_expression(A):C=A.args[_J]or[];D=[type(A)for A in C if not isinstance(A,exp.Cluster)];A.args[_J]=D
	elif isinstance(A,exp.Command)and A.this=='ALTER':
		E='(.+)\\s*CLUSTER\\s+BY([\\w\\s,]+)(.*)';B=re.sub(E,'\\1\\3',A.expression,flags=re.I);A.args[_S]=B
		if re.match('\\s*TABLE\\s+\\w+',B,flags=re.I):return parse_one(_T,read=_H)
	return A
def insert_session_id(expression,query):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).lower()=='current_session':return exp.Literal(this=query.session.session_id,is_string=_B)
	return A
def adjust_casing_of_table_refs(expression,query):
	A=expression
	if isinstance(A,exp.From):
		B=A.this
		if isinstance(B,exp.Expression)and B.args.get(_M):
			C=B.args[_M]
			if C.args.get(_O):C.args[_O]=_I
	return A
def pg_replace_describe_table(expression,**G):
	A=expression
	if not isinstance(A,exp.Describe):return A
	C=A.args.get(_D)or _F
	if str(C).upper()==_F:B=A.this.name;D=f"'{B}'"if B else'?';E=f"SELECT * FROM information_schema.columns WHERE table_name={D}";F=parse_one(E,read=_H);return F
	return A
def pg_replace_show_entities(expression,**N):
	G='columns';E='tables';B=expression
	if not isinstance(B,(exp.Command,exp.Show)):return B
	A=''
	if isinstance(B,exp.Command):
		H=str(B.this).upper()
		if H!='SHOW':return B
		A=str(B.args.get(_S)).strip().lower()
	elif isinstance(B,exp.Show):A=str(B.this).strip().lower()
	A=A.removeprefix('terse').strip()
	if A.startswith('primary keys'):I='\n        SELECT a.attname as column_name, format_type(a.atttypid, a.atttypmod) AS data_type, c.relname AS table_name\n        FROM   pg_index i\n        JOIN   pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)\n        JOIN   pg_class as c ON c.oid = i.indrelid\n        WHERE  i.indisprimary;\n        ';return parse_one(I,read=_H)
	if A.startswith('imported keys'):return parse_one(_T,read=_H)
	D=[];J='^\\s*\\S+\\s+(\\S+)\\.(\\S+)(.*)';F=re.match(J,A)
	if F:D.append(f"table_schema = '{F.group(2)}'")
	if A.startswith(E):C=E
	elif A.startswith('schemas'):C='schemata'
	elif A.startswith('objects'):C=E
	elif A.startswith(G):C=G
	elif A.startswith('procedures'):C='routines';D.append("specific_schema <> 'pg_catalog'")
	else:return B
	K=f"WHERE {' AND '.join(A for A in D)}"if D else'';L=f"SELECT * FROM information_schema.{C} {K}";M=parse_one(L,read=_H);return M
def pg_replace_questionmark_placeholder(expression,**B):
	A=expression
	if isinstance(A,exp.Placeholder):return exp.Literal(this='%s',is_string=_I)
	return A
def pg_replace_object_construct(expression,**G):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()==_U:
		class D(exp.Func):_sql_names=[_V];arg_types={_A:_B,_C:_B}
		B=A.args[_C]
		for C in range(1,len(B),2):E=B[C];B[C]=F=D();F.args[_C]=E
	return A
def pg_rename_reserved_keyword_functions(expression,**E):
	A=expression
	if isinstance(A,exp.Func)and isinstance(A.this,str):
		B={'current_role':'get_current_role'}
		for(C,D)in B.items():
			if str(A.this).lower()==C:A.args[_A]=D
	return A
def pg_return_inserted_items(expression,**B):
	A=expression
	if isinstance(A,exp.Insert):A.args['returning']=' RETURNING 1'
	return A
def pg_remove_table_func_wrapper(expression,**B):
	A=expression
	if isinstance(A,exp.Table)and str(A.this.this).upper()==_F:return A.this.expressions[0]
	return A
def pg_convert_array_agg_params(expression,**F):
	E='from';B=expression
	if isinstance(B,exp.Select):
		C=[A for A in B.expressions if isinstance(A,exp.WithinGroup)];A=_E
		if C:
			if isinstance(C[0].this,exp.ArrayAgg):C[0].args[_A]='ARRAY_AGG_ORDERED()';A=B.args.get(E)
		else:
			D=[A for A in B.expressions if isinstance(A,exp.ArrayAgg)]
			if D:
				A=B.args.get(E)
				if isinstance(A.this,exp.Values)and not A.this.args.get(_L):D[0].args[_A]='_tmp_col1'
		if A and isinstance(A.this,exp.Values)and not A.this.args.get(_L):A.this.args[_L]='_tmp_table(_tmp_col1)'
	return B
def pg_convert_array_constructor(expression,**C):
	A=expression
	if isinstance(A,exp.Array):B=exp.Anonymous();B.args[_A]='ARRAY_CONSTRUCT';B.args[_C]=A.expressions;return B
	return A
def pg_convert_array_contains_operators(expression,**C):
	A=expression
	if isinstance(A,exp.ArrayContains):B=exp.Anonymous();B.args[_A]='ARRAY_CONTAINS';B.args[_C]=[A.expression,A.this];return B
	return A
def pg_convert_array_function_arg_types(expression,**J):
	F='array_cat';A=expression
	class D(exp.Func):_sql_names=[_V];arg_types={_A:_B,_C:_B}
	G='array_append',F,'array_construct','array_construct_compact','array_contains'
	if isinstance(A,exp.Func):
		E=str(A.this).lower()
		if isinstance(A,exp.ArrayConcat):E=F
		for H in G:
			if E!=H:continue
			for(I,B)in enumerate(A.expressions):A.expressions[I]=C=D();C.args[_C]=B
			if isinstance(A,exp.ArrayConcat):B=A.this;A.args[_A]=C=D();C.args[_C]=B
	return A
def pg_add_alias_to_subquery(expression,**B):
	A=expression
	if isinstance(A,exp.Subquery):
		if not A.alias and A.parent_select:A.args[_L]=f"_tmp{short_uid()}"
	return A
def pg_convert_timestamp_types(expression,**D):
	A=expression
	if isinstance(A,exp.ColumnDef):
		B=str(A.args.get(_D,'')).upper()
		if B=='TIMESTAMP':A.args[_D]=C=exp.Identifier();C.args[_A]='TIMESTAMP WITHOUT TIME ZONE'
	return A
def pg_track_case_sensitive_identifiers(expression,query):
	B=expression;from snowflake_local.engine.postgres.db_state import State
	if isinstance(B,exp.Create):
		C=str(B.args.get(_D)).upper()
		if C in(_P,_N,_F):
			A=B
			while isinstance(A.this,exp.Expression):A=A.this
			if A.args.get(_O):D=A.this if C==_P else query.database;E=A.this if C==_N else _E;F=A.this if C==_F else _E;G=D,E,F;State.identifier_overrides.entries.append(G)
	return B
def pg_cast_params_for_string_agg(expression,**K):
	E='separator';A=expression
	if not isinstance(A,exp.GroupConcat):return A
	C=''
	def H(expr):
		B=expr;nonlocal C;D=B.this;A=B
		if isinstance(D,exp.Distinct):D=B.this.expressions[0];A=B.this.expressions
		if not isinstance(D,exp.Cast):
			E=exp.Cast();E.args[_A]=D;E.args['to']=exp.DataType.build(_G)
			if isinstance(A,list):
				A[0]=E
				if len(A)>1:F=A.pop(1);C=str(F.this)
			else:A.args[_A]=E
	H(A)
	if A.args.get(E)is _E:A.args[E]=exp.Literal(this=C,is_string=_B)
	if not A.parent_select:return A
	F=isinstance(A.this,exp.Distinct)
	if F:
		G=A.parent_select.find(exp.WithinGroup)
		if G:
			if len(A.this.expressions)!=1:raise Exception(f"Expected a single DISTINCT clause in combination with WITHIN GROUP, got: {A.this.expressions}")
			if isinstance(G.this,exp.GroupConcat):
				B=exp.Anonymous();I='STRING_AGG_ORDERED_DISTINCT'if F else'STRING_AGG_ORDERED';B.args[_A]=I;B.args[_C]=G.this.expressions
				if C:B.args[_C]=[exp.Literal(this=C,is_string=_B)]
				return B
	if not C and A.args.get(E):C=A.args[E].this
	B=exp.Anonymous();B.args[_A]='STRING_AGG_NOGROUP_DISTINCT'if F else'STRING_AGG_NOGROUP';B.args[_C]=ensure_list(A.this)
	if isinstance(B.args[_C][0],exp.Distinct):
		D=B.args[_C][0].expressions
		if isinstance(D,list)and len(D)==1:D=D[0]
		B.args[_C][0]=D
	if C:J=exp.Literal(this=C,is_string=_B);B.args[_C]+=[J]
	return B
def pg_cast_params_for_to_date(expression,**C):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).lower()=='to_date':
		A=A.copy();B=exp.Cast();B.args[_A]=A.expressions[0];B.args['to']=exp.DataType.build(_G);A.expressions[0]=B
		if len(A.expressions)<=1:LOG.info('Auto-detection of date format in TO_DATE(..) not yet supported');A.expressions.append(exp.Literal(this='YYYY/MM/DD',is_string=_B))
	return A
def pg_get_available_schemas(expression,query):
	B=query;A=expression
	if isinstance(A,exp.Func)and str(A.this).lower()=='current_schemas':
		C=try_get_db_engine()
		if C:from snowflake_local.engine.postgres.db_engine_postgres import DEFAULT_DATABASE as D;E=Query(query='SELECT schema_name FROM information_schema.schemata',database=B.database);F=B.database or D;G=C.execute_query(E);H=[f"{F}.{A[0]}".upper()for A in G.rows];return exp.Literal(this=json.dumps(H),is_string=_B)
	return A
def pg_fix_function_code_escaping(expression,**C):
	A=expression
	if isinstance(A,exp.Create)and str(A.args.get(_D)).upper()==_Q and isinstance(A.expression,exp.Literal):B=to_bytes(A.expression.this).decode('unicode_escape');A.expression.args[_A]=B
	return A
def ddb_replace_create_database(expression,**D):
	A=expression
	if isinstance(A,exp.Create)and str(A.args.get(_D)).upper()==_P:assert(C:=A.find(exp.Identifier)),f"No identifier in {A.sql}";B=C.this;return exp.Command(this='ATTACH',expression=exp.Literal(this=f"DATABASE ':memory:' AS {B}",is_string=_B),create_db_name=B)
	return A
def _is_create_table_expression(expression,**C):A=expression;return isinstance(A,exp.Create)and(B:=A.args.get(_D))and isinstance(B,str)and B.upper()==_F
def try_get_db_engine():
	try:return get_db_engine()
	except ImportError:return
def _patch_sqlglot():
	Snowflake.Parser.FUNCTIONS.pop(_U,_E)
	for A in('ANYARRAY','ANYELEMENT'):
		extend_enum(TokenType,A,A);extend_enum(exp.DataType.Type,A,A);D=getattr(exp.DataType.Type,A);B=getattr(exp.DataType.Type,A);tokens.Tokenizer.KEYWORDS[A]=B
		for C in(Postgres,Snowflake):C.Parser.TYPE_TOKENS.add(B);C.Parser.ID_VAR_TOKENS.add(B);C.Parser.FUNC_TOKENS.add(B);C.Generator.TYPE_MAPPING[D]=A;C.Tokenizer.KEYWORDS[A]=B
_patch_sqlglot()