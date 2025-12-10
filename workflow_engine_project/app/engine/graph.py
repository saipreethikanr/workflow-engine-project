from typing import Dict, List, Optional
import time
from app.engine.node import Node
from app.engine.state import WorkflowState
from app.models import ExecutionLog

class WorkflowGraph:
    """Core workflow engine that manages graph execution"""

    def __init__(self, entry_point: str):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, List[tuple]] = {}
        self.entry_point = entry_point
        self.execution_log: List[ExecutionLog] = []

    def add_node(self, node: Node):
        """Add a node to the graph"""
        self.nodes[node.name] = node

    def add_edge(self, from_node: str, to_node: str, condition: Optional[str] = None):
        """Add an edge between nodes"""
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append((to_node, condition))

    async def run(self, initial_state: Dict) -> tuple:
        """Execute the workflow from entry point to completion"""
        state = WorkflowState(initial_state)
        self.execution_log = []

        current_node_name = self.entry_point
        max_steps = 100
        steps = 0

        while current_node_name and steps < max_steps:
            steps += 1

            if current_node_name not in self.nodes:
                break

            node = self.nodes[current_node_name]
            result = await node.execute(state)
            state.update(result)

            log_entry = ExecutionLog(
                node=current_node_name,
                timestamp=time.time(),
                state_snapshot=state.get_state(),
                output=result
            )
            self.execution_log.append(log_entry)

            next_node = self._get_next_node(current_node_name, state)

            if next_node == current_node_name:
                if not result.get("should_loop", True):
                    next_node = self._get_alternate_next_node(current_node_name, state)

            current_node_name = next_node

        return state, self.execution_log

    def _get_next_node(self, current: str, state: WorkflowState) -> Optional[str]:
        """Determine the next node based on edges and conditions"""
        if current not in self.edges:
            return None

        for next_node, condition in self.edges[current]:
            if condition is None:
                return next_node

            try:
                safe_dict = {"state": state.get_state()}
                if eval(condition, {"__builtins__": {}}, safe_dict):
                    return next_node
            except Exception as e:
                print(f"Edge condition error: {e}")
                continue

        if self.edges[current]:
            return self.edges[current][0][0]

        return None

    def _get_alternate_next_node(self, current: str, state: WorkflowState) -> Optional[str]:
        """Find next node when loop exits"""
        if current not in self.edges:
            return None

        for next_node, condition in self.edges[current]:
            if next_node != current:
                if condition is None:
                    return next_node
                try:
                    safe_dict = {"state": state.get_state()}
                    if eval(condition, {"__builtins__": {}}, safe_dict):
                        return next_node
                except:
                    continue

        return None
