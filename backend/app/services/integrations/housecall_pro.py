import httpx

from app.services.integrations.base import CallData

_BASE = "https://api.housecallpro.com"


def _headers(api_key: str) -> dict:
    return {"Authorization": f"Token {api_key}", "Content-Type": "application/json"}


async def push(data: CallData, api_key: str) -> None:
    async with httpx.AsyncClient(timeout=15) as client:
        customer_id = await _upsert_customer(client, api_key, data)
        await _create_job(client, api_key, data, customer_id)
    print(f"[HousecallPro] Pushed call for {data.customer_name}", flush=True)


async def _upsert_customer(client: httpx.AsyncClient, api_key: str, data: CallData) -> str:
    # Search by phone
    res = await client.get(f"{_BASE}/v1/customers", headers=_headers(api_key), params={"q": data.customer_phone})
    customers = res.json().get("customers", [])
    if customers:
        return customers[0]["id"]

    parts = data.customer_name.strip().split(" ", 1) if data.customer_name else ["Unknown"]
    payload = {
        "first_name": parts[0],
        "last_name": parts[1] if len(parts) > 1 else "",
        "mobile_number": data.customer_phone,
    }
    res = await client.post(f"{_BASE}/v1/customers", headers=_headers(api_key), json=payload)
    return res.json()["id"]


async def _create_job(client: httpx.AsyncClient, api_key: str, data: CallData, customer_id: str) -> None:
    payload = {
        "customer_id": customer_id,
        "job_type": data.service_type,
        "note": data.call_summary,
        "work_status": "needs scheduling" if not data.booked else "scheduled",
    }
    await client.post(f"{_BASE}/v1/jobs", headers=_headers(api_key), json=payload)
