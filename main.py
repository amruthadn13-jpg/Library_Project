from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT
    )
    """)

    # Insert sample data if empty
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        books = [
            ("Atomic Habits", "James Clear"),
            ("The Alchemist", "Paulo Coelho"),
            ("Rich Dad Poor Dad", "Robert Kiyosaki"),
            ("Ikigai", "Hector Garcia")
        ]
        cursor.executemany("INSERT INTO books (title, author) VALUES (?, ?)", books)

    conn.commit()
    conn.close()

init_db()

# Home
@app.route("/")
def home():
    return render_template("home.html")

# View Books
@app.route("/view")
def view_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    conn.close()

    return render_template("view.html", books=books)

# Search Book
@app.route("/search", methods=["GET", "POST"])
def search_book():
    book = None

    if request.method == "POST":
        title = request.form["title"]

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM books WHERE LOWER(title)=LOWER(?)",
            (title,)
        )

        book = cursor.fetchone()
        conn.close()

    return render_template("search.html", book=book)

app.run(debug=True)
