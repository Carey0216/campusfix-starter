"""pytest fixtures：使用临时目录中的独立数据库，避免污染开发库"""
import sqlite3

import pytest

import app as app_module


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """为每个测试准备一个独立数据库的 Flask 测试客户端"""
    # 用临时目录中的数据库
    database = tmp_path / "test.db"
    monkeypatch.setitem(app_module.app.config, "DATABASE", str(database))
    monkeypatch.setitem(app_module.app.config, "TESTING", True)

    # 直接按 schema.sql 建空库（不依赖 init_db 的演示数据）
    conn = sqlite3.connect(database)
    try:
        with open(app_module.BASE_DIR / "schema.sql", encoding="utf-8") as f:
            conn.executescript(f.read())
    finally:
        conn.close()

    with app_module.app.test_client() as c:
        yield c
