from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
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
    # Integration API keys
    jobber_api_key: Mapped[str | None] = mapped_column(Text)
    hubspot_token: Mapped[str | None] = mapped_column(Text)
    housecall_pro_api_key: Mapped[str | None] = mapped_column(Text)
    quickbooks_token: Mapped[str | None] = mapped_column(Text)
    servicetitan_token: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
