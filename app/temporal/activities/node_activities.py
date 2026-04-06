from typing import Dict, Any, List
from temporalio import activity
import litellm
import httpx
import json

class NodeActivities:
    @activity.defn
    async def execute_node(self, node: Dict[str, Any], node_outputs: Dict[str, Any]) -> Any:
        """
        Executes a workflow node based on its type.
        """
        node_type = node.get("data", {}).get("type")
        config = node.get("data", {}).get("config", {})
        
        # Prepare inputs for the node (can depend on other nodes)
        # For simplicity, we pass all previous node outputs for use in jinja or similar
        input_data = node_outputs
        
        if node_type == "llm":
            return await self.execute_llm_node(config, input_data)
        elif node_type == "api":
            return await self.execute_api_node(config, input_data)
        elif node_type == "logic":
            return await self.execute_logic_node(config, input_data)
        elif node_type == "input":
            return config.get("value", {})
        elif node_type == "output":
            return config.get("value", {})
        else:
            raise ValueError(f"Unknown node type: {node_type}")

    async def execute_llm_node(self, config: Dict[str, Any], inputs: Dict[str, Any]) -> str:
        """
        Executes an LLM node via LiteLLM.
        """
        prompt_template = config.get("prompt", "")
        model = config.get("model", "gpt-4o")
        
        # Simple Jinja-like replacement (for demo, real app would use a renderer)
        prompt = prompt_template
        for key, value in inputs.items():
            if isinstance(value, str):
                prompt = prompt.replace(f"{{{{{key}}}}}", str(value))
            elif isinstance(value, dict):
                prompt = prompt.replace(f"{{{{{key}}}}}", json.dumps(value))

        response = await litellm.acompletion(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    async def execute_api_node(self, config: Dict[str, Any], inputs: Dict[str, Any]) -> Any:
        """
        Executes an external API call.
        """
        url = config.get("url")
        method = config.get("method", "GET")
        headers = config.get("headers", {})
        body = config.get("body", {})
        
        async with httpx.AsyncClient() as client:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=body)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            return response.json()

    async def execute_logic_node(self, config: Dict[str, Any], inputs: Dict[str, Any]) -> Any:
        # Simple logic node (e.g. if/else)
        # For demo, just returns the value of a field if present
        # In a real app, this would be an eval or a predefined logic set
        condition = config.get("condition")
        if condition == "pass":
            return inputs
        return {"status": "condition not met"}
