from sqlalchemy.future import select
from app.config.database import AsyncSessionLocal
from app.models.workflow import WorkflowModel
from app.schemas.workflow_schemas import WorkflowCreate, WorkflowResponse
from app.services.workflow_engine import workflow_engine

class WorkflowController:
    async def create_workflow(self, workflow_data: WorkflowCreate) -> WorkflowResponse:
        async with AsyncSessionLocal() as session:
            new_wf = WorkflowModel(
                name=workflow_data.name,
                description=workflow_data.description,
                nodes=[node.model_dump() for node in workflow_data.nodes],
                edges=[edge.model_dump() for edge in workflow_data.edges]
            )
            session.add(new_wf)
            await session.commit()
            await session.refresh(new_wf)
            return WorkflowResponse.model_validate(new_wf.to_dict())

    async def get_workflow(self, workflow_id: str) -> WorkflowResponse:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(WorkflowModel).where(WorkflowModel.id == workflow_id))
            workflow = result.scalar_one_or_none()
            if not workflow:
                raise ValueError("Workflow not found")
            return WorkflowResponse.model_validate(workflow.to_dict())

    async def execute_workflow(self, workflow_id: str, input_data: dict):
        # First retrieve the workflow structure
        workflow_resp = await self.get_workflow(workflow_id)
        
        # Then trigger execution via Temporal
        # WorkflowResponse to WorkflowCreate (minimal conversion)
        wf_create = WorkflowCreate(
            name=workflow_resp.name,
            description=workflow_resp.description,
            nodes=workflow_resp.nodes,
            edges=workflow_resp.edges
        )
        return await workflow_engine.execute_workflow(wf_create, input_data)

workflow_controller = WorkflowController()
