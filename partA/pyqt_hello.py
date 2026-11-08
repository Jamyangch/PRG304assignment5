
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QPushButton, QVBoxLayout
)

# Create application
app = QApplication(sys.argv)

# Create main window
window = QWidget()
window.setWindowTitle("PyQt6 Hello World - Your Name - Roll No")
window.resize(400, 250)

# Create widgets
label = QLabel("Hello, Welcome!")
message = QLabel("This is my first PyQt6 application.")
button = QPushButton("Click Me")

# Button click function
def button_clicked():
    message.setText("Button clicked successfully!")

# Connect button to function
button.clicked.connect(button_clicked)

# Create layout
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(message)
layout.addWidget(button)

# Set layout
window.setLayout(layout)

# Display window
window.show()

# Run application
sys.exit(app.exec())
