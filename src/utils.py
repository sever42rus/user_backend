import toml

from constants import BASE_DIR


def get_project_version() -> str:
    APP_ROOT = BASE_DIR.parent
    with open(f"{APP_ROOT}/pyproject.toml", encoding="utf-8") as f:
        pyproject_data = toml.load(f)
        return pyproject_data["tool"]["poetry"]["version"]
