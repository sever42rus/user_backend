from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine

from settings import postgres_settings

DB = PostgresEngine(config=postgres_settings.model_dump())

APP_REGISTRY = AppRegistry(
    apps=[
        "domains.update_action.piccolo_app",
        "domains.users.piccolo_app",
    ],
)
