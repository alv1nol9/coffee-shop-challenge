import pytest
from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine

@pytest.fixture(autouse=True)
def init_db(tmp_path, monkeypatch):
    # point DB to a temp file
    db_file = tmp_path / "test.db"
    monkeypatch.setattr('lib.db.connection.DB_PATH', str(db_file))
    # create schema and seed
    from scripts.setup_db import setup
    setup()
    yield

def test_author_save_and_find():
    a = Author('Dave')
    a.save()
    fetched = Author.find_by_name('Dave')
    assert fetched.id == a.id

def test_add_article_and_relations():
    a = Author('Eve').save()
    m = Magazine('Science Mag', 'Science').save()
    art = a.add_article(m, 'Quantum Leap')
    assert art.id is not None
    assert any(x.title == 'Quantum Leap' for x in a.articles())
    assert m in a.magazines()
