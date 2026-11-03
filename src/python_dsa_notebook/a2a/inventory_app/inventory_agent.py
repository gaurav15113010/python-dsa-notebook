from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

# load_dotenv(Path(__file__).resolve().parents[1] / ".env")
load_dotenv(override=True)


# Simulated inventory database
INVENTORY = {
    "RM100": 1000,
    "RM200": 250,
    "RM300": 0,
}

@tool
def check_inventory(material_id: str) -> str:
    """Check available stock for a material ID."""

    if material_id not in INVENTORY:
        return f"Material {material_id} not found"

    quantity = INVENTORY[material_id]

    return (
        f"Material {material_id} has "
        f"{quantity} units available"
    )

# model = ChatOpenAI(
#     model="gpt-5.4-mini",
#     temperature=0
# )

inventory_agent = create_agent(

    model="openai:gpt-5.4-mini",
    tools = [check_inventory],
    system_prompt = """
    You are an inventory management agent. Use the check_inventory tool to answer
    stock availability questions. Never invent stock quantities.
    """
)



async def run_inventory_agent(query: str) -> str:
    result = await inventory_agent.ainvoke(
        
        {
            "messages":[{"role": "user", "content": query}]
        }
        
    )
    return str(result["messages"][-1].content)

if __name__ == "__main__":
    import asyncio

    answer = asyncio.run(run_inventory_agent("How many RM100 are available?"))
    print(answer)

# Agent Card :An Agent Card is a machine-readable JSON document describing an agent's identity, capabilities, 
# skills, and communication interfaces. It is used to describe the agent to other agents and users.