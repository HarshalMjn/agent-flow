from datetime import timedelta
from typing import List, Dict, Any, Optional
from temporalio import workflow

# Import activities
with workflow.unsafe.imports_passed_through():
    from app.temporal.activities.node_activities import NodeActivities

@workflow.defn
class AgentWorkflow:
    @workflow.run
    async def run(self, workflow_data: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a DAG-based workflow.
        """
        nodes = workflow_data.get("nodes", [])
        edges = workflow_data.get("edges", [])
        
        # Build adjacency list
        node_map = {node["id"]: node for node in nodes}
        adj = {node["id"]: [] for node in nodes}
        in_degree = {node["id"]: 0 for node in nodes}
        
        for edge in edges:
            source = edge["source"]
            target = edge["target"]
            adj[source].append(target)
            in_degree[target] += 1
            
        # Topological Sort Execution (Kahn's algorithm style)
        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        results = { "input": input_data }
        node_outputs = {}
        
        while queue:
            # Execute independent nodes in parallel (if possible)
            # For simplicity, we execute sequentially here, but Temporal allows parallel activities
            node_id = queue.pop(0)
            node = node_map[node_id]
            
            # Execute node activity
            output = await workflow.execute_activity(
                NodeActivities.execute_node,
                args=[node, node_outputs],
                start_to_close_timeout=timedelta(minutes=5),
            )
            
            node_outputs[node_id] = output
            
            # Update neighbors
            for neighbor in adj.get(node_id, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return node_outputs
