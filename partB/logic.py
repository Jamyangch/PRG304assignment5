import database
from datetime import date, datetime


class LibraryLogic:

    def __init__(self):
        database.create_table()

    # BOOK MANAGEMENT

    def add_book(self, book_id, title, author, category):
        if not all([book_id, title, author, category]):
            return False, "Please fill in all book details."

        try:
            database.add_book(book_id, title, author, category)
            return True, "Book added successfully."
        except Exception as error:
            if "UNIQUE constraint failed" in str(error):
                return False, "This Book ID already exists."
            return False, f"Unable to add book: {error}"

    def get_books(self, search_text=""):
        return database.get_books(search_text)

    def update_book(self, book_id, title, author, category):
        if not all([book_id, title, author, category]):
            return False, "Please fill in all book details."

        try:
            result = database.update_book(
                book_id, title, author, category
            )
            if result:
                return True, "Book updated successfully."
            return False, "Book not found."
        except Exception as error:
            return False, f"Unable to update book: {error}"

    def delete_book(self, book_id):
        if not book_id:
            return False, "Please select a book first."

        result = database.delete_book(book_id)

        if result:
            return True, "Book deleted successfully."
        return False, "Book not found or has an active borrowing record."

    # MEMBER MANAGEMENT

    def add_member(self, member_id, name, phone, email):
        if not all([member_id, name, phone]):
            return False, "Member ID, name and phone are required."

        try:
            database.add_member(member_id, name, phone, email)
            return True, "Member registered successfully."
        except Exception as error:
            if "UNIQUE constraint failed" in str(error):
                return False, "This Member ID already exists."
            return False, f"Unable to register member: {error}"

    def get_members(self, search_text=""):
        return database.get_members(search_text)

    def delete_member(self, member_id):
        if not member_id:
            return False, "Please select a member first."

        result = database.delete_member(member_id)

        if result:
            return True, "Member deleted successfully."
        return False, "Member not found or has an active borrowing record."

    # ISSUE BOOK

    def issue_book(self, book_id, member_id, due_date):
        if not all([book_id, member_id, due_date]):
            return False, "Please complete all issue details."

        try:
            due = datetime.strptime(due_date, "%Y-%m-%d").date()

            if due <= date.today():
                return False, "Due date must be after today's date."

            issue_date = date.today().isoformat()

            result = database.issue_book(
                book_id, member_id, issue_date, due.isoformat()
            )

            if result:
                return True, "Book issued successfully."

            return False, "Book is unavailable or member does not exist."

        except ValueError:
            return False, "Please enter the date in YYYY-MM-DD format."
        except Exception as error:
            return False, f"Unable to issue book: {error}"

    # RETURN BOOK

    def return_book(self, book_id, member_id):
        if not book_id or not member_id:
            return False, "Please enter both Book ID and Member ID."

        result = database.return_book(
            book_id,
            member_id,
            date.today().isoformat()
        )

        if result:
            return True, "Book returned successfully."

        return False, "No active borrowing record found for this Book ID and Member ID."

    # SEARCH AND REPORTS

    def get_borrowing_history(self):
        return database.get_borrowing_history()

    def get_overdue_books(self):
        return database.get_overdue_books()

    def get_counts(self):
        return database.get_book_counts()