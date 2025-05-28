from ..db.connection import get_connection
from .article import Article

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute(
                "UPDATE authors SET name = ? WHERE id = ?",
                (self.name, self.id)
            )
        else:
            cursor.execute(
                "INSERT INTO authors (name) VALUES (?)",
                (self.name,)
            )
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM authors WHERE id = ?", (id,)
        ).fetchone()
        conn.close()
        return cls(row['name'], row['id']) if row else None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM authors WHERE name = ?", (name,)
        ).fetchone()
        conn.close()
        return cls(row['name'], row['id']) if row else None

    def articles(self):
        return Article.find_by_author(self.id)

    def magazines(self):
        conn = get_connection()
        rows = conn.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,)).fetchall()
        conn.close()
        from .magazine import Magazine
        return [Magazine(row['name'], row['category'], row['id']) for row in rows]

    def add_article(self, magazine, title):
        from .magazine import Magazine
        if isinstance(magazine, Magazine):
            mag_id = magazine.id
        else:
            mag = Magazine.find_by_name(magazine)
            mag_id = mag.id if mag else None

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO articles (title, author_id, magazine_id)
            VALUES (?, ?, ?)
        """, (title, self.id, mag_id))
        conn.commit()
        conn.close()
        return Article(title, self.id, mag_id)

    def topic_areas(self):
        conn = get_connection()
        rows = conn.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,)).fetchall()
        conn.close()
        return [row['category'] for row in rows]
