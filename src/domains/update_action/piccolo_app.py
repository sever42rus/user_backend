import os

from piccolo.conf.apps import AppConfig

from domains.update_action.tables import UpdateAction

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


APP_CONFIG = AppConfig(
    app_name="update_action",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "migrations"),
    table_classes=[UpdateAction],
    migration_dependencies=[],
    commands=[],
)
