from fastapi import FastAPI

from app import app
from app.endpoint.urls import URLs


def add_routes() -> FastAPI:
    """
    Generic Method to find and activate all http routes
    :return:
    """
    for route in URLs.include:
        exec(f"from app.api.{route}.views import router as {route}")
        app.include_router(eval(route))
    # use_route_names_as_operation_ids(app)
    return app
