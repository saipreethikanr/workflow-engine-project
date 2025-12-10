"""FastAPI application for workflow engine"""
from fastapi import FastAPI, HTTPException
import uuid
from app.models import (
    GraphCreateRequest, GraphRunRequest, GraphRunResponse,
    NodeType, ExecutionLog
)
from app.engine.graph import WorkflowGraph
from app.engine.node import Node
from app.tools.registry import tool_registry
from app.storage.memory import storage
from app.workflows.code_review import register_code_review_tools

app = FastAPI(
    title="Workflow Engine API",
    description="A minimal workflow/graph engine for building agent workflows",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    register_code_review_tools()

@app.get("/")
async def root():
    return {
        "message": "Workflow Engine API",
        "endpoints": {
            "create_graph": "POST /graph/create",
            "run_graph": "POST /graph/run",
            "get_state": "GET /graph/state/{run_id}",
            "list_graphs": "GET /graphs",
            "list_tools": "GET /tools"
        }
    }

@app.post("/graph/create")
async def create_graph(request: GraphCreateRequest):
    """Create a new workflow graph"""
    try:
        graph_def = request.graph
        graph = WorkflowGraph(entry_point=graph_def.entry_point)

        for node_def in graph_def.nodes:
            tool = None
            if node_def.tool:
                tool = tool_registry.get(node_def.tool)

            node = Node(
                name=node_def.name,
                node_type=node_def.type,
                tool=tool,
                condition=node_def.condition,
                max_iterations=node_def.max_iterations or 10
            )
            graph.add_node(node)

        for edge_def in graph_def.edges:
            graph.add_edge(
                edge_def.from_node,
                edge_def.to_node,
                edge_def.condition
            )

        graph_id = storage.save_graph(graph, request.name)

        return {
            "graph_id": graph_id,
            "name": request.name,
            "nodes": len(graph_def.nodes),
            "edges": len(graph_def.edges)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/graph/run")
async def run_graph(request: GraphRunRequest):
    """Run a workflow graph"""
    try:
        graph = storage.get_graph(request.graph_id)
        if not graph:
            raise HTTPException(status_code=404, detail="Graph not found")

        final_state, execution_log = await graph.run(request.initial_state)
        run_id = str(uuid.uuid4())

        storage.save_run(
            run_id,
            final_state,
            "completed",
            [log.dict() for log in execution_log]
        )

        return GraphRunResponse(
            run_id=run_id,
            final_state=final_state.get_state(),
            execution_log=execution_log,
            status="completed"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph/state/{run_id}")
async def get_run_state(run_id: str):
    """Get the state of a workflow run"""
    run_data = storage.get_run(run_id)
    if not run_data:
        raise HTTPException(status_code=404, detail="Run not found")
    return run_data

@app.get("/graphs")
async def list_graphs():
    """List all created graphs"""
    return {"graphs": storage.list_graphs()}

@app.get("/tools")
async def list_tools():
    """List all registered tools"""
    return {"tools": tool_registry.list_tools()}
