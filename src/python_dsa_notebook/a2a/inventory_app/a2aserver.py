
import uvicorn

from starlette.applications import Starlette

from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import (
    create_agent_card_routes,
    create_jsonrpc_routes,
)
from a2a.server.tasks import InMemoryTaskStore

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill,
)

from python_dsa_notebook.a2a.inventory_app.agent_executer import (
    InventoryAgentExecutor,
)


HOST = "127.0.0.1"
PORT = 8001
AGENT_URL = f"http://{HOST}:{PORT}/"


# STEP 1: Define agent skill
skill = AgentSkill(
    id="check_inventory",
    name="Check Inventory",
    description="Check available material stock",
    tags=["inventory", "stock"],
    examples=[
        "Check stock for RM100",
        "How much stock is available for RM200?",
    ],
)


# STEP 2: Define Agent Card
agent_card = AgentCard(
    name="Inventory Agent",
    description="Inventory Agent built with LangChain and OpenAI",
    version="1.0.0",
    supported_interfaces=[
        AgentInterface(
            url=AGENT_URL,
            protocol_binding="JSONRPC",
            protocol_version="1.0",
        )
    ],
    capabilities=AgentCapabilities(
        streaming=False,
    ),
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    skills=[skill],
)


# STEP 3: Initialize A2A request handler
handler = DefaultRequestHandler(
    agent_executor=InventoryAgentExecutor(),
    task_store=InMemoryTaskStore(),
    agent_card=agent_card,
)


# STEP 4: Register A2A routes
routes = [
    *create_agent_card_routes(agent_card),
    *create_jsonrpc_routes(handler, "/"),
]


# STEP 5: Create ASGI application
app = Starlette(routes=routes)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
    )
