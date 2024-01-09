_E='expression'
_D=None
_C='postgres'
_B='SELECT NULL'
_A='default'
import re
from abc import ABC
from localstack.utils.objects import get_all_subclasses
from sqlglot import exp,parse_one
from snowflake_local.engine.models import Query
from snowflake_local.server.models import QueryResponse
from snowflake_local.utils.strings import parse_comma_separated_variable_assignments
class QueryProcessor(ABC):
	def should_apply(A,query):return True
	def transform_query(A,expression,query):return expression
	def postprocess_result(A,query,result):0
	@classmethod
	def get_instances(D):
		A=[]
		for B in get_all_subclasses(QueryProcessor):C=B();A.append(C)
		return A
class HandleShowParameters(QueryProcessor):
	REGEX=re.compile('^\\s*SHOW\\s+PARAMETERS',flags=re.I);SUPPORTED_PARAMS={'AUTOCOMMIT':{_A:'true'},'TIMEZONE':{_A:'America/Los_Angeles'},'TIMESTAMP_NTZ_OUTPUT_FORMAT':{_A:'YYYY-MM-DD HH24:MI:SS.FF3'},'TIMESTAMP_LTZ_OUTPUT_FORMAT':{},'TIMESTAMP_TZ_OUTPUT_FORMAT':{}}
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(C,expression,**D):
		A=expression
		if isinstance(A,exp.Command)and str(A.this).upper()=='SHOW':
			B=str(A.args.get(_E)).strip().lower()
			if B.startswith('parameters'):return parse_one(_B,read=_C)
		return A
	def postprocess_result(H,query,result):
		D=result;C=query;B='TEXT';I={'key':B,'value':B,_A:B,'level':B,'description':B};D.data.rowtype=[]
		for(J,K)in I.items():D.data.rowtype.append({'name':J,'precision':_D,'scale':_D,'type':K,'nullable':True,'length':_D})
		D.data.rowset=[]
		for(A,L)in H.SUPPORTED_PARAMS.items():
			G=L.get(_A,'');E='';F=G
			if A in C.session.system_state.parameters:F=C.session.system_state.parameters[A];E='SYSTEM'
			if A in C.session.parameters:F=C.session.parameters[A];E='SESSION'
			M=A,F,G,E,'test description ...';D.data.rowset.append(M)
class HandleAlterSession(QueryProcessor):
	REGEX=re.compile('^\\s*ALTER\\s+SESSION\\s+SET\\s+(.+)',flags=re.I)
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(B,expression,query):
		A=expression
		if isinstance(A,exp.Command)and str(A.this).upper()=='ALTER':
			D=str(A.args.get(_E)).strip().lower()
			if D.startswith('session'):
				C=B.REGEX.match(str(A).replace('\n',''))
				if C:B._set_parameters(query,C.group(1))
				return parse_one(_B,read=_C)
		return A
	def _set_parameters(E,query,expression):
		B=parse_comma_separated_variable_assignments(expression)
		for(A,C)in B.items():
			A=A.strip().upper();D=HandleShowParameters.SUPPORTED_PARAMS.get(A)
			if D is _D:return
			query.session.parameters[A]=C
class HandleShowKeys(QueryProcessor):
	REGEX=re.compile('^\\s*SHOW\\s+(IMPORTED\\s+)?KEYS(\\s+.+)?',flags=re.I)
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(B,expression,query):
		A=expression
		if isinstance(A,(exp.Command,exp.Show)):return parse_one(_B,read=_C)
		return A
class HandleShowProcedures(QueryProcessor):
	REGEX=re.compile('^\\s*SHOW\\s+PROCEDURES(\\s+.+)?',flags=re.I)
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(B,expression,query):
		A=expression
		if isinstance(A,(exp.Command,exp.Show)):return parse_one(_B,read=_C)
		return A