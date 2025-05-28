from .connection import get_connection

def seed():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")

    # Seed authors
    authors = ['Alice', 'Bob', 'Carol']
    for name in authors:
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))

    # Seed magazines
    mags = [
        ('Tech Today', 'Technology'),
        ('Health Weekly', 'Health'),
        ('Travelogue', 'Travel')
    ]
    for name, cat in mags:
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)",
            (name, cat)
        )

    # Seed articles
    sample = [
        ('AI Revolution', 1, 1),
        ('Deep Health', 2, 2),
        ('Safari Tips', 3, 3),
        ('Cloud Computing', 1, 1),
        ('Vegan Life', 1, 2),
    ]
    for title, a_id, m_id in sample:
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, a_id, m_id)
        )

    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed()
    print("Database seeded.")
