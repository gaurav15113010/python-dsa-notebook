
import logging

from a2a.server.agent_execution import (
    AgentExecutor,
    RequestContext,
)
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.helpers import (
    get_message_text,
    new_task_from_user_message,
    new_text_message,
    new_text_part,
)

from python_dsa_notebook.a2a.inventory_app.inventory_agent import (
    run_inventory_agent,
)


logger = logging.getLogger(__name__)


class InventoryAgentExecutor(AgentExecutor):

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:

        # STEP 1: Retrieve the incoming A2A message
        message = context.message

        if message is None:
            raise ValueError("No A2A message provided")

        # STEP 2: Get existing task or create new task
        if context.current_task:
            task = context.current_task
        else:
            task = new_task_from_user_message(message)
            await event_queue.enqueue_event(task)

        # STEP 3: Create TaskUpdater
        updater = TaskUpdater(
            event_queue=event_queue,
            task_id=task.id,
            context_id=task.context_id,
        )

        try:
            # STEP 4: Extract text from A2A message
            query = get_message_text(message).strip()

            if not query:
                raise ValueError("Message text cannot be empty")

            logger.info("Received A2A request: %s", query)

            # STEP 5: Mark task as WORKING
            await updater.start_work(
                new_text_message("Checking inventory...")
            )

            # STEP 6: Call our existing LangChain agent
            result = await run_inventory_agent(query)

            logger.info("LangChain result: %s", result)

            # STEP 7: Add result as A2A artifact
            await updater.add_artifact(
                name="Inventory Result",
                parts=[
                    new_text_part(
                        text=result,
                        media_type="text/plain",
                    )
                ],
            )

            # STEP 8: Mark task as COMPLETED
            await updater.complete(
                new_text_message(
                    "Inventory check completed"
                )
            )

        except Exception:
            logger.exception("Inventory agent execution failed")

            # Send failure status without exposing internals
            await updater.failed(
                new_text_message(
                    "Inventory check failed"
                )
            )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        raise NotImplementedError(
            "Task cancellation is not supported"
        )
