import uuid
from typing import List, Dict, Any
from temporalio.client import Client
from app.config.settings import settings
from app.schemas.workflow_schemas import WorkflowCreate, WorkflowResponse, Node, Edge


class WorkflowEngine:
    def __init__(self):
        self.temporal_client = None

    async def get_client(self):
        if not self.temporal_client:
            retries = 5
            while retries > 0:
                try:
                    self.temporal_client = await Client.connect(settings.TEMPORAL_HOST)
                    break
                except Exception:
                    retries -= 1
                    await asyncio.sleep(2)
            if not self.temporal_client:
                raise ConnectionError(
                    f"Could not connect to Temporal at {settings.TEMPORAL_HOST}"
                )
        return self.temporal_client

    def validate_dag(self, nodes: List[Node], edges: List[Edge]):
        """
        Validates that the graph is a Directed Acyclic Graph (DAG).
        Simple cycle detection.
        """
        adj = {node.id: [] for node in nodes}
        for edge in edges:
            adj[edge.source].append(edge.target)

        visited = set()
        stack = set()

        def has_cycle(v):
            visited.add(v)
            stack.add(v)
            for neighbor in adj.get(v, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in stack:
                    return True
            stack.remove(v)
            return False

        for node in nodes:
            if node.id not in visited:
                if has_cycle(node.id):
                    raise ValueError(f"Cycle detected in workflow at node {node.id}")
        return True

    async def execute_workflow(
        self, workflow_data: WorkflowCreate, input_data: Dict[str, Any]
    ):
        """
        Triggers a Temporal workflow for the given DAG.
        """
        self.validate_dag(workflow_data.nodes, workflow_data.edges)

        client = await self.get_client()
        workflow_id = f"wf-{uuid.uuid4()}"

        from app.temporal.workflows.agent_workflow import AgentWorkflow

        # Start the workflow
        handle = await client.start_workflow(
            AgentWorkflow.run,
            args=[workflow_data.model_dump(), input_data],
            id=workflow_id,
            task_queue=settings.TEMPORAL_TASK_QUEUE,
        )

        return {"workflow_id": workflow_id, "run_id": handle.run_id}


workflow_engine = WorkflowEngine()
