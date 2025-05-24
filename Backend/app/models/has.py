# app/models/has.py
from sqlalchemy import Column, Integer, ForeignKey, Table
from app.db.base import Base

has = Table(
    "has",
    Base.metadata,
    Column("toilet_id", Integer, ForeignKey("toilet.id"), primary_key=True),
    Column("amenity_id", Integer, ForeignKey("amenity.id"), primary_key=True),
)
