from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas import search as schemas  # 替換成實際放 Search schema 的檔名

def search_toilets(
    db: Session,
    filters: schemas.Search,
    skip: int = 0,
    limit: int = 100
):
    sql = """
    SELECT t.id, t.building_id, t.floor, t.type, t.title,
           COALESCE(r.review_count, 0) AS review_count,
           COALESCE(r.avg_rating, 0) AS average_rating
    FROM toilet t
    LEFT JOIN (
        SELECT toilet_id,
               COUNT(*) AS review_count,
               AVG(rating) AS avg_rating
        FROM review
        GROUP BY toilet_id
    ) r ON t.id = r.toilet_id
    LEFT JOIN has h ON t.id = h.toilet_id
    WHERE 1=1
    """

    params = {}

    if filters.max_floor is not None:
        sql += " AND t.floor <= :max_floor"
        params["max_floor"] = filters.max_floor

    if filters.min_review_count is not None:
        sql += " AND COALESCE(r.review_count, 0) >= :min_review_count"
        params["min_review_count"] = filters.min_review_count

    if filters.min_average_rating is not None:
        sql += " AND COALESCE(r.avg_rating, 0) >= :min_average_rating"
        params["min_average_rating"] = filters.min_average_rating

    if filters.amenity_id is not None:
        sql += " AND h.amenity_id = :amenity_id"
        params["amenity_id"] = filters.amenity_id

    if filters.amenity_id is not None and filters.amenity_id > 0:
        sql += " AND h.amenity_id = :amenity_id"
        params["amenity_id"] = filters.amenity_id


    sql += " LIMIT :limit OFFSET :skip"
    params["limit"] = limit
    params["skip"] = skip

    query = text(sql)
    result = db.execute(query, params)
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]
