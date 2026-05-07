from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class WebhookConfig(Base):
    __tablename__ = "webhook_configs"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    url = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    events = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    organization = relationship("Organization", back_populates="webhooks")
    logs = relationship("WebhookLog", back_populates="webhook_config")


class WebhookLog(Base):
    __tablename__ = "webhook_logs"

    id = Column(Integer, primary_key=True)
    webhook_config_id = Column(Integer, ForeignKey("webhook_configs.id"), nullable=False)
    event = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    status_code = Column(Integer)
    delivered_at = Column(DateTime(timezone=True), server_default=func.now())

    webhook_config = relationship("WebhookConfig", back_populates="logs")
