_F='separator'
_E='values'
_D='[]'
_C=True
_B=False
_A=None
import datetime,json
from typing import Any,Callable
from localstack.utils.files import rm_rf
from localstack.utils.json import extract_jsonpath,json_safe
from localstack.utils.numbers import is_number
from localstack.utils.strings import to_bytes,to_str
AGG_COMPARABLE_TYPE=float|datetime.datetime
VARIANT=str
VARIANT_MARKER_PREFIX='=VARIANT::'
def load_data(file_ref,file_format):
	from snowflake_local.files.storage import FILE_STORAGE as D,FileRef as E;F=E.parse(file_ref);A=D.load_file(F);A=json.loads(to_str(A));G=A if isinstance(A,list)else[A];B=[]
	for C in G:
		if isinstance(C,dict):B.append({'_col1':json.dumps(C)})
		else:B.append(C)
	return B
def result_scan(file_path):
	A=file_path
	with open(A)as B:C=json.loads(B.read())
	try:rm_rf(A)
	except Exception:pass
	return C
def object_construct(*A,**E):
	B={}
	for C in range(0,len(A),2):D=A[C+1];B[A[C]]=_unwrap_variant_type(D)
	return to_variant(B)
def get_path(obj,path):
	C=obj;B=path
	if not B.startswith('.'):B=f".{B}"
	if not B.startswith('$'):B=f"${B}"
	if C is not _A and not isinstance(C,(list,dict)):C=_unwrap_variant_type(C,expected_type=(list,dict))
	A=extract_jsonpath(C,B)
	if A==[]:return''
	if is_number(A)and not isinstance(A,bool)and int(A)==A:A=int(A)
	A=json.dumps(A);return A
def to_variant(obj):
	A=obj
	if isinstance(A,str)and A.startswith(VARIANT_MARKER_PREFIX):return A
	try:B=json.dumps(A);return f"{VARIANT_MARKER_PREFIX}{B}"
	except Exception:return str(A)
def parse_json(obj):json.loads(obj);return obj
def to_char(obj,format=_A):
	B=obj
	if isinstance(B,bytes):C=''.join(f"{A:0x}"for A in B);return C.upper()
	if B is _A:return B
	A=str(B)
	if len(A)>=2 and A[0]==A[-1]=='"':return A[1:-1]
	A=to_bytes(A).decode('unicode_escape');return A
def to_boolean(obj):
	A=obj
	if A is _A:return _B
	if A=='true':return _C
	if A=='false':return _B
	return bool(A)
def cancel_all_queries(session):return'canceled'
def arg_min_aggregate(_result,_input1,_input2):
	def A(val1,val2):return val1<val2
	return _arg_min_max_aggregate(_result,_input1,_input2,comparator=A)
def arg_max_aggregate(_result,_input1,_input2):
	def A(val1,val2):return val1>val2
	return _arg_min_max_aggregate(_result,_input1,_input2,comparator=A)
def _arg_min_max_aggregate(_result,_input1,_input2,comparator):
	B=_input2;A=_result
	if B is _A:return A
	C=json.dumps(json_safe(_input1));D=json.dumps(json_safe(B))
	if A[1]is _A:return[C,D]
	E=_unwrap_variant_type(A[1])
	if comparator(B,E):return[C,D]
	return A
def arg_min_max_finalize(_result):
	A=_result
	if isinstance(A[0],str):return _unwrap_variant_type(A[0])
	return A[0]
def array_construct(*A):A=[_unwrap_variant_type(A)for A in A];B=to_variant(A);return B
def array_construct_compact(*A):return array_compact(array_construct(*A))
def array_compact(_array):
	A=_array
	if A is _A:A=_D
	if isinstance(A,VARIANT):A=_unwrap_variant_type(A,expected_type=list)
	B=[A for A in A if A is not _A];B=to_variant(B);return B
def array_distinct(_array):
	B=_array
	if B is _A:return to_variant(_A)
	B=_unwrap_variant_type(B,expected_type=list);A=[]
	for C in B:
		if C not in A:A.append(C)
	A=to_variant(A);return A
def array_agg_aggregate(_result,_input1):
	C=_input1;B=_result
	if C is _A:return B
	A=_unwrap_variant_type(B or _D);A.append(C);A=to_variant(A);return A
def string_agg_aggregate_distinct(_result,_input,separator=_A,distinct=_C):
	D=_result;C=separator;B=_input
	if B is _A:return D
	A=_unwrap_variant_type(D or _D)
	if C:
		if isinstance(A,dict):A=A[_E]
	if not distinct or B not in A:A.append(B)
	if C:A={_F:C,_E:A}
	A=to_variant(A);return A
def string_agg_aggregate(_result,_input,separator=_A):return string_agg_aggregate_distinct(_result,_input,separator=separator,distinct=_B)
def string_agg_aggregate_ordered_finalize(_result,separator=_A,sort=_C):
	B=separator;B=B or'';A=_unwrap_variant_type(_result)
	if sort:A=sorted(A)
	A=B.join([str(A)for A in A]);A=to_variant(A);return A
def string_agg_aggregate_finalize(_result,separator=_A):
	B=separator;A=_result;A=_unwrap_variant_type(A)
	if isinstance(A,dict)and A.get(_F):B=A[_F];A=A[_E]
	A=to_variant(A);return string_agg_aggregate_ordered_finalize(A,separator=B,sort=_B)
def array_append(_array,_item):
	B=_item;A=_array
	if A is _A:A=_D
	A=_unwrap_variant_type(A,expected_type=list)
	if not isinstance(A,list):raise Exception(f"Expected array as first parameter, got: {A}")
	B=_unwrap_variant_type(B);A.append(B);return to_variant(A)
def array_concat(_array1,_array2):
	B=_array2;A=_array1;A=_unwrap_variant_type(A,expected_type=list);B=_unwrap_variant_type(B,expected_type=list)
	if not isinstance(A,list):raise Exception(f"Expected array as first parameter, got: {A}")
	if not isinstance(B,list):raise Exception(f"Expected array as second parameter, got: {B}")
	C=A+B;return to_variant(C)
def array_contains(_value,_array):
	B=_array;A=_value;A=_unwrap_variant_type(A);B=_unwrap_variant_type(B,expected_type=list)
	for C in B:
		if A==C:return _C
	return _B
def to_binary(_obj,_format=_A):A=_format;A=A or'UTF-8';return str(_obj).encode(A)
def _unwrap_variant_type(variant_obj_str,expected_type=_A):
	C=expected_type;B=variant_obj_str;B=B.removeprefix(VARIANT_MARKER_PREFIX);A=json.loads(B)
	if C:
		if not isinstance(A,C)and isinstance(A,str):
			try:
				D=json.loads(A)
				if isinstance(D,C):A=D
			except Exception:pass
	return A