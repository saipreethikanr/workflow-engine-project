"""In-memory storage for graphs and runs"""
import uuid
from typing import Dict, Any, Optional
from app.engine.graph import WorkflowGraph
from app.engine.state import WorkflowState

class MemoryStorage:
    """Simple in-memory storage for graphs and run states"""

    def __init__(self):
        self.graphs: Dict[str, tuple] = {}
        self.runs: Dict[str, Dict[str, Any]] = {}

    def save_graph(self, graph: WorkflowGraph, name: str) -> str:
        """Save a graph and return its ID"""
        graph_id = str(uuid.uuid4())
        self.graphs[graph_id] = (graph, {"name": name})
        return graph_id

    def get_graph(self, graph_id: str) -> Optional[WorkflowGraph]:
        """Retrieve a graph by ID"""
        if graph_id in self.graphs:
            return self.graphs[graph_id][0]
        return None

    def save_run(self, run_id: str, state: WorkflowState, status: str, execution_log: list):
        """Save run state"""
        self.runs[run_id] = {
            "state": state.get_state(),
            "status": status,
            "execution_log": execution_log
        }

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve run data by ID"""
        return self.runs.get(run_id)

    def list_graphs(self) -> Dict[str, str]:
        """List all graphs"""
        return {
            gid: meta["name"] 
            for gid, (_, meta) in self.graphs.items()
        }

storage = MemoryStorage()
