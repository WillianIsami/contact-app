import tkinter as tk
import sqlite3
from tkinter import messagebox

class ContactApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title = ("Contact App")
        self.db_connection = sqlite3.connect("contacts.db")
        self.create_table()
        self.create_widgets()

    def create_table(self):
        with self.db_connection:
            self.db_connection.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL, 
                    phone TEXT NOT NULL
                )
            ''')

    def create_widgets(self):
        font = ("Arial", 12)
        tk.Label(self, text="Name:", font=font, bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self, text="Email:", font=font, bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self, text="Phone:", font=font, bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=2, column=1)
        self.listbox = tk.Listbox(self, width=50)
        self.listbox.grid(row=5, column=0, columnspan=2)
        tk.Button(self, text="Add Contact", font=font, bg="#f0f0f0", command=self.add_contact).grid(row=3, column=0, columnspan=2)
        tk.Button(self, text="Refresh Users", font=font, bg="#f0f0f0", command=self.refresh_users).grid(row=6, column=0, columnspan=2)

    def refresh_users(self):
        self.listbox.delete(0, tk.END)
        with self.db_connection:
            cursor = self.db_connection.execute('SELECT * FROM contacts')
            users = cursor.fetchall()
        if not users:
            messagebox.showinfo("No contacts", "No contacts avaliable")
            return 
        for user in users:
            self.listbox.insert(tk.END, f"Name: {user[1]},   Email: {user[2]},     Phone: {user[3]}")

    def add_contact(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        if name and email and phone:
            with self.db_connection:
                self.db_connection.execute('''
                    INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)
                ''', (name, email, phone))
            messagebox.showinfo("Success", "Contact added successfully.")
            self.clear_entries()
        else:
            messagebox.showwarning("Error", "Please fill in all fields.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = ContactApp()
    app.mainloop()
