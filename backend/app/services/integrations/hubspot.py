import time

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
        contact_id = results[0]["id"]
        if data.address:
            await client.patch(
                f"{_BASE}/crm/v3/objects/contacts/{contact_id}",
                headers=_headers(token),
                json={"properties": {"address": data.address}},
            )
        return contact_id

    # Create new contact
    props = {"phone": data.customer_phone, "hs_lead_status": "NEW"}
    if data.customer_name:
        parts = data.customer_name.strip().split(" ", 1)
        props["firstname"] = parts[0]
        if len(parts) > 1:
            props["lastname"] = parts[1]
    if data.address:
        props["address"] = data.address

    res = await client.post(f"{_BASE}/crm/v3/objects/contacts", headers=_headers(token), json={"properties": props})
    return res.json()["id"]


async def _create_deal(client: httpx.AsyncClient, token: str, data: CallData, contact_id: str) -> str:
    stage = "closedwon" if data.booked else "appointmentscheduled"
    deal_name = f"{data.service_type} – {data.customer_name}"
    if data.booked and data.appointment_date:
        appt = data.appointment_date
        if data.appointment_time:
            appt += f" {data.appointment_time}"
        deal_name += f" | {appt}"

    notes_body = ""
    if data.issue_description:
        notes_body += f"Issue: {data.issue_description}\n"
    if data.call_summary:
        notes_body += f"Summary: {data.call_summary}"

    props = {
        "dealname": deal_name,
        "dealstage": stage,
        "hs_deal_stage_probability": "1" if data.booked else "0.5",
    }
    if notes_body:
        props["description"] = notes_body
    if data.booked and data.appointment_date:
        from datetime import datetime
        try:
            ts = int(datetime.strptime(data.appointment_date, "%Y-%m-%d").timestamp() * 1000)
            props["closedate"] = str(ts)
        except Exception:
            pass

    res = await client.post(
        f"{_BASE}/crm/v3/objects/deals",
        headers=_headers(token),
        json={"properties": props},
    )
    deal_id = res.json()["id"]
    await client.put(
        f"{_BASE}/crm/v3/objects/deals/{deal_id}/associations/contacts/{contact_id}/deal_to_contact",
        headers=_headers(token),
    )
    return deal_id


async def _create_note(client: httpx.AsyncClient, token: str, data: CallData, contact_id: str, deal_id: str) -> None:
    lines = []
    if data.issue_description:
        lines.append(f"Issue: {data.issue_description}")
    if data.address:
        lines.append(f"Service address: {data.address}")
    if data.booked and data.appointment_date:
        lines.append(f"Appointment: {data.appointment_date} {data.appointment_time or ''}".strip())
    if data.call_summary:
        lines.append(f"\nSummary: {data.call_summary}")
    body = "\n".join(lines)
    if not body:
        return
    ts = str(int(time.time() * 1000))
    res = await client.post(
        f"{_BASE}/crm/v3/objects/notes",
        headers=_headers(token),
        json={"properties": {"hs_note_body": body, "hs_timestamp": ts}},
    )
    data_resp = res.json()
    if "id" not in data_resp:
        print(f"[HubSpot] Note creation failed: {data_resp}", flush=True)
        return
    note_id = data_resp["id"]
    for obj_type, obj_id, assoc in [
        ("contacts", contact_id, "note_to_contact"),
        ("deals", deal_id, "note_to_deal"),
    ]:
        await client.put(
            f"{_BASE}/crm/v3/objects/notes/{note_id}/associations/{obj_type}/{obj_id}/{assoc}",
            headers=_headers(token),
        )
