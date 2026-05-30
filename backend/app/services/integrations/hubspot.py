import httpx

from app.services.integrations.base import CallData

_BASE = "https://api.hubapi.com"


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


async def push(data: CallData, token: str) -> None:
    async with httpx.AsyncClient(timeout=15) as client:
        contact_id = await _upsert_contact(client, token, data)
        deal_id = await _create_deal(client, token, data, contact_id)
        await _create_note(client, token, data, contact_id, deal_id)
    print(f"[HubSpot] Pushed call for {data.customer_name}", flush=True)


async def _upsert_contact(client: httpx.AsyncClient, token: str, data: CallData) -> str:
    # Search by phone
    res = await client.post(
        f"{_BASE}/crm/v3/objects/contacts/search",
        headers=_headers(token),
        json={"filterGroups": [{"filters": [{"propertyName": "phone", "operator": "EQ", "value": data.customer_phone}]}]},
    )
    results = res.json().get("results", [])
    if results:
        return results[0]["id"]

    # Create new contact
    props = {
        "phone": data.customer_phone,
        "hs_lead_status": "NEW",
        "lead_source": "Cleo AI Voice",
    }
    if data.customer_name:
        parts = data.customer_name.strip().split(" ", 1)
        props["firstname"] = parts[0]
        if len(parts) > 1:
            props["lastname"] = parts[1]

    res = await client.post(f"{_BASE}/crm/v3/objects/contacts", headers=_headers(token), json={"properties": props})
    data_json = res.json()
    print(f"[HubSpot] Contact create response ({res.status_code}): {data_json}", flush=True)
    if "id" not in data_json:
        # Retry with minimal fields only
        minimal = {"phone": data.customer_phone}
        if data.customer_name:
            parts = data.customer_name.strip().split(" ", 1)
            minimal["firstname"] = parts[0]
            if len(parts) > 1:
                minimal["lastname"] = parts[1]
        res = await client.post(f"{_BASE}/crm/v3/objects/contacts", headers=_headers(token), json={"properties": minimal})
        data_json = res.json()
        print(f"[HubSpot] Contact retry response ({res.status_code}): {data_json}", flush=True)
    return data_json["id"]


async def _create_deal(client: httpx.AsyncClient, token: str, data: CallData, contact_id: str) -> str:
    stage = "closedwon" if data.booked else "appointmentscheduled"
    deal_name = f"{data.service_type} – {data.customer_name}"
    if data.booked and data.appointment_date:
        appt = data.appointment_date
        if data.appointment_time:
            appt += f" {data.appointment_time}"
        deal_name += f" | {appt}"

    description = ""
    if data.issue_description:
        description += f"Issue: {data.issue_description}\n"
    if data.call_summary:
        description += f"\nCall summary: {data.call_summary}"

    props = {
        "dealname": deal_name,
        "dealstage": stage,
        "pipeline": "default",
        "description": description.strip(),
    }
    if data.booked and data.appointment_date:
        props["closedate"] = data.appointment_date

    res = await client.post(
        f"{_BASE}/crm/v3/objects/deals",
        headers=_headers(token),
        json={"properties": props},
    )
    deal_id = res.json()["id"]
    # Associate deal with contact
    await client.put(
        f"{_BASE}/crm/v3/objects/deals/{deal_id}/associations/contacts/{contact_id}/deal_to_contact",
        headers=_headers(token),
    )
    return deal_id


async def _create_note(client: httpx.AsyncClient, token: str, data: CallData, contact_id: str, deal_id: str) -> None:
    body = f"Call summary: {data.call_summary}"
    if data.booked and data.appointment_date:
        body += f"\nAppointment: {data.appointment_date} {data.appointment_time or ''}"
    res = await client.post(
        f"{_BASE}/crm/v3/objects/notes",
        headers=_headers(token),
        json={"properties": {"hs_note_body": body, "hs_timestamp": "0"}},
    )
    note_id = res.json()["id"]
    for obj_type, obj_id, assoc in [
        ("contacts", contact_id, "note_to_contact"),
        ("deals", deal_id, "note_to_deal"),
    ]:
        await client.put(
            f"{_BASE}/crm/v3/objects/notes/{note_id}/associations/{obj_type}/{obj_id}/{assoc}",
            headers=_headers(token),
        )
