import os
from sys import stdout
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware, db
from redis_om import get_redis_connection
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import RedirectResponse
from app.shared.bases.base_model import Base, ModelMixin
from app.shared.middleware.auth import JWTBearer
from config.settings import Settings
from loguru import logger


    
host = Settings.omni_host
port = Settings.omni_port
logger.configure(
    handlers=[
        dict(
            sink="logs/app.log",
            level="TRACE",
            format="{time} {level} {message} {file} {line} ",
            backtrace=True,
            diagnose=True,
            serialize=True,
            catch=True,
            enqueue=True,
        ),
        dict(
            sink=stdout,
            level="TRACE",
            format="{time} {level} {message} {file} {line}",
            backtrace=True,
            diagnose=True,
            serialize=True,
            catch=True,
            enqueue=True,
        ),
    ],
)

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    DBSessionMiddleware,
    db_url=Settings.db_url,
    engine_args={"pool_size": 100000, "max_overflow": 10000},
)
app.add_middleware(AuthenticationMiddleware, backend=JWTBearer())
app.build_middleware_stack()

with db():
    ModelMixin.set_session(db.session)

base_dir = f"{os.path.dirname(os.path.abspath(__file__))}"


redis = get_redis_connection()

app.build_middleware_stack()


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")
