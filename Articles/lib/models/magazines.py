from ..db.connection import get_connection
from .author import Author
from .article import Article

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self.name, self.category, self.id)
            )
        else:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM magazines WHERE id = ?", (id,)
        ).fetchone()
        conn.close()
        return cls(row['name'], row['category'], row['id']) if row else None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM magazines WHERE name = ?", (name,)
        ).fetchone()
        conn.close()
        return cls(row['name'], row['category'], row['id']) if row else None

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM magazines WHERE category = ?", (category,)
        ).fetchall()
        conn.close()
        return [cls(r['name'], r['category'], r['id']) for r in rows]

    def articles(self):
        return Article.find_by_magazine(self.id)

    def contributors(self):
        conn = get_connection()
        rows = conn.execute("""
            SELECT DISTINCT au.* FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
        """, (self.id,)).fetchall()
        conn.close()
        return [Author(r['name'], r['id']) for r in rows]

    def article_titles(self):
        conn = get_connection()
        rows = conn.execute(
            "SELECT title FROM articles WHERE magazine_id = ?", (self.id,)
        ).fetchall()
        conn.close()
        return [r['title'] for r in rows]

    def contributing_authors(self):
        conn = get_connection()
        rows = conn.execute("""
            SELECT au.*, COUNT(*) as cnt FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
            GROUP BY au.id
            HAVING cnt > 2
        """, (self.id,)).fetchall()
        conn.close()
        return [Author(r['name'], r['id']) for r in rows]
