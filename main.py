import tkinter as tk
from tkinter import messagebox
import json
import secrets
import string
from PIL import Image, ImageTk

def generate_password():
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def save_data():
    website = website_entry.get()
    email_username = email_username_entry.get()
    password = password_entry.get()
    
    if not website or not email_username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    new_data = {
        website: {
            "email": email_username,
            "password": password,
        }
    }
    
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        data = {}
    data.update(new_data)
    
    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)
    
    website_entry.delete(0, tk.END)
    email_username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    
    messagebox.showinfo("Success", "Data added successfully!")

def search_data():
    website = website_entry.get()
    
    if not website:
        messagebox.showerror("Error", "Website field is required!")
        return
    
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found!")
        return
    
    if website in data:
        email_username = data[website]["email"]
        password = data[website]["password"]
        email_username_entry.delete(0, tk.END)
        email_username_entry.insert(0, email_username)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
    else:
        messagebox.showerror("Error", f"No details for the {website} website exists!")

window = tk.Tk()
window.title("Password Manager")

button_style = {'font': ('Arial', 10, 'bold'), 'bg': '#ff3333', 'fg': 'white'}
entry_style = {'font': ('Arial', 10)}

logo_image = Image.open("logo.png")
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(window, image=logo_photo, bg='white')
logo_label.grid(row=0, column=0, columnspan=3, pady=(10, 0))

website_label = tk.Label(window, text="Website:", bg='white')
website_label.grid(row=1, column=0, sticky='e')
website_entry = tk.Entry(window, **entry_style, width=35)
website_entry.grid(row=1, column=1, pady=5)
search_data_button = tk.Button(window, text="Search", **button_style, command=search_data)
search_data_button.grid(row=1, column=2, padx=(5, 10), pady=5)

email_username_label = tk.Label(window, text="Email/Username:", bg='white')
email_username_label.grid(row=2, column=0, sticky='e')
email_username_entry = tk.Entry(window, **entry_style, width=35)
email_username_entry.grid(row=2, column=1, pady=5)

password_label = tk.Label(window, text="Password:", bg='white')
password_label.grid(row=3, column=0, sticky='e')
password_entry = tk.Entry(window, **entry_style, width=35)
password_entry.grid(row=3, column=1, pady=5)

generate_password_button = tk.Button(window, text="Generate Password", **button_style, command=generate_password)
generate_password_button.grid(row=3, column=2, padx=(5, 10), pady=5)

add_button = tk.Button(window, text="Save", **button_style, width=35, command=save_data)
add_button.grid(row=4, column=1, pady=(5, 10))

window.configure(bg='white')

window.mainloop()