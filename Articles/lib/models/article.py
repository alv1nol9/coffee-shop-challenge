from ..db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        conn = get_connection()
        cur = conn.cursor()
        if self.id:
            cur.execute(
                """
                UPDATE articles
                SET title = ?, author_id = ?, magazine_id = ?
                WHERE id = ?
                """,
                (self.title, self.author_id, self.magazine_id, self.id)
            )
        else:
            cur.execute(
                """
                INSERT INTO articles (title, author_id, magazine_id)
                VALUES (?, ?, ?)
                """,
                (self.title, self.author_id, self.magazine_id)
            )
            self.id = cur.lastrowid
        conn.commit()
        conn.close()
        return self

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM articles WHERE id = ?", (id,)
        ).fetchone()
        conn.close()
        return cls(row["title"], row["author_id"], row["magazine_id"], row["id"]) if row else None

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM articles WHERE title = ?", (title,)
        ).fetchall()
        conn.close()
        return [
            cls(r["title"], r["author_id"], r["magazine_id"], r["id"])
            for r in rows
        ]

    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM articles WHERE author_id = ?", (author_id,)
        ).fetchall()
        conn.close()
        return [
            cls(r["title"], r["author_id"], r["magazine_id"], r["id"])
            for r in rows
        ]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,)
        ).fetchall()
        conn.close()
        return [
            cls(r["title"], r["author_id"], r["magazine_id"], r["id"])
            for r in rows
        ]

    @classmethod
    def authors_for_magazine(cls, magazine_id):
        from .author import Author
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT DISTINCT au.*
            FROM authors au
            JOIN articles a
              ON au.id = a.author_id
            WHERE a.magazine_id = ?
            """,
            (magazine_id,)
        ).fetchall()
        conn.close()
        return [Author(r["name"], r["id"]) for r in rows]

    @classmethod
    def magazines_with_multiple_authors(cls, min_authors=2):
        from .magazine import Magazine
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT m.*, COUNT(DISTINCT a.author_id) AS cnt
            FROM magazines m
            JOIN articles a
              ON m.id = a.magazine_id
            GROUP BY m.id
            HAVING cnt >= ?
            """,
            (min_authors,)
        ).fetchall()
        conn.close()
        return [
            Magazine(r["name"], r["category"], r["id"])
            for r in rows
        ]

    @classmethod
    def article_counts_per_magazine(cls):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT magazine_id, COUNT(*) AS count
            FROM articles
            GROUP BY magazine_id
            """
        ).fetchall()
        conn.close()
        return {r["magazine_id"]: r["count"] for r in rows}

    @classmethod
    def top_author(cls):
        from .author import Author
        conn = get_connection()
        row = conn.execute(
            """
            SELECT author_id, COUNT(*) AS cnt
            FROM articles
            GROUP BY author_id
            ORDER BY cnt DESC
            LIMIT 1
            """
        ).fetchone()
        conn.close()
        return Author.find_by_id(row["author_id"]) if row else None
