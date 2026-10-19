"""重启或重建容器不能重置已经保存的工单。"""
import sqlite3

from container_entrypoint import ensure_database


def test_first_start_initializes_database_and_restart_keeps_tickets(tmp_path):
    database = tmp_path / "volume" / "campusfix.db"
    ensure_database(database)
    with sqlite3.connect(database) as conn:
        assert conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0] == 5
        conn.execute("INSERT INTO tickets (title, room, description) VALUES (?, ?, ?)",
                     ("持久化验证", "B202", "重建容器后应保留"))
    before = database.read_bytes()
    ensure_database(database)
    assert database.read_bytes() == before
    with sqlite3.connect(database) as conn:
        assert conn.execute("SELECT title FROM tickets WHERE title = ?", ("持久化验证",)).fetchone()
