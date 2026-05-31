from dataclasses import dataclass


@dataclass
class CallData:
    customer_name: str
    customer_phone: str
    service_type: str
    issue_description: str
    booked: bool
    appointment_date: str | None
    appointment_time: str | None
    call_summary: str
    address: str = ""
