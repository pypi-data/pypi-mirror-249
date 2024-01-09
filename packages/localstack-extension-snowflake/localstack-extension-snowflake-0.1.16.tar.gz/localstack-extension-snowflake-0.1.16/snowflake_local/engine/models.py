_A=None
import dataclasses
from sqlglot import exp
@dataclasses.dataclass
class SystemState:
	_instance=_A;parameters:dict[str,str]=dataclasses.field(default_factory=dict)
	@classmethod
	def get(A):A._instance=A._instance or SystemState();return A._instance
@dataclasses.dataclass
class Session:session_id:str;auth_token:str|_A=_A;warehouse:str|_A=_A;schema:str|_A=_A;database:str|_A=_A;parameters:dict[str,str]=dataclasses.field(default_factory=dict);system_state:SystemState=dataclasses.field(default_factory=SystemState.get)
@dataclasses.dataclass
class Query:
	query:str|exp.Expression;query_id:str|_A=_A;original_query:str|exp.Expression|_A=_A;params:list|_A=_A;database:str|_A=_A;session:Session|_A=_A
	def __post_init__(A,*B,**C):
		if A.query and not A.original_query:A.original_query=A.query
@dataclasses.dataclass
class TableColumn:name:str;type_name:str;type_size:int=0
@dataclasses.dataclass
class QueryResult:rows:list[tuple]=dataclasses.field(default_factory=list);columns:list[TableColumn]=dataclasses.field(default_factory=list)
@dataclasses.dataclass
class QueryState:query:Query;query_state:str|_A=_A;result:QueryResult|_A=_A