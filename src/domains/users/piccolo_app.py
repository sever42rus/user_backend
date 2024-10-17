import os

from piccolo.conf.apps import AppConfig

from domains.users.tables import User

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


APP_CONFIG = AppConfig(
    app_name="users",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "migrations"),
    table_classes=[User],
    migration_dependencies=[],
    commands=[],
)
