
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QStackedWidget, QHeaderView, QMessageBox,
    QDateEdit, QFrame
)
from PyQt6.QtCore import (
    Qt, QDate, QPropertyAnimation,
    QEasingCurve, QPoint
)
from PyQt6.QtGui import QAction

from logic import LibraryLogic


class LibraryWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.logic = LibraryLogic()
        self.flower_animations = []

        self.setWindowTitle("Library Book Management System")
        self.setMinimumSize(1100, 700)

        self.create_interface()
        self.apply_style()
        self.refresh_all()

    # MAIN INTERFACE

    def create_interface(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # SIDEBAR

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(15, 25, 15, 20)
        side_layout.setSpacing(12)

        logo = QLabel("LIBRARY")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("BOOK MANAGEMENT")
        subtitle.setObjectName("sidebarSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        side_layout.addWidget(logo)
        side_layout.addWidget(subtitle)
        side_layout.addSpacing(25)

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Book Management", self.show_books),
            ("Member Management", self.show_members),
            ("Issue & Return Books", self.show_issue),
            ("Borrowing History", self.show_history),
            ("Overdue Books", self.show_overdue)
        ]

        for text, function in buttons:
            button = QPushButton(text)
            button.setObjectName("navButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(function)
            side_layout.addWidget(button)

        side_layout.addStretch()

        footer = QLabel("Library Management System")
        footer.setObjectName("sidebarFooter")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side_layout.addWidget(footer)

        # MAIN CONTENT

        self.stack = QStackedWidget()

        self.create_dashboard_page()
        self.create_books_page()
        self.create_members_page()
        self.create_issue_page()
        self.create_history_page()
        self.create_overdue_page()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

        self.create_menu()

    # MENU BAR

    def create_menu(self):

        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        refresh_action = QAction("Refresh Data", self)
        refresh_action.triggered.connect(self.refresh_all)
        file_menu.addAction(refresh_action)

        records_menu = menu.addMenu("Records")

        history_action = QAction("Borrowing History", self)
        history_action.triggered.connect(self.show_history)
        records_menu.addAction(history_action)

        overdue_action = QAction("Overdue Books", self)
        overdue_action.triggered.connect(self.show_overdue)
        records_menu.addAction(overdue_action)

        help_menu = menu.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        exit_menu = menu.addMenu("Exit")

        exit_action = QAction("Close Application", self)
        exit_action.triggered.connect(self.close)
        exit_menu.addAction(exit_action)

    # COMMON PAGE DESIGN

    def create_page(self, title, description):

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        heading = QLabel(title)
        heading.setObjectName("pageTitle")

        details = QLabel(description)
        details.setObjectName("pageDescription")

        layout.addWidget(heading)
        layout.addWidget(details)

        return page, layout

    def create_table(self, headers):

        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        table.setAlternatingRowColors(True)
        table.setMinimumHeight(250)

        return table

    def fill_table(self, table, records):

        table.setRowCount(0)

        for row_data in records:
            row = table.rowCount()
            table.insertRow(row)

            for column, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )
                table.setItem(row, column, item)

    def create_action_button(self, text, function):

        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(function)

        return button

    # DASHBOARD

    def create_dashboard_page(self):

        page, layout = self.create_page(
            "Dashboard",
            "Overview of your library activities and records."
        )

        # WELCOME BANNER

        banner = QFrame()
        banner.setObjectName("dashboardBanner")
        banner.setMinimumHeight(145)

        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(25, 25, 25, 25)

        welcome = QLabel("Welcome to Library!")
        welcome.setObjectName("bannerTitle")

        message = QLabel(
            "A happy place to manage books, members and borrowing records."
        )
        message.setObjectName("bannerSubtitle")

        banner_layout.addWidget(welcome)
        banner_layout.addWidget(message)

        # FLOATING FLOWERS

        flowers = ["🌸", "🌼", "🌷", "🌺", "🌸"]

        flower_positions = [
            (550, 15),
            (610, 55),
            (670, 20),
            (730, 60),
            (770, 15)
        ]

        for i, flower in enumerate(flowers):

            flower_label = QLabel(flower, banner)

            flower_label.setStyleSheet(
                "font-size: 27px; background: transparent;"
            )

            flower_label.setFixedSize(40, 40)

            x, y = flower_positions[i]
            flower_label.move(x, y)

            animation = QPropertyAnimation(
                flower_label, b"pos", self
            )

            animation.setDuration(1800 + (i * 300))
            animation.setStartValue(QPoint(x, y))
            animation.setEndValue(QPoint(x + 8, y + 22))

            animation.setEasingCurve(
                QEasingCurve.Type.InOutSine
            )

            animation.setLoopCount(-1)
            animation.start()

            self.flower_animations.append(animation)

        layout.addWidget(banner)

        # STATISTIC CARDS

        cards_layout = QGridLayout()
        cards_layout.setSpacing(15)

        self.total_card = self.create_card(
            "TOTAL BOOKS", "0", "totalCard"
        )

        self.available_card = self.create_card(
            "AVAILABLE BOOKS", "0", "availableCard"
        )

        self.borrowed_card = self.create_card(
            "BORROWED BOOKS", "0", "borrowedCard"
        )

        self.overdue_card = self.create_card(
            "OVERDUE BOOKS", "0", "overdueCard"
        )

        cards_layout.addWidget(self.total_card, 0, 0)
        cards_layout.addWidget(self.available_card, 0, 1)
        cards_layout.addWidget(self.borrowed_card, 1, 0)
        cards_layout.addWidget(self.overdue_card, 1, 1)

        layout.addLayout(cards_layout)

        # RECENT BORROWING RECORDS

        recent_title = QLabel("Recent Borrowing Records")
        recent_title.setObjectName("sectionTitle")

        layout.addWidget(recent_title)

        self.dashboard_table = self.create_table([
            "Book ID", "Book Title", "Member Name",
            "Issue Date", "Due Date", "Return Date"
        ])

        layout.addWidget(self.dashboard_table)
        layout.addStretch()

        self.stack.addWidget(page)

    def create_card(self, title, value, object_name):

        card = QFrame()
        card.setObjectName("dashboardCard")
        card.setMinimumHeight(105)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 12, 18, 12)

        heading = QLabel(title)
        heading.setObjectName("cardTitle")

        number = QLabel(value)
        number.setObjectName("cardNumber")

        card_layout.addWidget(heading)
        card_layout.addWidget(number)

        if object_name == "totalCard":
            self.total_number = number

        elif object_name == "availableCard":
            self.available_number = number

        elif object_name == "borrowedCard":
            self.borrowed_number = number

        elif object_name == "overdueCard":
            self.overdue_number = number

        return card

    def refresh_dashboard(self):

        total, available, borrowed, overdue = (
            self.logic.get_counts()
        )

        self.total_number.setText(str(total))
        self.available_number.setText(str(available))
        self.borrowed_number.setText(str(borrowed))
        self.overdue_number.setText(str(overdue))

        history = self.logic.get_borrowing_history()

        recent_records = []

        for record in history[:5]:

            recent_records.append([
                record[1],
                record[2],
                record[4],
                record[5],
                record[6],
                record[7] if record[7] else "Not returned"
            ])

        self.fill_table(
            self.dashboard_table, recent_records
        )

    # BOOK MANAGEMENT

    def create_books_page(self):

        page, layout = self.create_page(
            "Book Management",
            "Add, update, delete and search library books."
        )

        form_layout = QGridLayout()
        form_layout.setSpacing(10)

        self.book_id = QLineEdit()
        self.book_id.setPlaceholderText("Enter Book ID")

        self.book_title = QLineEdit()
        self.book_title.setPlaceholderText("Enter Book Title")

        self.book_author = QLineEdit()
        self.book_author.setPlaceholderText("Enter Author Name")

        # CATEGORY DROPDOWN

        self.book_category = QComboBox()

        self.book_category.addItems([
            "Select Category",
            "Fiction",
            "Non-Fiction",
            "Science",
            "Technology",
            "History",
            "Mathematics",
            "Literature",
            "Education",
            "Others"
        ])

        form_layout.addWidget(QLabel("Book ID"), 0, 0)
        form_layout.addWidget(self.book_id, 0, 1)

        form_layout.addWidget(QLabel("Book Title"), 0, 2)
        form_layout.addWidget(self.book_title, 0, 3)

        form_layout.addWidget(QLabel("Author"), 1, 0)
        form_layout.addWidget(self.book_author, 1, 1)

        form_layout.addWidget(QLabel("Category"), 1, 2)
        form_layout.addWidget(self.book_category, 1, 3)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        add_button = self.create_action_button(
            "Add Book", self.add_book
        )

        update_button = self.create_action_button(
            "Update Book", self.update_book
        )

        delete_button = self.create_action_button(
            "Delete Book", self.delete_book
        )

        clear_button = self.create_action_button(
            "Clear Fields", self.clear_book_fields
        )

        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        self.book_search = QLineEdit()
        self.book_search.setPlaceholderText(
            "Search by Book ID, title, author or category..."
        )

        self.book_search.textChanged.connect(
            self.load_books
        )

        layout.addWidget(self.book_search)

        self.book_table = self.create_table([
            "Book ID", "Title", "Author", "Category",
            "Status", "Borrower", "Issue Date", "Due Date"
        ])

        self.book_table.itemSelectionChanged.connect(
            self.select_book
        )

        layout.addWidget(self.book_table)
        layout.addStretch()

        self.stack.addWidget(page)

    def add_book(self):

        book_id = self.book_id.text().strip()
        title = self.book_title.text().strip()
        author = self.book_author.text().strip()

        category = self.book_category.currentText()

        if category == "Select Category":
            category = ""

        success, message = self.logic.add_book(
            book_id, title, author, category
        )

        self.show_message(success, message)

        if success:
            self.clear_book_fields()
            self.refresh_all()

    def update_book(self):

        book_id = self.book_id.text().strip()
        title = self.book_title.text().strip()
        author = self.book_author.text().strip()

        category = self.book_category.currentText()

        if category == "Select Category":
            category = ""

        success, message = self.logic.update_book(
            book_id, title, author, category
        )

        self.show_message(success, message)

        if success:
            self.refresh_all()

    def delete_book(self):

        book_id = self.book_id.text().strip()

        if not book_id:
            self.show_message(
                False, "Please select a book first."
            )
            return

        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this book?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:

            success, message = self.logic.delete_book(book_id)
            self.show_message(success, message)

            if success:
                self.clear_book_fields()
                self.refresh_all()

    def clear_book_fields(self):

        self.book_id.clear()
        self.book_title.clear()
        self.book_author.clear()
        self.book_category.setCurrentIndex(0)

    def select_book(self):

        row = self.book_table.currentRow()

        if row < 0:
            return

        self.book_id.setText(
            self.book_table.item(row, 0).text()
        )

        self.book_title.setText(
            self.book_table.item(row, 1).text()
        )

        self.book_author.setText(
            self.book_table.item(row, 2).text()
        )

        self.book_category.setCurrentText(
            self.book_table.item(row, 3).text()
        )

    def load_books(self, *args):

        if hasattr(self, "book_table"):

            records = self.logic.get_books(
                self.book_search.text()
            )

            self.fill_table(self.book_table, records)

    # MEMBER MANAGEMENT

    def create_members_page(self):

        page, layout = self.create_page(
            "Member Management",
            "Register members and manage their information."
        )

        form_layout = QGridLayout()

        self.member_id = QLineEdit()
        self.member_id.setPlaceholderText("Enter Member ID")

        self.member_name = QLineEdit()
        self.member_name.setPlaceholderText("Enter Member Name")

        self.member_phone = QLineEdit()
        self.member_phone.setPlaceholderText("Enter Phone Number")

        self.member_email = QLineEdit()
        self.member_email.setPlaceholderText(
            "Enter Email (Optional)"
        )

        form_layout.addWidget(QLabel("Member ID"), 0, 0)
        form_layout.addWidget(self.member_id, 0, 1)

        form_layout.addWidget(QLabel("Member Name"), 0, 2)
        form_layout.addWidget(self.member_name, 0, 3)

        form_layout.addWidget(QLabel("Phone"), 1, 0)
        form_layout.addWidget(self.member_phone, 1, 1)

        form_layout.addWidget(QLabel("Email"), 1, 2)
        form_layout.addWidget(self.member_email, 1, 3)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        add_button = self.create_action_button(
            "Register Member", self.add_member
        )

        delete_button = self.create_action_button(
            "Delete Member", self.delete_member
        )

        clear_button = self.create_action_button(
            "Clear Fields", self.clear_member_fields
        )

        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        self.member_search = QLineEdit()
        self.member_search.setPlaceholderText(
            "Search by Member ID, name or phone..."
        )

        self.member_search.textChanged.connect(
            self.load_members
        )

        layout.addWidget(self.member_search)

        self.member_table = self.create_table([
            "Member ID", "Name", "Phone", "Email"
        ])

        self.member_table.itemSelectionChanged.connect(
            self.select_member
        )

        layout.addWidget(self.member_table)
        layout.addStretch()

        self.stack.addWidget(page)

    def add_member(self):

        member_id = self.member_id.text().strip()
        name = self.member_name.text().strip()
        phone = self.member_phone.text().strip()
        email = self.member_email.text().strip()

        success, message = self.logic.add_member(
            member_id, name, phone, email
        )

        self.show_message(success, message)

        if success:
            self.clear_member_fields()
            self.refresh_all()

    def delete_member(self):

        member_id = self.member_id.text().strip()

        if not member_id:
            self.show_message(
                False, "Please select a member first."
            )
            return

        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this member?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:

            success, message = self.logic.delete_member(
                member_id
            )

            self.show_message(success, message)

            if success:
                self.clear_member_fields()
                self.refresh_all()

    def clear_member_fields(self):

        self.member_id.clear()
        self.member_name.clear()
        self.member_phone.clear()
        self.member_email.clear()

    def select_member(self):

        row = self.member_table.currentRow()

        if row < 0:
            return

        self.member_id.setText(
            self.member_table.item(row, 0).text()
        )

        self.member_name.setText(
            self.member_table.item(row, 1).text()
        )

        self.member_phone.setText(
            self.member_table.item(row, 2).text()
        )

        self.member_email.setText(
            self.member_table.item(row, 3).text()
        )

    def load_members(self, *args):

        if hasattr(self, "member_table"):

            records = self.logic.get_members(
                self.member_search.text()
            )

            self.fill_table(self.member_table, records)

    # ISSUE AND RETURN BOOK

    def create_issue_page(self):

        page, layout = self.create_page(
            "Issue & Return Books",
            "Issue available books to registered members or record returns."
        )

        form_layout = QGridLayout()
        form_layout.setSpacing(15)

        self.issue_book_id = QLineEdit()
        self.issue_book_id.setPlaceholderText("Enter Book ID")

        self.issue_member_id = QLineEdit()
        self.issue_member_id.setPlaceholderText("Enter Member ID")

        self.due_date = QDateEdit()
        self.due_date.setCalendarPopup(True)
        self.due_date.setDate(
            QDate.currentDate().addDays(14)
        )
        self.due_date.setDisplayFormat("yyyy-MM-dd")

        form_layout.addWidget(QLabel("Book ID"), 0, 0)
        form_layout.addWidget(self.issue_book_id, 0, 1)

        form_layout.addWidget(QLabel("Member ID"), 1, 0)
        form_layout.addWidget(self.issue_member_id, 1, 1)

        form_layout.addWidget(QLabel("Due Date"), 2, 0)
        form_layout.addWidget(self.due_date, 2, 1)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        issue_button = self.create_action_button(
            "Issue Book", self.issue_book
        )

        return_button = self.create_action_button(
            "Return Book", self.return_book
        )

        clear_button = self.create_action_button(
            "Clear Fields", self.clear_issue_fields
        )

        button_layout.addWidget(issue_button)
        button_layout.addWidget(return_button)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        instruction = QLabel(
            "Select a book from the table below to fill its Book ID."
        )

        instruction.setObjectName("pageDescription")
        layout.addWidget(instruction)

        self.issue_table = self.create_table([
            "Book ID", "Title", "Author", "Category",
            "Status", "Borrower", "Issue Date", "Due Date"
        ])

        self.issue_table.itemSelectionChanged.connect(
            self.select_issue_book
        )

        layout.addWidget(self.issue_table)
        layout.addStretch()

        self.stack.addWidget(page)

    def issue_book(self):

        book_id = self.issue_book_id.text().strip()
        member_id = self.issue_member_id.text().strip()

        due_date = self.due_date.date().toString(
            "yyyy-MM-dd"
        )

        success, message = self.logic.issue_book(
            book_id, member_id, due_date
        )

        self.show_message(success, message)

        if success:
            self.clear_issue_fields()
            self.refresh_all()

    # CORRECTED RETURN BOOK FUNCTION

    def return_book(self):

        book_id = self.issue_book_id.text().strip()
        member_id = self.issue_member_id.text().strip()

        success, message = self.logic.return_book(
            book_id, member_id
        )

        self.show_message(success, message)

        if success:
            self.clear_issue_fields()
            self.refresh_all()

    def clear_issue_fields(self):

        self.issue_book_id.clear()
        self.issue_member_id.clear()

        self.due_date.setDate(
            QDate.currentDate().addDays(14)
        )

    def select_issue_book(self):

        row = self.issue_table.currentRow()

        if row < 0:
            return

        self.issue_book_id.setText(
            self.issue_table.item(row, 0).text()
        )

    def load_issue_table(self):

        records = self.logic.get_books()
        self.fill_table(self.issue_table, records)

    # BORROWING HISTORY

    def create_history_page(self):

        page, layout = self.create_page(
            "Borrowing History",
            "View all previous and current borrowing records."
        )

        self.history_table = self.create_table([
            "Loan ID", "Book ID", "Book Title",
            "Member ID", "Member Name",
            "Issue Date", "Due Date", "Return Date"
        ])

        layout.addWidget(self.history_table)
        layout.addStretch()

        self.stack.addWidget(page)

    def load_history(self):

        records = self.logic.get_borrowing_history()

        self.fill_table(self.history_table, records)

    # OVERDUE BOOKS

    def create_overdue_page(self):

        page, layout = self.create_page(
            "Overdue Books",
            "View books that have passed their expected return date."
        )

        self.overdue_table = self.create_table([
            "Book ID", "Book Title", "Member Name",
            "Issue Date", "Due Date"
        ])

        layout.addWidget(self.overdue_table)
        layout.addStretch()

        self.stack.addWidget(page)

    def load_overdue(self):

        records = self.logic.get_overdue_books()

        self.fill_table(self.overdue_table, records)

    # NAVIGATION

    def show_dashboard(self):

        self.stack.setCurrentIndex(0)
        self.refresh_dashboard()

    def show_books(self):

        self.stack.setCurrentIndex(1)
        self.load_books()

    def show_members(self):

        self.stack.setCurrentIndex(2)
        self.load_members()

    def show_issue(self):

        self.stack.setCurrentIndex(3)
        self.load_issue_table()

    def show_history(self):

        self.stack.setCurrentIndex(4)
        self.load_history()

    def show_overdue(self):

        self.stack.setCurrentIndex(5)
        self.load_overdue()

    # REFRESH ALL DATA

    def refresh_all(self):

        if hasattr(self, "book_table"):
            self.load_books()

        if hasattr(self, "member_table"):
            self.load_members()

        if hasattr(self, "issue_table"):
            self.load_issue_table()

        if hasattr(self, "history_table"):
            self.load_history()

        if hasattr(self, "overdue_table"):
            self.load_overdue()

        if hasattr(self, "dashboard_table"):
            self.refresh_dashboard()

    # MESSAGES

    def show_message(self, success, message):

        if success:
            QMessageBox.information(
                self, "Success", message
            )
        else:
            QMessageBox.warning(
                self, "Information", message
            )

    def show_about(self):

        QMessageBox.information(
            self,
            "About",
            "Library Book Management System\n\n"
            "This application helps manage books, members, "
            "book issues, returns and borrowing records."
        )

    # STYLING

    def apply_style(self):

        self.setStyleSheet("""
            QMainWindow {
                background-color: #fff7fb;
            }

            QWidget {
                font-family: Arial;
                font-size: 13px;
                color: #263449;
            }

            #sidebar {
                background-color: #142b4a;
            }

            #logo {
                color: white;
                font-size: 25px;
                font-weight: bold;
            }

            #sidebarSubtitle {
                color: #b9c9dd;
                font-size: 10px;
                letter-spacing: 2px;
            }

            #sidebarFooter {
                color: #a9bad0;
                font-size: 10px;
            }

            QPushButton#navButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 12px;
                border: none;
                border-radius: 6px;
                font-size: 13px;
            }

            QPushButton#navButton:hover {
                background-color: #29486d;
            }

            QPushButton {
                background-color: #c66d9d;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #a94f83;
            }

            QLineEdit, QDateEdit, QComboBox {
                background-color: white;
                border: 1px solid #e7c9da;
                border-radius: 5px;
                padding: 9px;
                min-height: 20px;
            }

            QLineEdit:focus, QDateEdit:focus,
            QComboBox:focus {
                border: 1px solid #c66d9d;
            }

            QComboBox::drop-down {
                border: none;
                width: 25px;
            }

            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #f8e5ef;
                selection-color: #874b70;
            }

            QTableWidget {
                background-color: white;
                alternate-background-color: #fff4f9;
                border: 1px solid #f0dce7;
                border-radius: 6px;
                gridline-color: #f2e5ec;
            }

            QHeaderView::section {
                background-color: #f8e5ef;
                color: #874b70;
                padding: 10px;
                border: none;
                font-weight: bold;
            }

            #pageTitle {
                color: #874b70;
                font-size: 25px;
                font-weight: bold;
            }

            #pageDescription {
                color: #967b8b;
                font-size: 12px;
            }

            #dashboardBanner {
                background-color: #f8dce8;
                border: 2px solid #f2c4d8;
                border-radius: 18px;
            }

            #bannerTitle {
                color: #874b70;
                font-size: 25px;
                font-weight: bold;
            }

            #bannerSubtitle {
                color: #966b83;
                font-size: 13px;
            }

            #dashboardCard {
                background-color: #fffafd;
                border: 1px solid #f3d5e4;
                border-radius: 15px;
            }

            #cardTitle {
                color: #a47791;
                font-size: 11px;
                font-weight: bold;
            }

            #cardNumber {
                color: #a94f83;
                font-size: 30px;
                font-weight: bold;
            }

            #sectionTitle {
                color: #a65380;
                font-size: 17px;
                font-weight: bold;
            }

            QMenuBar {
                background-color: white;
                color: #263449;
                padding: 5px;
            }

            QMenuBar::item:selected {
                background-color: #f8e5ef;
            }

            QMenu {
                background-color: white;
                border: 1px solid #f0dce7;
            }

            QMenu::item:selected {
                background-color: #f8e5ef;
            }
        """)

    # EXIT CONFIRMATION

    def closeEvent(self, event):

        answer = QMessageBox.question(
            self,
            "Exit Application",
            "Are you sure you want to close the Library System?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


# RUN APPLICATION

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = LibraryWindow()
    window.show()

    sys.exit(app.exec())
