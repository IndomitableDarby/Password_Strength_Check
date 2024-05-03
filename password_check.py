import tkinter as tk
from tkinter import messagebox
import string
import random
import re

def check_password_strength(password):
    score = 0

    # Length check
    length = len(password)
    if length >= 8:
        score += 20
    if length >= 12:
        score += 20
    if length >= 16:
        score += 20

    # Character set check
    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)
    if all([has_lowercase, has_uppercase, has_digit, has_special]):
        score += 20

    # Check common passwords
    common_passwords = ['password', '123456', 'qwerty', 'letmein']
    if password.lower() in common_passwords:
        score -= 30

    return score

def generate_password(length=12, use_lowercase=True, use_uppercase=True, use_digits=True, use_special=True):
    charset = ''
    if use_lowercase:
        charset += string.ascii_lowercase
    if use_uppercase:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    if use_special:
        charset += string.punctuation

    if not charset:
        raise ValueError("At least one character set must be selected.")

    return ''.join(random.choice(charset) for _ in range(length))

def evaluate_password():
    password = password_entry.get()
    if not password:
        messagebox.showwarning("Error", "Please enter a password to evaluate.")
        return

    score = check_password_strength(password)

    if score >= 60:
        strength_label.config(text="Strong", fg="green")
        draw_progress_bar(score, "green")
        hacked_days = random.randint(100, 365)
        hacked_message = f"Your strong password is safe! Hacked by hackers in {hacked_days} days."
    elif score >= 40:
        strength_label.config(text="Medium", fg="orange")
        draw_progress_bar(score, "orange")
        hacked_days = random.randint(30, 100)
        hacked_message = f"Your medium password might be at risk! Hacked by hackers in {hacked_days} days."
    else:
        strength_label.config(text="Weak", fg="red")
        draw_progress_bar(score, "red")
        hacked_days = random.randint(1, 30)
        hacked_message = f"Your weak password is vulnerable! Hacked by hackers in {hacked_days} days."

    feedback_label.config(text=hacked_message)
    update_background_color(score)

def generate_new_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError("Invalid password length")

        use_lowercase = lowercase_var.get()
        use_uppercase = uppercase_var.get()
        use_digits = digits_var.get()
        use_special = special_var.get()

        new_password = generate_password(length=length, use_lowercase=use_lowercase, use_uppercase=use_uppercase,
                                          use_digits=use_digits, use_special=use_special)
        generated_password_label.config(text=new_password)

    except ValueError:
        messagebox.showwarning("Error", "Please enter a valid password length.")

def toggle_password_visibility():
    current_state = password_entry.cget("show")
    if current_state == "*":
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

def draw_progress_bar(score, color):
    canvas.delete("progress")
    width = int(score * 2)  # Adjust width based on score (scaling factor)
    canvas.create_rectangle(10, 10, width, 30, fill=color, outline=color, tags="progress")

def update_background_color(score):
    if score >= 60:
        window.config(bg="#C8E6C9")  # Light green background for strong password
    elif score >= 40:
        window.config(bg="#FFF9C4")  # Light yellow background for medium password
    else:
        window.config(bg="#FFCDD2")  # Light red background for weak password

# Create main window
window = tk.Tk()
window.title("Password Strength Checker")

# Create widgets with custom styling
password_label = tk.Label(window, text="Enter Password:")
password_entry = tk.Entry(window, show="*")
visibility_button = tk.Button(window, text="Show/Hide", command=toggle_password_visibility)
evaluate_button = tk.Button(window, text="Evaluate", command=evaluate_password)
strength_label = tk.Label(window, text="", font=("Helvetica", 16, "bold"))
canvas = tk.Canvas(window, width=200, height=30)
feedback_label = tk.Label(window, text="", wraplength=300)
generate_label = tk.Label(window, text="Generate Password Length:")
length_entry = tk.Entry(window, width=5)
generate_button = tk.Button(window, text="Generate Password", command=generate_new_password)
generated_password_label = tk.Label(window, text="", font=("Courier", 12), wraplength=300)

# Checkboxes for character set selection
lowercase_var = tk.BooleanVar()
uppercase_var = tk.BooleanVar()
digits_var = tk.BooleanVar()
special_var = tk.BooleanVar()

lowercase_checkbox = tk.Checkbutton(window, text="Lowercase", variable=lowercase_var, onvalue=True, offvalue=False)
uppercase_checkbox = tk.Checkbutton(window, text="Uppercase", variable=uppercase_var, onvalue=True, offvalue=False)
digits_checkbox = tk.Checkbutton(window, text="Digits", variable=digits_var, onvalue=True, offvalue=False)
special_checkbox = tk.Checkbutton(window, text="Special Characters", variable=special_var, onvalue=True, offvalue=False)

# Arrange widgets using grid layout
password_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
password_entry.grid(row=0, column=1, padx=10, pady=10)
visibility_button.grid(row=0, column=2, padx=10, pady=10)
evaluate_button.grid(row=0, column=3, padx=10, pady=10)
strength_label.grid(row=1, column=0, columnspan=4, pady=10)
canvas.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
feedback_label.grid(row=3, column=0, columnspan=4, pady=10)
generate_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
length_entry.grid(row=4, column=1, padx=10, pady=10)
lowercase_checkbox.grid(row=4, column=2, padx=10, pady=10, sticky="w")
uppercase_checkbox.grid(row=4, column=3, padx=10, pady=10, sticky="w")
digits_checkbox.grid(row=5, column=2, padx=10, pady=10, sticky="w")
special_checkbox.grid(row=5, column=3, padx=10, pady=10, sticky="w")
generate_button.grid(row=5, column=1, padx=10, pady=10)
generated_password_label.grid(row=6, column=0, columnspan=4, pady=10)

# Run the main event loop
window.mainloop()
