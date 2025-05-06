import json
from typing import Optional

from sqlalchemy import asc, desc


async def common_parameters(
    filter_params: Optional[str] = None,
    sort: Optional[str] = None,
    direction: Optional[str] = None,
):
    params = {}
    if filter_params:
        params["filter_params"] = json.loads(filter_params)
    if sort:
        params["sort"] = sort
        params["direction"] = "desc"
        if direction:
            params["direction"] = direction

    return params


def filter_queries(db_query, db_model, common_params: dict):
    query = db_query
    if common_params.get("filter_params"):
        filter_params = common_params["filter_params"]
        for attr in [x for x in filter_params if filter_params[x] is not None]:
            if attr == "is_like":
                continue
            if filter_params.get("is_like"):
                query = query.filter(
                    getattr(db_model, attr).like(f"{filter_params[attr]}%")
                )
            else:
                query = query.filter(getattr(db_model, attr) == filter_params[attr])
    if common_params.get("sort"):
        sort = common_params["sort"]
        direction = common_params["direction"]
        if direction == "asc":
            query = query.order_by(asc(getattr(db_model, sort)))
        elif direction == "desc":
            query = query.order_by(desc(getattr(db_model, sort)))

    return query
