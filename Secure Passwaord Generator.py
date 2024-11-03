from tkinter import *
from tkinter import messagebox
from random import choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    length = int(length_entry.get())
    use_letters = letters_var.get()
    use_numbers = numbers_var.get()
    use_symbols = symbols_var.get()

    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    password_list = []

    if use_letters:
        password_list.extend([choice(letters) for _ in range(length // 3)])
    if use_numbers:
        password_list.extend([choice(numbers) for _ in range(length // 3)])
    if use_symbols:
        password_list.extend([choice(symbols) for _ in range(length // 3)])

    while len(password_list) < length:
        password_list.append(choice(letters + numbers + symbols if (use_letters and use_numbers and use_symbols)
                                    else letters if use_letters else numbers if use_numbers else symbols))

    shuffle(password_list)
    password = "".join(password_list[:length])
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("passworddata.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("passworddata.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("passworddata.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("passworddata.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exist.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()

search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
email_entry = Entry(width=21)
email_entry.grid(row=2, column=1)
email_entry.insert(0, "xyz@gmail.com")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)

criteria_frame = LabelFrame(window, text="Password Criteria")
criteria_frame.grid(row=4, column=0, columnspan=3, pady=10)

letters_var = BooleanVar(value=True)
letters_check = Checkbutton(criteria_frame, text="Letters", variable=letters_var)
letters_check.grid(row=0, column=0)

numbers_var = BooleanVar(value=True)
numbers_check = Checkbutton(criteria_frame, text="Numbers", variable=numbers_var)
numbers_check.grid(row=0, column=1)

symbols_var = BooleanVar(value=True)
symbols_check = Checkbutton(criteria_frame, text="Symbols", variable=symbols_var)
symbols_check.grid(row=0, column=2)

length_label = Label(criteria_frame, text="Length:")
length_label.grid(row=1, column=0)
length_entry = Entry(criteria_frame, width=5)
length_entry.insert(0, "12")  
length_entry.grid(row=1, column=1)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=5, column=0, columnspan=3)

window.mainloop()