import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class RegisterWindow:

    def __init__(self, root):

        self.root = root

        self.register_window = tk.Toplevel(root)
        self.register_window.title("Lecturer Registration")
        self.register_window.geometry("450x450")
        self.register_window.resizable(False, False)

        tk.Label(
            self.register_window,
            text="Register Lecturer Account",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Full Name
        tk.Label(
            self.register_window,
            text="Full Name"
        ).pack()

        self.fullname = tk.Entry(
            self.register_window,
            width=35
        )
        self.fullname.pack(pady=5)

        # Username
        tk.Label(
            self.register_window,
            text="Username"
        ).pack()

        self.username = tk.Entry(
            self.register_window,
            width=35
        )
        self.username.pack(pady=5)

        # Password
        tk.Label(
            self.register_window,
            text="Password"
        ).pack()

        self.password = tk.Entry(
            self.register_window,
            show="*",
            width=35
        )
        self.password.pack(pady=5)

        # Campus
        tk.Label(
            self.register_window,
            text="Campus"
        ).pack()

        self.campus = ttk.Combobox(
            self.register_window,
            width=32,
            state="readonly"
        )

        self.campus["values"] = (
            "Richfield Centurion",
            "Richfield Braamfontein",
            "Richfield Polokwane"
        )

        self.campus.current(0)
        self.campus.pack(pady=5)

        tk.Button(
            self.register_window,
            text="Register",
            bg="green",
            fg="white",
            width=20,
            command=self.register
        ).pack(pady=20)

    # ==========================================
    # REGISTER USER
    # ==========================================

    def register(self):

        fullname = self.fullname.get().strip()
        username = self.username.get().strip()
        password = self.password.get().strip()
        campus = self.campus.get().strip()

        if fullname == "":
            messagebox.showerror(
                "Error",
                "Please enter Full Name."
            )
            return

        if username == "":
            messagebox.showerror(
                "Error",
                "Please enter Username."
            )
            return

        if password == "":
            messagebox.showerror(
                "Error",
                "Please enter Password."
            )
            return

        try:

            conn = sqlite3.connect(
                "database/campus.db"
            )

            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO users(
                fullname,
                username,
                password,
                role,
                campus
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                fullname,
                username,
                password,
                "Lecturer",
                campus
            ))

            conn.commit()
            conn.close()

            self.register_window.destroy()

            # Success Window
            success_window = tk.Toplevel(self.root)
            success_window.title(
                "Registration Successful"
            )
            success_window.geometry("400x300")
            success_window.resizable(False, False)

            tk.Label(
                success_window,
                text="✓",
                fg="green",
                font=("Arial", 40, "bold")
            ).pack(pady=10)

            tk.Label(
                success_window,
                text="Registration Successful",
                font=("Arial", 16, "bold")
            ).pack(pady=5)

            tk.Label(
                success_window,
                text=f"Welcome {fullname}"
            ).pack()

            tk.Label(
                success_window,
                text="Your account has been created successfully."
            ).pack(pady=10)

            # ===================================
            # CONTINUE BUTTON
            # ===================================

            def continue_to_dashboard():

                success_window.destroy()

                # Import here to avoid circular import
                from gui.lecturer_dashboard import LecturerDashboard

                LecturerDashboard(
                    self.root,
                    fullname,
                    campus
                )

            tk.Button(
                success_window,
                text="Continue",
                bg="green",
                fg="white",
                width=20,
                command=continue_to_dashboard
            ).pack(pady=10)

            # ===================================
            # LOG OUT BUTTON
            # ===================================

            tk.Button(
                success_window,
                text="Log Out",
                bg="red",
                fg="white",
                width=20,
                command=self.root.destroy
            ).pack(pady=5)

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Registration Error",
                "Username already exists."
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )