import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


def _send(to_email: str, subject: str, html: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.gmail_user
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(settings.gmail_user, settings.gmail_app_password)
        server.sendmail(settings.gmail_user, to_email, msg.as_string())


async def send_call_summary(
    to_email: str,
    business_name: str,
    customer_name: str | None,
    customer_phone: str,
    summary: str,
    transcript: str | None,
    booked: bool = False,
    appointment_date: str | None = None,
    appointment_time: str | None = None,
) -> None:
    if not to_email or not settings.gmail_user or not settings.gmail_app_password:
        return

    caller = customer_name or customer_phone or "Unknown caller"
    appt_line = ""
    if booked and appointment_date:
        appt_line = f"<p><strong>Appointment:</strong> {appointment_date}{' ' + appointment_time if appointment_time else ''}</p>"

    transcript_section = ""
    if transcript:
        formatted = transcript.replace("\n", "<br>")
        transcript_section = f"""
        <details style="margin-top:24px">
          <summary style="cursor:pointer;color:#7c3aed;font-size:13px">View full transcript</summary>
          <div style="margin-top:12px;padding:16px;background:#f9f9f9;border-radius:8px;font-size:13px;line-height:1.6;color:#444;white-space:pre-wrap">{formatted}</div>
        </details>"""

    html = f"""
    <div style="font-family:Inter,Arial,sans-serif;max-width:560px;margin:0 auto;padding:32px 24px;background:#fff">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:24px">
        <div style="width:32px;height:32px;background:#7c3aed;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:14px">C</div>
        <span style="font-weight:600;color:#111;font-size:16px">Cleo</span>
      </div>

      <h2 style="font-size:20px;font-weight:600;color:#111;margin:0 0 4px">Call Summary</h2>
      <p style="color:#888;font-size:13px;margin:0 0 24px">{business_name}</p>

      <div style="background:#f5f3ff;border-radius:12px;padding:20px;margin-bottom:20px">
        <p style="margin:0 0 8px"><strong>Caller:</strong> {caller}</p>
        <p style="margin:0 0 8px"><strong>Phone:</strong> {customer_phone}</p>
        {appt_line}
        <p style="margin:0"><strong>Booked:</strong> {'Yes' if booked else 'No'}</p>
      </div>

      <div style="border-left:3px solid #7c3aed;padding-left:16px;margin-bottom:24px">
        <p style="font-size:13px;color:#555;line-height:1.6;margin:0">{summary}</p>
      </div>

      {transcript_section}

      <p style="font-size:11px;color:#bbb;margin-top:32px;border-top:1px solid #eee;padding-top:16px">
        Sent by Cleo Voice AI · <a href="#" style="color:#bbb">Unsubscribe</a>
      </p>
    </div>
    """

    subject = f"Call Summary — {caller}"
    if booked:
        subject += f" — Appointment Booked"

    try:
        await asyncio.to_thread(_send, to_email, subject, html)
        print(f"[Email] Summary sent to {to_email} for caller {caller}", flush=True)
    except Exception as e:
        print(f"[Email] Failed to send to {to_email}: {e}", flush=True)
