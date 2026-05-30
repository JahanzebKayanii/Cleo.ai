import httpx

from app.services.integrations.base import CallData

_BASE = "https://quickbooks.api.intuit.com/v3"


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json"}


async def push(data: CallData, token: str) -> None:
    # QuickBooks requires a company_id (realm_id) alongside the token.
    # Token format expected: "REALM_ID:ACCESS_TOKEN"
    if ":" not in token:
        print("[QuickBooks] Invalid token format. Expected REALM_ID:ACCESS_TOKEN", flush=True)
        return
    realm_id, access_token = token.split(":", 1)
    async with httpx.AsyncClient(timeout=15) as client:
        await _upsert_customer(client, access_token, realm_id, data)
    print(f"[QuickBooks] Pushed customer for {data.customer_name}", flush=True)


async def _upsert_customer(client: httpx.AsyncClient, token: str, realm_id: str, data: CallData) -> str:
    parts = data.customer_name.strip().split(" ", 1) if data.customer_name else ["Unknown"]
    payload = {
        "DisplayName": data.customer_name or data.customer_phone,
        "GivenName": parts[0],
        "FamilyName": parts[1] if len(parts) > 1 else "",
        "PrimaryPhone": {"FreeFormNumber": data.customer_phone},
        "Notes": data.call_summary,
    }
    res = await client.post(
        f"{_BASE}/company/{realm_id}/customer",
        headers={**_headers(token), "Content-Type": "application/json"},
        json=payload,
        params={"minorversion": "65"},
    )
    return res.json().get("Customer", {}).get("Id", "")
