from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class NodeType(str, Enum):
    FUNCTION = "function"
    CONDITIONAL = "conditional"
    LOOP = "loop"

class NodeDefinition(BaseModel):
    name: str
    type: NodeType = NodeType.FUNCTION
    tool: Optional[str] = None
    condition: Optional[str] = None
    max_iterations: Optional[int] = 10

class EdgeDefinition(BaseModel):
    from_node: str
    to_node: str
    condition: Optional[str] = None

class GraphDefinition(BaseModel):
    nodes: List[NodeDefinition]
    edges: List[EdgeDefinition]
    entry_point: str

class GraphCreateRequest(BaseModel):
    graph: GraphDefinition
    name: Optional[str] = "unnamed_graph"

class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any] = Field(default_factory=dict)

class ExecutionLog(BaseModel):
    node: str
    timestamp: float
    state_snapshot: Dict[str, Any]
    output: Optional[Any] = None

class GraphRunResponse(BaseModel):
    run_id: str
    final_state: Dict[str, Any]
    execution_log: List[ExecutionLog]
    status: str
