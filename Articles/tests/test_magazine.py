import pytest
from lib.db.connection import get_connection
from lib.models.magazine import Magazine
from lib.models.author import Author

@pytest.fixture(autouse=True)
def init_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test2.db"
    monkeypatch.setattr('lib.db.connection.DB_PATH', str(db_file))
    from scripts.setup_db import setup
    setup()
    yield

def test_magazine_save_and_find():
    m = Magazine('Fun Times', 'Leisure')
    m.save()
    fetched = Magazine.find_by_name('Fun Times')
    assert fetched.id == m.id

def test_contributors_and_titles():
    a1 = Author('X').save()
    a2 = Author('Y').save()
    m = Magazine('Pop Mag', 'Culture').save()
    a1.add_article(m, 'Pop 101')
    a2.add_article(m, 'Pop 202')
    titles = m.article_titles()
    assert 'Pop 101' in titles and 'Pop 202' in titles
    contribs = m.contributors()
    assert any(c.name == 'X' for c in contribs) and any(c.name == 'Y' for c in contribs)
