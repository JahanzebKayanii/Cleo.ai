import httpx
from sqlalchemy import select

from app.services.integrations.base import CallData

_GQL = "https://api.getjobber.com/api/graphql"
_TOKEN_URL = "https://api.getjobber.com/api/oauth/token"
_VERSION = "2024-07-05"


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-JOBBER-GRAPHQL-VERSION": _VERSION,
    }


async def _refresh_access_token(refresh_token: str) -> str | None:
    from app.core.config import settings
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.post(
            _TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "client_id": settings.jobber_client_id,
                "client_secret": settings.jobber_client_secret,
                "refresh_token": refresh_token,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    tokens = res.json()
    return tokens.get("access_token")


async def _get_valid_token(config: dict) -> str | None:
    """Returns a valid access token, refreshing if needed."""
    token = config.get("jobber_api_key")
    if not token:
        return None

    # Try a lightweight introspection query to check token validity
    # We'll just use the token and refresh on 401 inside push()
    return token


async def push(data: CallData, config: dict) -> None:
    """config must include jobber_api_key and optionally jobber_refresh_token."""
    token = config.get("jobber_api_key")
    if not token:
        return

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            client_id = await _upsert_client(client, token, data)
            await _create_request(client, token, data, client_id)
        except _TokenExpiredError:
            # Refresh token and retry once
            refresh_token = config.get("jobber_refresh_token")
            if not refresh_token:
                print("[Jobber] Token expired but no refresh token stored", flush=True)
                return
            new_token = await _refresh_access_token(refresh_token)
            if not new_token:
                print("[Jobber] Token refresh failed", flush=True)
                return
            # Persist new token
            await _save_new_token(new_token)
            client_id = await _upsert_client(client, new_token, data)
            await _create_request(client, new_token, data, client_id)

    print(f"[Jobber] Pushed call for {data.customer_name}", flush=True)


class _TokenExpiredError(Exception):
    pass


async def _save_new_token(new_token: str) -> None:
    from app.core.database import get_db_context
    from app.models.business import Business
    async with get_db_context() as db:
        result = await db.execute(select(Business).where(Business.id == 1))
        biz = result.scalar_one_or_none()
        if biz:
            biz.jobber_api_key = new_token
            await db.commit()


async def _upsert_client(client: httpx.AsyncClient, token: str, data: CallData) -> str:
    query = """
    query SearchClients($q: String!) {
      clients(filter: { keywords: $q }) {
        nodes { id }
      }
    }
    """
    res = await client.post(
        _GQL,
        headers=_headers(token),
        json={"query": query, "variables": {"q": data.customer_phone}},
    )
    print(f"[Jobber] client search status={res.status_code} body={res.text[:300]}", flush=True)
    if res.status_code == 401:
        raise _TokenExpiredError()
    body = res.json()
    if "errors" in body:
        print(f"[Jobber] Client search errors: {body['errors']}", flush=True)
    nodes = body.get("data", {}).get("clients", {}).get("nodes", [])
    if nodes:
        return nodes[0]["id"]

    # Create new client
    parts = data.customer_name.strip().split(" ", 1) if data.customer_name else ["Unknown"]
    inp: dict = {
        "firstName": parts[0],
        "lastName": parts[1] if len(parts) > 1 else "",
        "phones": [{"number": data.customer_phone, "primary": True}],
    }
    if data.address:
        inp["billingAddress"] = {"street": data.address, "postalCode": ""}

    mutation = """
    mutation CreateClient($input: ClientCreateInput!) {
      clientCreate(input: $input) {
        client { id }
        userErrors { message }
      }
    }
    """
    res = await client.post(
        _GQL,
        headers=_headers(token),
        json={"query": mutation, "variables": {"input": inp}},
    )
    print(f"[Jobber] clientCreate status={res.status_code} body={res.text[:300]}", flush=True)
    if res.status_code == 401:
        raise _TokenExpiredError()
    body = res.json()
    errors = body.get("data", {}).get("clientCreate", {}).get("userErrors", [])
    if errors:
        print(f"[Jobber] clientCreate errors: {errors}", flush=True)
    return body["data"]["clientCreate"]["client"]["id"]


async def _create_request(
    client: httpx.AsyncClient, token: str, data: CallData, client_id: str
) -> None:
    title = data.service_type
    if data.issue_description:
        title = f"{data.service_type} – {data.issue_description[:60]}"

    lines = []
    if data.issue_description:
        lines.append(f"Issue: {data.issue_description}")
    if data.address:
        lines.append(f"Service address: {data.address}")
    if data.booked and data.appointment_date:
        appt = data.appointment_date
        if data.appointment_time:
            appt += f" {data.appointment_time}"
        lines.append(f"Appointment: {appt}")
    if data.call_summary:
        lines.append(f"\nSummary: {data.call_summary}")
    details = "\n".join(lines) or data.call_summary

    mutation = """
    mutation CreateRequest($input: RequestCreateInput!) {
      requestCreate(input: $input) {
        request { id }
        userErrors { message }
      }
    }
    """
    res = await client.post(
        _GQL,
        headers=_headers(token),
        json={"query": mutation, "variables": {"input": {"title": title, "clientId": client_id, "details": details}}},
    )
    print(f"[Jobber] requestCreate status={res.status_code} body={res.text[:300]}", flush=True)
    if res.status_code == 401:
        raise _TokenExpiredError()
    body = res.json()
    if "errors" in body:
        print(f"[Jobber] requestCreate GraphQL errors: {body['errors']}", flush=True)
        return
    errors = body.get("data", {}).get("requestCreate", {}).get("userErrors", [])
    if errors:
        print(f"[Jobber] requestCreate userErrors: {errors}", flush=True)
