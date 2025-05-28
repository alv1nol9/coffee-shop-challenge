import pytest
from lib.db.connection import get_connection
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

@pytest.fixture(autouse=True)
def init_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test3.db"
    monkeypatch.setattr('lib.db.connection.DB_PATH', str(db_file))
    from scripts.setup_db import setup
    setup()
    yield

def test_article_save_and_find():
    a = Author('Z').save()
    m = Magazine('Daily', 'News').save()
    art = Article('Headline', a.id, m.id).save()
    fetched = Article.find_by_id(art.id)
    assert fetched.title == 'Headline'

def test_class_queries():
    a = Author('W').save()
    m1 = Magazine('M1', 'Cat').save()
    m2 = Magazine('M2', 'Cat').save()
    a.add_article(m1, 'A1')
    a.add_article(m2, 'A2')
    by_author = Article.find_by_author(a.id)
    assert len(by_author) == 2
    top = Article.top_author()
    assert top.id == a.id
