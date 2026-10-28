import tkinter as tk
from tkinter import messagebox

from users import login
from gui.register import RegisterWindow
from gui.lecturer_dashboard import LecturerDashboard
from gui.admin_dashboard import AdminDashboard
from gui.operator_dashboard import OperatorDashboard


class LoginWindow:

    def __init__(self, root):

        self.root = root

        self.root.title("Smart Campus Resource Booking System")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Heading
        tk.Label(
            root,
            text="SMART CAMPUS RESOURCE BOOKING SYSTEM",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # Username
        tk.Label(
            root,
            text="Username"
        ).pack()

        self.username = tk.Entry(
            root,
            width=30
        )
        self.username.pack(pady=5)

        # Password
        tk.Label(
            root,
            text="Password"
        ).pack()

        self.password = tk.Entry(
            root,
            show="*",
            width=30
        )
        self.password.pack(pady=5)

        # Login Button
        tk.Button(
            root,
            text="Login",
            bg="green",
            fg="white",
            width=20,
            command=self.do_login
        ).pack(pady=10)

        # Register Button
        tk.Button(
            root,
            text="Register Lecturer Account",
            bg="blue",
            fg="white",
            width=25,
            command=self.open_register
        ).pack(pady=5)

    # ==================================
    # OPEN REGISTER WINDOW
    # ==================================

    def open_register(self):

        RegisterWindow(self.root)

    # ==================================
    # LOGIN USER
    # ==================================

    def do_login(self):

        username = self.username.get().strip()
        password = self.password.get().strip()

        if username == "" or password == "":

            messagebox.showerror(
                "Login Error",
                "Please enter username and password."
            )
            return

        user = login(username, password)

        if user is None:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )
            return

        fullname = user[1]
        role = user[4]
        campus = user[5]

        messagebox.showinfo(
            "Login Successful",
            f"Welcome {fullname}"
        )

        # Hide Login Window
        self.root.withdraw()

        # Lecturer Dashboard
        if role == "Lecturer":

            LecturerDashboard(
                self.root,
                fullname,
                campus
            )

        # Campus Administrator Dashboard
        elif role == "CampusAdministrator":

            AdminDashboard(
                self.root
            )

        # System Operator Dashboard
        elif role == "SystemOperator":

            OperatorDashboard(
                self.root
            )

        else:

            messagebox.showerror(
                "Role Error",
                f"Unknown user role: {role}"
            )

            self.root.deiconify()