from typing import Callable, Dict, Any, Optional
from app.models import NodeType
from app.engine.state import WorkflowState

class Node:
    """Represents a node in the workflow graph"""

    def __init__(
        self,
        name: str,
        node_type: NodeType,
        tool: Optional[Callable] = None,
        condition: Optional[str] = None,
        max_iterations: int = 10
    ):
        self.name = name
        self.node_type = node_type
        self.tool = tool
        self.condition = condition
        self.max_iterations = max_iterations
        self.iterations = 0

    async def execute(self, state: WorkflowState) -> Dict[str, Any]:
        """Execute the node and return results"""
        if self.node_type == NodeType.FUNCTION:
            if self.tool:
                result = self.tool(state.get_state())
                return result or {}
            return {}

        elif self.node_type == NodeType.CONDITIONAL:
            if self.condition:
                return {"condition_result": self._evaluate_condition(state)}
            return {"condition_result": True}

        elif self.node_type == NodeType.LOOP:
            self.iterations += 1
            should_continue = self.iterations < self.max_iterations
            if self.condition:
                should_continue = should_continue and self._evaluate_condition(state)
            return {"should_loop": should_continue, "iterations": self.iterations}

        return {}

    def _evaluate_condition(self, state: WorkflowState) -> bool:
        """Safely evaluate a condition string"""
        if not self.condition:
            return True

        try:
            safe_dict = {"state": state.get_state()}
            result = eval(self.condition, {"__builtins__": {}}, safe_dict)
            return bool(result)
        except Exception as e:
            print(f"Condition evaluation error: {e}")
            return False

    def reset(self):
        """Reset node state"""
        self.iterations = 0
