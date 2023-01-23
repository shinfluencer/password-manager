import tkinter
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_characters = []

    for _ in range(nr_letters):
        password_characters.append(random.choice(letters))

    for _ in range(nr_symbols):
        password_characters.append(random.choice(symbols))

    for _ in range(nr_numbers):
        password_characters.append(random.choice(numbers))

    random.shuffle(password_characters)

    password = "".join(password_characters)
    
    pyperclip.copy(password)
    password_entry.delete(0, tkinter.END)
    password_entry.insert(tkinter.END, string=password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_entry = {
        website: {
            "email": email,
            "password": password
        }
    }
    
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning("Empty Entries", "Please don't leave any inputs empty!")
    else:
        try:
            with open(file="passwords.json", mode="r") as passwords:
                data = json.load(passwords)
        except FileNotFoundError and json.JSONDecodeError:
            with open(file="passwords.json", mode="w") as passwords:
                json.dump(new_entry, passwords, indent=4) 
                messagebox.showinfo("New Password", f"Added {website} to the database.") 
        else:
            data.update(new_entry)            

            with open(file="passwords.json", mode="w") as passwords:
                json.dump(data, passwords, indent=4)
                messagebox.showinfo("New Password", f"Added {website} to the database.")    
        finally:
            website_entry.delete(0, tkinter.END)
            email_entry.delete(0, tkinter.END)
            password_entry.delete(0, tkinter.END)
            
# ---------------------------- SEARCH WEBSITE ---------------------------- #
def search_website():
    requested_website = website_entry.get().title()
    
    if len(requested_website) > 0:
        try:
            with open("passwords.json") as passwords:
                data = json.load(passwords)
        except FileNotFoundError and json.JSONDecodeError:
            messagebox.showerror("No Passwords", "You have no passwords saved.")
        else:
            try:
                requested_data = data[requested_website]
            except KeyError:
                messagebox.showwarning(f"No Password", f"You have no passwords saved for {requested_website}.")
            else:
                email = requested_data["email"]
                password = requested_data["password"]
                messagebox.showinfo(f"{requested_website}", f"Email: {email}\nPassword: {password}")
        finally:
            website_entry.delete(0, tkinter.END)
    else:
        messagebox.showerror("No Website", "Please enter a website.")
        

# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("MyPass Password Manager")
window.config(padx=50, pady=50)
window.resizable(width=False, height=False)

canvas = tkinter.Canvas(width=200, height=200)
logo = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
website_label = tkinter.Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = tkinter.Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = tkinter.Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = tkinter.Entry(width=16)
website_entry.grid(column=1, row=1)

email_entry = tkinter.Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2)

password_entry = tkinter.Entry(width=16)
password_entry.grid(column=1, row=3)

# Buttons
search_button = tkinter.Button(text="Search", width=15, command=search_website)
search_button.grid(column=2, row=1)

generate_password_button = tkinter.Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = tkinter.Button(text="Add", width=30, command=add_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
