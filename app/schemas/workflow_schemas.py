from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional

class NodeData(BaseModel):
    label: str
    type: str # 'llm', 'api', 'logic', 'input', 'output'
    config: Dict[str, Any]

class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: NodeData

class Edge(BaseModel):
    id: str
    source: str
    target: str

class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    nodes: List[Node]
    edges: List[Edge]

class WorkflowResponse(BaseModel):
    id: str
    name: str
    status: str
    nodes: List[Node]
    edges: List[Edge]
    
    model_config = ConfigDict(from_attributes=True)
