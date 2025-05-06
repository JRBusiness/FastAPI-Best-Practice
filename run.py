import contextlib
import uuid

import uvicorn
from redis_om import Migrator
from sqlalchemy.exc import PendingRollbackError
from app.api.search.schemas import AccountModel
from app.endpoint.build_routes import add_routes
from redis_om.model import NotFoundError

from config.settings import Settings

app = add_routes()


def main():
    try:
        Migrator().run()

        with contextlib.suppress(NotFoundError):
            list_active_session = AccountModel.all_pks()
            if not list_active_session:
                account_model = AccountModel(
                    pk=str(uuid.uuid4()),
                    name="Account Status",
                    token="",
                    session_token="",
                    code="",
                    in_use=0,
                )
                account_model.save()
        uvicorn.run(
            "app:app",
            host=Settings.api_host,
            port=int(Settings.api_port),
            workers=5,
            # ssl_keyfile="certs/client.key",
            # ssl_certfile="certs/client.pem",
        )
    except PendingRollbackError as e:
        print(f"PendingRollBackError detected with message {e}")
        with open("Restart_error.txt", "a") as f:
            f.write(f"{e}'\n\n'")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
