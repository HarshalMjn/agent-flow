import asyncio
from temporalio.worker import Worker
from temporalio.client import Client
from app.config.settings import settings
from app.temporal.workflows.agent_workflow import AgentWorkflow
from app.temporal.activities.node_activities import NodeActivities
from app.temporal.constants import AGENT_FLOW_TASK_QUEUE

async def run_agent_flow_worker(client: Client):
    # Initialize activities
    activities = NodeActivities()
    
    # Register worker
    await Worker(
        client,
        task_queue=AGENT_FLOW_TASK_QUEUE,
        workflows=[AgentWorkflow],
        activities=[activities.execute_node],
    ).run()

async def main():
    # Connect to temporal server with retry logic
    client = None
    retries = 10
    while retries > 0:
        try:
            client = await Client.connect(
                settings.TEMPORAL_HOST, 
                namespace=settings.TEMPORAL_NAMESPACE
            )
            print("✅ Connected to Temporal server")
            break
        except Exception as e:
            retries -= 1
            print(f"⏳ Waiting for Temporal server ({settings.TEMPORAL_HOST})... {retries} retries left. Error: {e}")
            await asyncio.sleep(5)
    
    if not client:
        print("❌ Could not connect to Temporal server. Exiting.")
        return
    
    print(f"🚀 Workers started on task queue: {AGENT_FLOW_TASK_QUEUE}")
    
    # Using gather to support multiple workers in the future, matching Kraken
    await asyncio.gather(
        run_agent_flow_worker(client),
    )

if __name__ == "__main__":
    asyncio.run(main())
