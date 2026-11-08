
import tkinter as tk

# Create main window
root = tk.Tk()
root.title("Tkinter Hello World - Your Name - Roll No")
root.geometry("400x250")

# Create welcome label
label = tk.Label(
    root,
    text="Hello, Welcome!",
    font=("Arial", 18)
)
label.pack(pady=15)

# Create message label
message = tk.Label(
    root,
    text="This is my first Tkinter application.",
    font=("Arial", 11)
)
message.pack(pady=10)

# Button click function
def button_clicked():
    message.config(text="Button clicked successfully!")

# Create button
button = tk.Button(
    root,
    text="Click Me",
    command=button_clicked
)
button.pack(pady=15)

# Run application
root.mainloop()
