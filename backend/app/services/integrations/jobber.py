import httpx

from app.services.integrations.base import CallData

_GQL = "https://api.getjobber.com/api/graphql"


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "X-JOBBER-GRAPHQL-VERSION": "2024-07-05"}


async def push(data: CallData, token: str) -> None:
    async with httpx.AsyncClient(timeout=15) as client:
        client_id = await _upsert_client(client, token, data)
        await _create_request(client, token, data, client_id)
    print(f"[Jobber] Pushed call for {data.customer_name}", flush=True)


async def _upsert_client(client: httpx.AsyncClient, token: str, data: CallData) -> str:
    # Search existing clients by phone
    query = """
    query SearchClients($phone: String!) {
      clients(filter: { phone: $phone }) {
        nodes { id }
      }
    }
    """
    res = await client.post(_GQL, headers=_headers(token), json={"query": query, "variables": {"phone": data.customer_phone}})
    nodes = res.json().get("data", {}).get("clients", {}).get("nodes", [])
    if nodes:
        return nodes[0]["id"]

    parts = data.customer_name.strip().split(" ", 1) if data.customer_name else ["Unknown"]
    mutation = """
    mutation CreateClient($input: ClientCreateInput!) {
      clientCreate(input: $input) {
        client { id }
        userErrors { message }
      }
    }
    """
    inp = {
        "firstName": parts[0],
        "lastName": parts[1] if len(parts) > 1 else "",
        "phones": [{"number": data.customer_phone, "primary": True}],
    }
    res = await client.post(_GQL, headers=_headers(token), json={"query": mutation, "variables": {"input": inp}})
    return res.json()["data"]["clientCreate"]["client"]["id"]


async def _create_request(client: httpx.AsyncClient, token: str, data: CallData, client_id: str) -> None:
    title = f"{data.service_type} – {data.issue_description[:60]}" if data.issue_description else data.service_type
    mutation = """
    mutation CreateRequest($input: RequestCreateInput!) {
      requestCreate(input: $input) {
        request { id }
        userErrors { message }
      }
    }
    """
    inp = {
        "title": title,
        "clientId": client_id,
        "details": data.call_summary,
    }
    await client.post(_GQL, headers=_headers(token), json={"query": mutation, "variables": {"input": inp}})
