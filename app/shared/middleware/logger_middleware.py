import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

logger = logging.getLogger("RequestLoggingMiddleware")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    async def dispatch(self, request, call_next):
        await self.set_body(request)
        try:
            json_body = await request.json()

        except Exception:
            json_body = await request.body()

        # log action here
        actions = {
            "create",
            "update",
            "delete",
            "approve",
            "reject",
            "cancel",
            "complete",
            "assign",
            "unassign",
        }

        if any(
            part in actions
            for action in request.url.path.split("/")
            for part in action.split("_")
        ):
            # logger logic
            logger.info(f"{request.method} {request.url.path}")
            logger.info(f"payload: {json_body}")

            # user identity logic
            data = dict(
                ip=request.client.host, path=request.url.path, newValueJson=json_body
            )
            try:
                # YOUR IDENTITY RECORD HERE
                # request.user.id
                pass
            except Exception:
                logger.info("User not found")
                return await call_next(request)

            ## Default identity record
            # logger.info(f"User: {request.user.id}, AuthInfo: {request.auth.scopes}")
            # if request.user.id == '44c6b702-6ea5-4872-b140-3b5e0b22ead6' or request.user.admin:
            #     data['adminId'] = request.user.id
            # elif request.user.agent:
            #     data['agentId'] = request.user.id

            # YOUR LOG ACTION HERE

        return await call_next(request)
