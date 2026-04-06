from fastapi import APIRouter
from app.controllers import workflow_controller
from app.schemas import workflow_schemas

router = APIRouter()

@router.post("/", response_model=workflow_schemas.WorkflowResponse)
async def create_workflow(workflow: workflow_schemas.WorkflowCreate):
    return await workflow_controller.create_workflow(workflow)

@router.get("/{workflow_id}", response_model=workflow_schemas.WorkflowResponse)
async def get_workflow(workflow_id: str):
    return await workflow_controller.get_workflow(workflow_id)

@router.post("/{workflow_id}/execute")
async def execute_workflow(workflow_id: str, input_data: dict):
    return await workflow_controller.execute_workflow(workflow_id, input_data)
