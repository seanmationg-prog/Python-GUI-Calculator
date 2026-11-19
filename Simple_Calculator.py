import tkinter as tk

# 1. Main Window Setup (Modified dimensions and modern slate blue theme)
window = tk.Tk()
window.title("Modern Calculator")
window.geometry("380x540")
window.resizable(False, False)
window.configure(bg="#0f172a")

expression = ""

# 2. Calculator Display (Modified font size and dark slate colors)
display = tk.Entry(
    window,
    font=("Segoe UI", 28, "bold"),
    bg="#1e293b",
    fg="#f8fafc",
    insertbackground="#38bdf8",
    justify="right",
    bd=0
)
display.pack(fill="x", padx=16, pady=24, ipady=18)

# 3. Keyboard Input Validation (Allows numbers, operators, and navigation keys)
def validate_input(event):
    if event.char.isdigit() or event.char in "+-*/." or event.keysym in (
        "BackSpace", "Delete", "Left", "Right"
    ):
        return None
    if event.keysym == "Return":
        calculate()
        return "break"
    return "break"

def sync_expression(event):
    global expression
    expression = display.get()

display.bind("<Key>", validate_input)
display.bind("<KeyRelease>", sync_expression)

# 4. Button Functions
def button_click(value):
    global expression
    expression += str(value)
    display.delete(0, tk.END)
    display.insert(tk.END, expression)

def clear():
    global expression
    expression = ""
    display.delete(0, tk.END)

# New Feature: Backspace function to remove the last character
def backspace():
    global expression
    expression = expression[:-1]
    display.delete(0, tk.END)
    display.insert(tk.END, expression)

def calculate():
    global expression
    try:
        result = eval(expression)
        display.delete(0, tk.END)
        display.insert(tk.END, str(result))
        expression = str(result)
    except Exception:
        display.delete(0, tk.END)
        display.insert(tk.END, "ERROR")
        expression = ""

# 5. Button Layout (Rearranged top row to include Clear and Backspace)
buttons = [
    ["C", "⌫", "/", "*"],
    ["7", "8", "9", "-"],
    ["4", "5", "6", "+"],
    ["1", "2", "3", "="],
    ["0", "."]
]

button_frame = tk.Frame(window, bg="#0f172a")
button_frame.pack(expand=True, fill="both", padx=12, pady=10)

# 6. Generating Buttons Dynamically
for row_index, row in enumerate(buttons):
    for col_index, value in enumerate(row):
        # Assign commands and custom colors based on button type
        if value == "=":
            command = calculate
            color = "#10b981"  # Emerald green
        elif value == "C":
            command = clear
            color = "#ef4444"  # Coral red
        elif value == "⌫":
            command = backspace
            color = "#f59e0b"  # Amber
        elif value in ["+", "-", "*", "/"]:
            command = lambda v=value: button_click(v)
            color = "#0284c7"  # Sky blue
        else:
            command = lambda v=value: button_click(v)
            color = "#334155"  # Slate gray

        button = tk.Button(
            button_frame,
            text=value,
            font=("Segoe UI", 18, "bold"),
            bg=color,
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            bd=0,
            command=command
        )

        # Make '0' span 2 columns and '=' span 2 rows for a clean layout
        if value == "0":
            button.grid(row=row_index, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        elif value == ".":
            button.grid(row=row_index, column=2, sticky="nsew", padx=5, pady=5)
        elif value == "=":
            button.grid(row=row_index, column=3, rowspan=2, sticky="nsew", padx=5, pady=5)
        else:
            button.grid(row=row_index, column=col_index, sticky="nsew", padx=5, pady=5)

# 7. Grid Configuration (5 rows, 4 columns)
for i in range(5):
    button_frame.grid_rowconfigure(i, weight=1)

for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1)

window.mainloop()
