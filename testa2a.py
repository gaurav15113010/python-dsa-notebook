
import asyncio
import httpx

from a2a.client import (
    A2ACardResolver,
    ClientConfig,
    create_client,
)
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest


async def main():

    base_url = "http://127.0.0.1:8001"

    # 1. Discover the remote agent
    async with httpx.AsyncClient() as http_client:
        resolver = A2ACardResolver(
            httpx_client=http_client,
            base_url=base_url,
        )

        agent_card = await resolver.get_agent_card()

    print("Discovered Agent:", agent_card.name)

    # 2. Create A2A client
    config = ClientConfig(streaming=False)

    client = await create_client(
        agent=agent_card,
        client_config=config,
    )

    # 3. Prepare A2A request
    message = new_text_message(
        "Check stock for RM100",
        role=Role.ROLE_USER,
    )

    request = SendMessageRequest(message=message)

    # 4. Send message to Inventory Agent
    async for response in client.send_message(request):
        print("A2A Response:")
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
