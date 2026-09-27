import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import re

from storage import (
    vault_exists,
    create_vault,
    load_vault,
    save_vault
)


class PasswordManager:

    # Auto-lock after 5 minutes of inactivity
    AUTO_LOCK_TIME = 5 * 60 * 1000

    # Clipboard automatically cleared after 20 seconds
    CLIPBOARD_CLEAR_TIME = 20 * 1000

    def __init__(self, root):

        self.root = root

        self.root.title("Secure Password Manager")
        self.root.geometry("950x650")
        self.root.resizable(False, False)

        self.root.configure(bg="#0f172a")

        self.master_password = None
        self.entries = []

        self.auto_lock_job = None
        self.clipboard_job = None

        # Detect user activity
        self.root.bind_all("<Key>", self.reset_auto_lock)
        self.root.bind_all("<Button>", self.reset_auto_lock)
        self.root.bind_all("<Motion>", self.reset_auto_lock)

        self.show_login_screen()

    # ==================================================
    # CLEAR SCREEN
    # ==================================================

    def clear_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # ==================================================
    # PASSWORD STRENGTH
    # ==================================================

    def password_strength(self, password):

        score = 0

        if len(password) >= 8:
            score += 1

        if len(password) >= 12:
            score += 1

        if re.search(r"[A-Z]", password):
            score += 1

        if re.search(r"[a-z]", password):
            score += 1

        if re.search(r"[0-9]", password):
            score += 1

        if re.search(r"[^A-Za-z0-9]", password):
            score += 1

        if score <= 2:
            return "Weak", "red"

        elif score <= 4:
            return "Medium", "orange"

        else:
            return "Strong", "green"

    # ==================================================
    # LOGIN SCREEN
    # ==================================================

    def show_login_screen(self):

        self.clear_screen()

        self.cancel_auto_lock()

        outer = tk.Frame(
            self.root,
            bg="#0f172a"
        )

        outer.pack(
            fill="both",
            expand=True
        )

        card = tk.Frame(
            outer,
            bg="#1e293b",
            padx=45,
            pady=40
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        title = tk.Label(
            card,
            text="🔐 Secure Password Manager",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1e293b"
        )

        title.pack(pady=(0, 10))

        subtitle = tk.Label(
            card,
            text="Local • Encrypted • Secure",
            font=("Arial", 11),
            fg="#94a3b8",
            bg="#1e293b"
        )

        subtitle.pack(pady=(0, 25))

        if vault_exists():

            tk.Label(
                card,
                text="Enter Master Password",
                font=("Arial", 11),
                fg="white",
                bg="#1e293b"
            ).pack(anchor="w")

            password_frame = tk.Frame(
                card,
                bg="#1e293b"
            )

            password_frame.pack(pady=8)

            self.password_entry = tk.Entry(
                password_frame,
                show="•",
                width=30,
                font=("Arial", 12),
                bg="#334155",
                fg="white",
                insertbackground="white",
                relief="flat"
            )

            self.password_entry.pack(side="left")

            self.login_show_button = tk.Button(
                password_frame,
                text="Show",
                command=self.toggle_login_password,
                bg="#475569",
                fg="white",
                relief="flat"
            )

            self.login_show_button.pack(
                side="left",
                padx=5
            )

            tk.Button(
                card,
                text="Unlock Vault",
                command=self.unlock_vault,
                width=25,
                bg="#2563eb",
                fg="white",
                font=("Arial", 11, "bold"),
                relief="flat",
                pady=8
            ).pack(pady=20)

            self.password_entry.bind(
                "<Return>",
                lambda event: self.unlock_vault()
            )

            self.password_entry.focus()

        else:

            tk.Label(
                card,
                text="Create Master Password",
                font=("Arial", 11),
                fg="white",
                bg="#1e293b"
            ).pack(anchor="w")

            self.password_entry = tk.Entry(
                card,
                show="•",
                width=38,
                font=("Arial", 12),
                bg="#334155",
                fg="white",
                insertbackground="white",
                relief="flat"
            )

            self.password_entry.pack(pady=8)

            self.password_strength_label = tk.Label(
                card,
                text="Password strength: ",
                font=("Arial", 9),
                fg="#94a3b8",
                bg="#1e293b"
            )

            self.password_strength_label.pack(
                anchor="w"
            )

            self.password_entry.bind(
                "<KeyRelease>",
                self.update_master_strength
            )

            tk.Label(
                card,
                text="Confirm Master Password",
                font=("Arial", 11),
                fg="white",
                bg="#1e293b"
            ).pack(
                anchor="w",
                pady=(15, 0)
            )

            self.confirm_entry = tk.Entry(
                card,
                show="•",
                width=38,
                font=("Arial", 12),
                bg="#334155",
                fg="white",
                insertbackground="white",
                relief="flat"
            )

            self.confirm_entry.pack(pady=8)

            tk.Button(
                card,
                text="Create Secure Vault",
                command=self.create_new_vault,
                width=25,
                bg="#16a34a",
                fg="white",
                font=("Arial", 11, "bold"),
                relief="flat",
                pady=8
            ).pack(pady=20)

    # ==================================================
    # LOGIN PASSWORD SHOW/HIDE
    # ==================================================

    def toggle_login_password(self):

        if self.password_entry.cget("show") == "":

            self.password_entry.config(show="•")
            self.login_show_button.config(text="Show")

        else:

            self.password_entry.config(show="")
            self.login_show_button.config(text="Hide")

    # ==================================================
    # MASTER PASSWORD STRENGTH
    # ==================================================

    def update_master_strength(self, event=None):

        password = self.password_entry.get()

        if not password:

            self.password_strength_label.config(
                text="Password strength:"
            )

            return

        strength, color = self.password_strength(
            password
        )

        self.password_strength_label.config(
            text=f"Password strength: {strength}",
            fg=color
        )

    # ==================================================
    # CREATE VAULT
    # ==================================================

    def create_new_vault(self):

        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not password:

            messagebox.showwarning(
                "Missing Password",
                "Please enter a master password."
            )

            return

        strength, _ = self.password_strength(
            password
        )

        if len(password) < 10:

            messagebox.showwarning(
                "Weak Password",
                "Use at least 10 characters for the master password."
            )

            return

        if strength == "Weak":

            messagebox.showwarning(
                "Weak Password",
                "Please create a stronger master password."
            )

            return

        if password != confirm:

            messagebox.showerror(
                "Password Error",
                "Master passwords do not match."
            )

            return

        create_vault(password)

        self.master_password = password
        self.entries = []

        messagebox.showinfo(
            "Success",
            "Secure vault created successfully."
        )

        self.show_dashboard()

    # ==================================================
    # UNLOCK
    # ==================================================

    def unlock_vault(self):

        password = self.password_entry.get()

        if not password:

            messagebox.showwarning(
                "Warning",
                "Please enter your master password."
            )

            return

        try:

            self.entries = load_vault(password)

            self.master_password = password

            self.show_dashboard()

        except ValueError:

            messagebox.showerror(
                "Access Denied",
                "Incorrect master password."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Unable to open vault:\n{error}"
            )

    # ==================================================
    # DASHBOARD
    # ==================================================

    def show_dashboard(self):

        self.clear_screen()

        self.start_auto_lock()

        self.root.configure(
            bg="#0f172a"
        )

        # Header
        header = tk.Frame(
            self.root,
            bg="#111827",
            height=70
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="🔐 Secure Password Manager",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#111827"
        ).pack(
            side="left",
            padx=25,
            pady=18
        )

        tk.Button(
            header,
            text="🔒 Lock",
            command=self.lock_vault,
            bg="#dc2626",
            fg="white",
            relief="flat",
            padx=15
        ).pack(
            side="right",
            padx=25
        )

        # Main area
        content = tk.Frame(
            self.root,
            bg="#0f172a",
            padx=25,
            pady=20
        )

        content.pack(
            fill="both",
            expand=True
        )

        # Search area
        search_frame = tk.Frame(
            content,
            bg="#0f172a"
        )

        search_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            search_frame,
            text="🔎 Search",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#0f172a"
        ).pack(
            side="left"
        )

        self.search_entry = tk.Entry(
            search_frame,
            width=35,
            font=("Arial", 11),
            bg="#1e293b",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        self.search_entry.pack(
            side="left",
            padx=10,
            ipady=6
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_table()
        )

        tk.Button(
            search_frame,
            text="+ Add Password",
            command=self.add_password_window,
            bg="#2563eb",
            fg="white",
            relief="flat",
            padx=15,
            pady=7
        ).pack(
            side="right"
        )

        # Table
        table_frame = tk.Frame(
            content,
            bg="#1e293b"
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Treeview",
            background="#1e293b",
            foreground="white",
            fieldbackground="#1e293b",
            rowheight=35,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#334155",
            foreground="white",
            font=("Arial", 10, "bold")
        )

        columns = (
            "website",
            "username"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "website",
            text="Website / Service"
        )

        self.tree.heading(
            "username",
            text="Username / Email"
        )

        self.tree.column(
            "website",
            width=400
        )

        self.tree.column(
            "username",
            width=400
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

        # Buttons
        button_frame = tk.Frame(
            content,
            bg="#0f172a"
        )

        button_frame.pack(
            pady=15
        )

        tk.Button(
            button_frame,
            text="👁 View Password",
            command=self.view_password,
            bg="#475569",
            fg="white",
            relief="flat",
            padx=12,
            pady=7
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="✏ Edit",
            command=self.edit_password,
            bg="#7c3aed",
            fg="white",
            relief="flat",
            padx=15,
            pady=7
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="🗑 Delete",
            command=self.delete_password,
            bg="#dc2626",
            fg="white",
            relief="flat",
            padx=15,
            pady=7
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="🎲 Password Generator",
            command=self.generate_password_window,
            bg="#0891b2",
            fg="white",
            relief="flat",
            padx=12,
            pady=7
        ).pack(
            side="left",
            padx=5
        )

        self.refresh_table()

    # ==================================================
    # REFRESH TABLE
    # ==================================================

    def refresh_table(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        search_text = self.search_entry.get().lower()

        for index, entry in enumerate(self.entries):

            website = entry["website"]
            username = entry["username"]

            if (
                search_text in website.lower()
                or search_text in username.lower()
            ):

                self.tree.insert(
                    "",
                    "end",
                    iid=str(index),
                    values=(
                        website,
                        username
                    )
                )

    # ==================================================
    # ADD PASSWORD
    # ==================================================

    def add_password_window(self):

        window = tk.Toplevel(self.root)

        window.title("Add Credential")
        window.geometry("500x500")
        window.configure(bg="#0f172a")
        window.resizable(False, False)

        frame = tk.Frame(
            window,
            bg="#1e293b",
            padx=30,
            pady=25
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            frame,
            text="Add New Credential",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1e293b"
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Website / Service",
            fg="white",
            bg="#1e293b"
        ).pack(anchor="w")

        website_entry = tk.Entry(
            frame,
            width=45,
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        website_entry.pack(
            pady=8,
            ipady=5
        )

        tk.Label(
            frame,
            text="Username / Email",
            fg="white",
            bg="#1e293b"
        ).pack(anchor="w")

        username_entry = tk.Entry(
            frame,
            width=45,
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        username_entry.pack(
            pady=8,
            ipady=5
        )

        tk.Label(
            frame,
            text="Password",
            fg="white",
            bg="#1e293b"
        ).pack(anchor="w")

        password_frame = tk.Frame(
            frame,
            bg="#1e293b"
        )

        password_frame.pack(
            fill="x"
        )

        password_entry = tk.Entry(
            password_frame,
            width=35,
            show="•",
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        password_entry.pack(
            side="left",
            ipady=5
        )

        def toggle():

            if password_entry.cget("show") == "":

                password_entry.config(show="•")
                toggle_button.config(text="Show")

            else:

                password_entry.config(show="")
                toggle_button.config(text="Hide")

        toggle_button = tk.Button(
            password_frame,
            text="Show",
            command=toggle,
            bg="#475569",
            fg="white",
            relief="flat"
        )

        toggle_button.pack(
            side="left",
            padx=5
        )

        strength_label = tk.Label(
            frame,
            text="Password strength:",
            fg="#94a3b8",
            bg="#1e293b"
        )

        strength_label.pack(
            anchor="w",
            pady=5
        )

        def update_strength(event=None):

            password = password_entry.get()

            if not password:

                strength_label.config(
                    text="Password strength:"
                )

                return

            strength, color = self.password_strength(
                password
            )

            strength_label.config(
                text=f"Password strength: {strength}",
                fg=color
            )

        password_entry.bind(
            "<KeyRelease>",
            update_strength
        )

        def generate():

            password_entry.delete(
                0,
                tk.END
            )

            password_entry.insert(
                0,
                self.generate_secure_password()
            )

            update_strength()

        tk.Button(
            frame,
            text="🎲 Generate Strong Password",
            command=generate,
            bg="#0891b2",
            fg="white",
            relief="flat",
            pady=6
        ).pack(
            pady=10
        )

        def save():

            website = website_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get()

            if not website or not username or not password:

                messagebox.showwarning(
                    "Missing Information",
                    "Please fill in all fields.",
                    parent=window
                )

                return

            self.entries.append({
                "website": website,
                "username": username,
                "password": password
            })

            save_vault(
                self.entries,
                self.master_password
            )

            self.refresh_table()

            messagebox.showinfo(
                "Success",
                "Credential saved securely.",
                parent=window
            )

            window.destroy()

        tk.Button(
            frame,
            text="Save Credential",
            command=save,
            width=25,
            bg="#16a34a",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            pady=8
        ).pack(pady=10)

    # ==================================================
    # EDIT PASSWORD
    # ==================================================

    def edit_password(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an account first."
            )

            return

        index = int(selected[0])

        entry = self.entries[index]

        window = tk.Toplevel(self.root)

        window.title("Edit Credential")
        window.geometry("500x450")
        window.configure(bg="#0f172a")
        window.resizable(False, False)

        frame = tk.Frame(
            window,
            bg="#1e293b",
            padx=30,
            pady=25
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            frame,
            text="Edit Credential",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1e293b"
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Website / Service",
            fg="white",
            bg="#1e293b"
        ).pack(anchor="w")

        website_entry = tk.Entry(
            frame,
            width=45,
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        website_entry.insert(
            0,
            entry["website"]
        )

        website_entry.pack(
            pady=8,
            ipady=5
        )

        tk.Label(
            frame,
            text="Username / Email",
            fg="white",
            bg="#1e293b"
        ).pack(anchor="w")

        username_entry = tk.Entry(
            frame,
            width=45,
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        username_entry.insert(
            0,
            entry["username"]
        )

        username_entry.pack(
            pady=8,
            ipady=5
        )

        tk.Label(
            frame,
            text="Password",
            fg="white",
            bg="#1e293b"
        ).pack(anchor="w")

        password_entry = tk.Entry(
            frame,
            width=45,
            show="•",
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        password_entry.insert(
            0,
            entry["password"]
        )

        password_entry.pack(
            pady=8,
            ipady=5
        )

        def toggle_password():

            if password_entry.cget("show") == "":

                password_entry.config(show="•")
                show_button.config(text="Show")

            else:

                password_entry.config(show="")
                show_button.config(text="Hide")

        show_button = tk.Button(
            frame,
            text="Show",
            command=toggle_password,
            bg="#475569",
            fg="white",
            relief="flat"
        )

        show_button.pack()

        def update():

            new_website = website_entry.get().strip()
            new_username = username_entry.get().strip()
            new_password = password_entry.get()

            if not new_website or not new_username or not new_password:

                messagebox.showwarning(
                    "Missing Information",
                    "All fields are required.",
                    parent=window
                )

                return

            self.entries[index] = {
                "website": new_website,
                "username": new_username,
                "password": new_password
            }

            save_vault(
                self.entries,
                self.master_password
            )

            self.refresh_table()

            messagebox.showinfo(
                "Updated",
                "Credential updated successfully.",
                parent=window
            )

            window.destroy()

        tk.Button(
            frame,
            text="Save Changes",
            command=update,
            width=25,
            bg="#7c3aed",
            fg="white",
            relief="flat",
            pady=8
        ).pack(pady=20)

    # ==================================================
    # VIEW PASSWORD
    # ==================================================

    def view_password(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an account first."
            )

            return

        index = int(selected[0])

        entry = self.entries[index]

        window = tk.Toplevel(self.root)

        window.title("Credential Details")
        window.geometry("450x330")
        window.configure(bg="#0f172a")
        window.resizable(False, False)

        frame = tk.Frame(
            window,
            bg="#1e293b",
            padx=30,
            pady=25
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            frame,
            text="Credential Details",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#1e293b"
        ).pack(pady=10)

        tk.Label(
            frame,
            text=f"Website: {entry['website']}",
            font=("Arial", 11),
            fg="white",
            bg="#1e293b"
        ).pack(pady=5)

        tk.Label(
            frame,
            text=f"Username: {entry['username']}",
            font=("Arial", 11),
            fg="white",
            bg="#1e293b"
        ).pack(pady=5)

        password_frame = tk.Frame(
            frame,
            bg="#1e293b"
        )

        password_frame.pack(pady=10)

        password_entry = tk.Entry(
            password_frame,
            width=25,
            show="•",
            font=("Arial", 11),
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        password_entry.insert(
            0,
            entry["password"]
        )

        password_entry.config(
            state="readonly"
        )

        password_entry.pack(
            side="left",
            ipady=5
        )

        def toggle():

            password_entry.config(
                state="normal"
            )

            if password_entry.cget("show") == "":

                password_entry.config(
                    show="•"
                )

                show_button.config(
                    text="Show"
                )

            else:

                password_entry.config(
                    show=""
                )

                show_button.config(
                    text="Hide"
                )

            password_entry.config(
                state="readonly"
            )

        show_button = tk.Button(
            password_frame,
            text="Show",
            command=toggle,
            bg="#475569",
            fg="white",
            relief="flat"
        )

        show_button.pack(
            side="left",
            padx=5
        )

        tk.Button(
            frame,
            text="📋 Copy Password",
            command=lambda: self.copy_to_clipboard(
                entry["password"]
            ),
            bg="#0891b2",
            fg="white",
            relief="flat",
            pady=7
        ).pack(pady=10)

    # ==================================================
    # DELETE
    # ==================================================

    def delete_password(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an account first."
            )

            return

        index = int(selected[0])

        entry = self.entries[index]

        confirmation = messagebox.askyesno(
            "Confirm Delete",
            f"Delete credentials for {entry['website']}?"
        )

        if confirmation:

            del self.entries[index]

            save_vault(
                self.entries,
                self.master_password
            )

            self.refresh_table()

            messagebox.showinfo(
                "Deleted",
                "Credential deleted successfully."
            )

    # ==================================================
    # PASSWORD GENERATOR
    # ==================================================

    def generate_secure_password(self, length=18):

        characters = (
            string.ascii_letters
            + string.digits
            + string.punctuation
        )

        while True:

            password = ''.join(
                secrets.choice(characters)
                for _ in range(length)
            )

            if (
                re.search(r"[A-Z]", password)
                and re.search(r"[a-z]", password)
                and re.search(r"[0-9]", password)
                and re.search(r"[^A-Za-z0-9]", password)
            ):

                return password

    # ==================================================
    # PASSWORD GENERATOR WINDOW
    # ==================================================

    def generate_password_window(self):

        window = tk.Toplevel(self.root)

        window.title("Password Generator")
        window.geometry("500x300")
        window.configure(bg="#0f172a")
        window.resizable(False, False)

        frame = tk.Frame(
            window,
            bg="#1e293b",
            padx=30,
            pady=30
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            frame,
            text="🎲 Secure Password Generator",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#1e293b"
        ).pack(pady=10)

        password_var = tk.StringVar()

        password_entry = tk.Entry(
            frame,
            textvariable=password_var,
            width=42,
            font=("Arial", 11),
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        password_entry.pack(
            pady=15,
            ipady=7
        )

        def generate():

            password_var.set(
                self.generate_secure_password()
            )

        tk.Button(
            frame,
            text="Generate",
            command=generate,
            bg="#0891b2",
            fg="white",
            relief="flat",
            padx=20,
            pady=7
        ).pack(
            side="left",
            padx=10
        )

        tk.Button(
            frame,
            text="Copy",
            command=lambda: self.copy_to_clipboard(
                password_var.get()
            ),
            bg="#2563eb",
            fg="white",
            relief="flat",
            padx=20,
            pady=7
        ).pack(
            side="left",
            padx=10
        )

        generate()

    # ==================================================
    # CLIPBOARD
    # ==================================================

    def copy_to_clipboard(self, text):

        if not text:

            messagebox.showwarning(
                "Warning",
                "There is no password to copy."
            )

            return

        self.root.clipboard_clear()
        self.root.clipboard_append(text)

        if self.clipboard_job:

            try:
                self.root.after_cancel(
                    self.clipboard_job
                )
            except:
                pass

        self.clipboard_job = self.root.after(
            self.CLIPBOARD_CLEAR_TIME,
            self.clear_clipboard
        )

        messagebox.showinfo(
            "Copied",
            "Password copied.\n\n"
            "The clipboard will be cleared automatically "
            "after 20 seconds."
        )

    def clear_clipboard(self):

        try:

            self.root.clipboard_clear()

            self.clipboard_job = None

        except:
            pass

    # ==================================================
    # AUTO LOCK
    # ==================================================

    def start_auto_lock(self):

        self.cancel_auto_lock()

        self.auto_lock_job = self.root.after(
            self.AUTO_LOCK_TIME,
            self.auto_lock
        )

    def reset_auto_lock(self, event=None):

        if self.master_password is None:
            return

        self.start_auto_lock()

    def cancel_auto_lock(self):

        if self.auto_lock_job:

            try:

                self.root.after_cancel(
                    self.auto_lock_job
                )

            except:
                pass

            self.auto_lock_job = None

    def auto_lock(self):

        if self.master_password is not None:

            self.master_password = None
            self.entries = []

            messagebox.showinfo(
                "Vault Locked",
                "The vault was automatically locked "
                "due to inactivity."
            )

            self.show_login_screen()

    # ==================================================
    # MANUAL LOCK
    # ==================================================

    def lock_vault(self):

        self.cancel_auto_lock()

        self.master_password = None
        self.entries = []

        self.show_login_screen()


# ======================================================
# START APPLICATION
# ======================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = PasswordManager(root)

    root.mainloop()