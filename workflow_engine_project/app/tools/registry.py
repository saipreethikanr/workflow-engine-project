from typing import Dict, Callable

class ToolRegistry:
    """Central registry for all available tools"""

    def __init__(self):
        self._tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        """Register a tool function"""
        self._tools[name] = func

    def get(self, name: str) -> Callable:
        """Get a tool by name"""
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found in registry")
        return self._tools[name]

    def list_tools(self) -> list:
        """List all registered tools"""
        return list(self._tools.keys())

tool_registry = ToolRegistry()
