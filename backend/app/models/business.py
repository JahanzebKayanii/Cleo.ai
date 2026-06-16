from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Business(Base):
    __tablename__ = "business"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), default="Apex Home Services")
    description: Mapped[str | None] = mapped_column(Text)
    timezone: Mapped[str] = mapped_column(String(64), default="America/Chicago")
    services: Mapped[str] = mapped_column(Text, default='["HVAC", "plumbing", "electrical"]')
    hours_open: Mapped[int] = mapped_column(Integer, default=8)
    hours_close: Mapped[int] = mapped_column(Integer, default=18)
    service_area: Mapped[str | None] = mapped_column(Text, default="Austin, TX and surrounding areas within 30 miles")
    owner_email: Mapped[str | None] = mapped_column(String(255))
    transfer_phone: Mapped[str | None] = mapped_column(String(20))
    # Multi-tenant fields
    twilio_phone_number: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    slug: Mapped[str | None] = mapped_column(String(50), unique=True, index=True)
    dashboard_password: Mapped[str | None] = mapped_column(String(255))
    industry: Mapped[str] = mapped_column(String(50), default="hvac")
    qdrant_collection: Mapped[str | None] = mapped_column(String(100))
    google_calendar_id: Mapped[str | None] = mapped_column(Text)
    google_service_account_b64: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    stripe_customer_id: Mapped[str | None] = mapped_column(String(100))
    stripe_subscription_id: Mapped[str | None] = mapped_column(String(100))
    custom_instructions: Mapped[str | None] = mapped_column(Text)
    # Integration API keys / OAuth tokens
    jobber_api_key: Mapped[str | None] = mapped_column(Text)
    jobber_refresh_token: Mapped[str | None] = mapped_column(Text)
    hubspot_token: Mapped[str | None] = mapped_column(Text)
    housecall_pro_api_key: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
