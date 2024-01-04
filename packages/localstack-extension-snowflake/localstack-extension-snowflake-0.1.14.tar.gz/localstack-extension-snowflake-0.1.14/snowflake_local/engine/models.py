_A=None
import dataclasses
from sqlglot import exp
@dataclasses.dataclass
class Session:session_id:str;auth_token:str|_A=_A;warehouse:str|_A=_A;schema:str|_A=_A;database:str|_A=_A
@dataclasses.dataclass
class Query:query:str|exp.Expression;query_id:str|_A=_A;original_query:str|exp.Expression|_A=_A;params:list|_A=_A;database:str|_A=_A;session:Session|_A=_A
@dataclasses.dataclass
class TableColumn:name:str;type_name:str;type_size:int=0
@dataclasses.dataclass
class QueryResult:rows:list[tuple]=dataclasses.field(default_factory=list);columns:list[TableColumn]=dataclasses.field(default_factory=list)
@dataclasses.dataclass
class QueryState:query:Query;query_state:str|_A=_A;result:QueryResult|_A=_A