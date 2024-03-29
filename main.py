# internal pkg
import tkinter
from tkinter import messagebox
import random
import json

# External pkg
# link:- https://pypi.org/project/pyperclip/
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def password_generate():
    # clear password entry
    password_entry.delete(0, tkinter.END)

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    # insert password in password entry
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_button_click():
    website_input = website_entry.get()
    email_username_input = email_username_entry.get()
    password_input = password_entry.get()
    new_data = {website_input: {"email": email_username_input, "password": password_input}}

    # empty entry pop up
    if len(website_input) == 0 or len(email_username_input) == 0 or len(password_input) == 0:
        messagebox.showinfo(title="Alert", message="Please don't left any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(fp=data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(obj=new_data, fp=data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(obj=data, fp=data_file, indent=4)
        finally:
            # delete the data present on gui using .delete function
            website_entry.delete(0, tkinter.END)
            password_entry.delete(0, tkinter.END)
            email_username_entry.delete(0, tkinter.END)

            email_username_entry.insert(0, "your_email@example.com")


# ---------------------------- UI SETUP ------------------------------- #


window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = tkinter.Canvas(width=200, height=200)
lock_png = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 95, image=lock_png)
canvas.grid(row=0, column=1)

# Website label
website_label = tkinter.Label(text="Website:")
website_label.grid(row=1, column=0)

# Website Entry
website_entry = tkinter.Entry(width=20)
website_entry.grid(row=1, column=1, columnspan=1)
# focus the cursor
website_entry.focus()


def search():
    search_website = website_entry.get()
    try:
        with open("data.json", 'r') as data_file:
            data = json.load(fp=data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="File Error", message="Data file doesn't exist")
    else:
        if search_website in data:
            email = data[search_website]['email']
            password = data[search_website]['password']
            messagebox.showinfo(title=search_website, message=f"Email: {email}\n Password: {password}")
        elif len(search_website) == 0:
            messagebox.showinfo(message="Please Enter website name to search")
        else:
            messagebox.showinfo(message="Website data not found")


# Search button
search_button = tkinter.Button(text="Search", width=10, command=search)
search_button.grid(row=1, column=2)

# Email/Username Label
email_username_label = tkinter.Label(text="Email/Username:")
email_username_label.grid(row=2, column=0)

# Email/Username Entry
email_username_entry = tkinter.Entry(width=35)

# Change your_email@example.com to your email
email_username_entry.insert(0, "your_email@example.com")
email_username_entry.grid(row=2, column=1, columnspan=2)

# Password Label
password_label = tkinter.Label(text="Password:")
password_label.grid(row=3, column=0)

# Password Entry
password_entry = tkinter.Entry(width=20)
password_entry.grid(row=3, column=1)

# Generate Password Button
generate_password_button = tkinter.Button(text="GeneratePassword", width=10, command=password_generate)
generate_password_button.grid(row=3, column=2)

# Add Button
add_button = tkinter.Button(text="Add", width=35, command=add_button_click)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
