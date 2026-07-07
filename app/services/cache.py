import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.config import settings
from app.models import IOCCache


def get_cached_result(db: Session, ioc: str, source: str):
    row = (
        db.query(IOCCache)
        .filter(IOCCache.ioc == ioc, IOCCache.source == source, IOCCache.ttl_until > datetime.utcnow())
        .order_by(IOCCache.fetched_at.desc())
        .first()
    )
    if not row:
        return None
    return json.loads(row.response_json)


def set_cached_result(db: Session, ioc: str, ioc_type: str, source: str, data: dict):
    now = datetime.utcnow()
    row = IOCCache(
        ioc=ioc,
        ioc_type=ioc_type,
        source=source,
        response_json=json.dumps(data, default=str),
        fetched_at=now,
        ttl_until=now + timedelta(hours=settings.cache_ttl_hours),
    )
    db.add(row)
    db.commit()
