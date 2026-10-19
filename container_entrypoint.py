"""容器单进程入口：仅首次创建数据库，随后启动 Gunicorn。"""
import os
from pathlib import Path

from app import DATABASE
from init_db import main as initialize_database


def ensure_database(database=DATABASE):
    database = Path(database)
    if not database.exists():
        initialize_database(database)


if __name__ == "__main__":
    ensure_database()
    os.execvp("gunicorn", [
        "gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1",
        "--access-logfile", "-", "--error-logfile", "-", "app:app",
    ])
