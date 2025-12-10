from typing import Dict, Any
import copy

class WorkflowState:
    """Manages the shared state that flows through the workflow"""

    def __init__(self, initial_state: Dict[str, Any] = None):
        self._state = initial_state or {}
        self._history = [copy.deepcopy(self._state)]

    def get(self, key: str, default: Any = None) -> Any:
        return self._state.get(key, default)

    def set(self, key: str, value: Any):
        self._state[key] = value

    def update(self, updates: Dict[str, Any]):
        self._state.update(updates)
        self._history.append(copy.deepcopy(self._state))

    def get_state(self) -> Dict[str, Any]:
        return copy.deepcopy(self._state)

    def get_history(self) -> list:
        return self._history

    def __getitem__(self, key: str) -> Any:
        return self._state[key]

    def __setitem__(self, key: str, value: Any):
        self.set(key, value)
