class URLs:
    """
    Generic method to create routers in FastAPI so they are added to the swagger doc.
    To use, add the route name as a string to the include list and your route will be built.
    """

    include = [
        "admin",
        "auth",
        "users",
    ]
