"""Code Review Mini-Agent Workflow"""
from app.tools.registry import tool_registry

def extract_functions(state: dict) -> dict:
    """Extract functions from code"""
    code = state.get("code", "")
    functions = []
    lines = code.split("\n")
    for line in lines:
        if line.strip().startswith("def "):
            func_name = line.split("def ")[1].split("(")[0]
            functions.append(func_name)

    return {
        "functions": functions,
        "function_count": len(functions)
    }

def check_complexity(state: dict) -> dict:
    """Check code complexity"""
    code = state.get("code", "")
    lines = len(code.split("\n"))
    complexity_score = min(lines / 10, 10)

    return {
        "complexity_score": complexity_score,
        "lines_of_code": lines
    }

def detect_issues(state: dict) -> dict:
    """Detect basic code issues"""
    code = state.get("code", "")
    issues = []

    if "TODO" in code:
        issues.append("Contains TODO comments")
    if "print(" in code:
        issues.append("Contains print statements")
    if len(code.split("\n")) > 100:
        issues.append("File too long (>100 lines)")

    return {
        "issues": issues,
        "issue_count": len(issues)
    }

def suggest_improvements(state: dict) -> dict:
    """Suggest code improvements"""
    issues = state.get("issues", [])
    suggestions = []

    for issue in issues:
        if "TODO" in issue:
            suggestions.append("Complete TODO items before merging")
        if "print" in issue:
            suggestions.append("Replace print with logging")
        if "too long" in issue:
            suggestions.append("Split into smaller modules")

    return {
        "suggestions": suggestions,
        "suggestion_count": len(suggestions)
    }

def calculate_quality_score(state: dict) -> dict:
    """Calculate overall quality score"""
    issue_count = state.get("issue_count", 0)
    complexity = state.get("complexity_score", 5)
    quality_score = max(0, 10 - issue_count - (complexity / 2))

    return {
        "quality_score": quality_score,
        "quality_check_complete": True
    }

def register_code_review_tools():
    tool_registry.register("extract_functions", extract_functions)
    tool_registry.register("check_complexity", check_complexity)
    tool_registry.register("detect_issues", detect_issues)
    tool_registry.register("suggest_improvements", suggest_improvements)
    tool_registry.register("calculate_quality_score", calculate_quality_score)
