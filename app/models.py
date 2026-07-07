from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class IOCCache(Base):
    __tablename__ = "ioc_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ioc: Mapped[str] = mapped_column(String(512), index=True)
    ioc_type: Mapped[str] = mapped_column(String(50), index=True)
    source: Mapped[str] = mapped_column(String(50), index=True)
    response_json: Mapped[str] = mapped_column(Text)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ttl_until: Mapped[datetime] = mapped_column(DateTime, index=True)


class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ioc: Mapped[str] = mapped_column(String(512), index=True)
    normalized_ioc: Mapped[str] = mapped_column(String(512), index=True)
    ioc_type: Mapped[str] = mapped_column(String(50), index=True)
    score: Mapped[int] = mapped_column(Integer)
    verdict: Mapped[str] = mapped_column(String(50), index=True)
    reason: Mapped[str] = mapped_column(Text)
    sources_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
