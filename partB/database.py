import sqlite3
from pathlib import Path
from datetime import date

DB_PATH = Path(__file__).with_name("library.db")


def connect_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA busy_timeout = 10000")
    return conn


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Available',
            borrower_name TEXT DEFAULT '',
            issue_date TEXT DEFAULT '',
            due_date TEXT DEFAULT ''
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT NOT NULL,
            member_id TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT DEFAULT '',
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (member_id) REFERENCES members(member_id)
        )
    """)

    cursor.execute("PRAGMA table_info(books)")
    columns = [column[1] for column in cursor.fetchall()]

    for column in ["borrower_name", "issue_date", "due_date"]:
        if column not in columns:
            cursor.execute(
                f"ALTER TABLE books ADD COLUMN {column} TEXT DEFAULT ''"
            )

    conn.commit()
    conn.close()


# BOOK MANAGEMENT

def add_book(book_id, title, author, category):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO books (book_id, title, author, category)
        VALUES (?, ?, ?, ?)
    """, (book_id, title, author, category))

    conn.commit()
    conn.close()


def get_books(search_text=""):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT book_id, title, author, category, status,
               borrower_name, issue_date, due_date
        FROM books
        WHERE book_id LIKE ? OR title LIKE ?
           OR author LIKE ? OR category LIKE ?
        ORDER BY book_id
    """, (
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%"
    ))

    records = cursor.fetchall()
    conn.close()
    return records


def update_book(book_id, title, author, category):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE books
        SET title=?, author=?, category=?
        WHERE book_id=?
    """, (title, author, category, book_id))

    conn.commit()
    result = cursor.rowcount
    conn.close()
    return result


def delete_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM loans
        WHERE book_id=? AND return_date=''
    """, (book_id,))

    active_loan = cursor.fetchone()[0]

    if active_loan:
        conn.close()
        return 0

    cursor.execute(
        "DELETE FROM books WHERE book_id=?",
        (book_id,)
    )

    result = cursor.rowcount
    conn.commit()
    conn.close()
    return result


# MEMBER MANAGEMENT

def add_member(member_id, name, phone, email):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO members (member_id, name, phone, email)
        VALUES (?, ?, ?, ?)
    """, (member_id, name, phone, email))

    conn.commit()
    conn.close()


def get_members(search_text=""):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT member_id, name, phone, email
        FROM members
        WHERE member_id LIKE ? OR name LIKE ? OR phone LIKE ?
        ORDER BY name
    """, (
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%"
    ))

    records = cursor.fetchall()
    conn.close()
    return records


def delete_member(member_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM loans
        WHERE member_id=? AND return_date=''
    """, (member_id,))

    active_loan = cursor.fetchone()[0]

    if active_loan:
        conn.close()
        return 0

    cursor.execute(
        "DELETE FROM members WHERE member_id=?",
        (member_id,)
    )

    result = cursor.rowcount
    conn.commit()
    conn.close()
    return result


# ISSUE AND RETURN BOOKS

def issue_book(book_id, member_id, issue_date, due_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status FROM books WHERE book_id=?
    """, (book_id,))

    book = cursor.fetchone()

    if not book or book[0] != "Available":
        conn.close()
        return False

    cursor.execute("""
        SELECT name FROM members WHERE member_id=?
    """, (member_id,))

    member = cursor.fetchone()

    if not member:
        conn.close()
        return False

    cursor.execute("""
        INSERT INTO loans
        (book_id, member_id, issue_date, due_date)
        VALUES (?, ?, ?, ?)
    """, (book_id, member_id, issue_date, due_date))

    cursor.execute("""
        UPDATE books
        SET status='Borrowed',
            borrower_name=?,
            issue_date=?,
            due_date=?
        WHERE book_id=?
    """, (member[0], issue_date, due_date, book_id))

    conn.commit()
    conn.close()
    return True


def return_book(book_id, member_id, return_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT loan_id FROM loans
        WHERE book_id=?
          AND member_id=?
          AND return_date=''
        ORDER BY loan_id DESC
        LIMIT 1
    """, (book_id, member_id))

    loan = cursor.fetchone()

    if not loan:
        conn.close()
        return False

    cursor.execute("""
        UPDATE loans
        SET return_date=?
        WHERE loan_id=?
    """, (return_date, loan[0]))

    cursor.execute("""
        UPDATE books
        SET status='Available',
            borrower_name='',
            issue_date='',
            due_date=''
        WHERE book_id=?
    """, (book_id,))

    conn.commit()
    conn.close()
    return True


# BORROWING HISTORY AND OVERDUE BOOKS

def get_borrowing_history():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT loans.loan_id, books.book_id, books.title,
               members.member_id, members.name,
               loans.issue_date, loans.due_date,
               loans.return_date
        FROM loans
        JOIN books ON loans.book_id = books.book_id
        JOIN members ON loans.member_id = members.member_id
        ORDER BY loans.loan_id DESC
    """)

    records = cursor.fetchall()
    conn.close()
    return records


def get_overdue_books():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT books.book_id, books.title, members.name,
               loans.issue_date, loans.due_date
        FROM loans
        JOIN books ON loans.book_id = books.book_id
        JOIN members ON loans.member_id = members.member_id
        WHERE loans.return_date=''
          AND loans.due_date < ?
        ORDER BY loans.due_date
    """, (date.today().isoformat(),))

    records = cursor.fetchall()
    conn.close()
    return records


# DASHBOARD COUNTS

def get_book_counts():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM books WHERE status='Available'
    """)
    available = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM books WHERE status='Borrowed'
    """)
    borrowed = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM loans
        WHERE return_date='' AND due_date < ?
    """, (date.today().isoformat(),))
    overdue = cursor.fetchone()[0]

    conn.close()
    return total, available, borrowed, overdue