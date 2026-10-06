import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, ttk


class HospitalManagementSystem(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Hospital Management System - Portal")
        self.geometry("500x550")
        self.config(bg="#f4f6f9")

        # User database including doctor credentials
        self.users = {
            "admin": {"password": "pass123", "name": "Hospital Admin"},
            "doctor": {"password": "doc123", "name": "Dr. Smith"},
            "reception": {"password": "rec123", "name": "Front Desk"},
        }

        self.container = tk.Frame(self, bg="#f4f6f9")
        self.container.pack(fill="both", expand=True)

        self.show_login_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_container()

        title_label = tk.Label(
            self.container,
            text="Hospital Management System",
            font=("Arial", 20, "bold"),
            bg="#f4f6f9",
            fg="#2c3e50",
        )
        title_label.pack(pady=(40, 10))

        subtitle_label = tk.Label(
            self.container,
            text="Please log in to your account",
            font=("Arial", 11),
            bg="#f4f6f9",
            fg="#7f8c8d",
        )
        subtitle_label.pack(pady=(0, 20))

        login_frame = tk.Frame(
            self.container, bg="#ffffff", padx=30, pady=30, relief="raised", bd=1
        )
        login_frame.pack(padx=40, pady=10, fill="x")

        tk.Label(
            login_frame,
            text="Username:",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
        ).pack(anchor="w", pady=(0, 5))
        self.entry_user = tk.Entry(login_frame, font=("Arial", 11), width=28)
        self.entry_user.pack(pady=(0, 15))
        self.entry_user.insert(0, "doctor")

        tk.Label(
            login_frame,
            text="Password:",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
        ).pack(anchor="w", pady=(0, 5))
        self.entry_pass = tk.Entry(
            login_frame, font=("Arial", 11), width=28, show="*"
        )
        self.entry_pass.pack(pady=(0, 15))
        self.entry_pass.insert(0, "doc123")

        btn_login = tk.Button(
            login_frame,
            text="Login",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            width=24,
            pady=8,
            command=self.handle_login,
        )
        btn_login.pack(pady=(5, 10))

        btn_forgot = tk.Button(
            login_frame,
            text="Forgotten Password?",
            bg="#ffffff",
            fg="#2980b9",
            font=("Arial", 9, "underline"),
            bd=0,
            cursor="hand2",
            command=self.handle_forgot_password,
        )
        btn_forgot.pack()

        footer_label = tk.Label(
            self.container,
            text="DEVELOPED BY - FEYI GROUP LTD",
            font=("Arial", 15, "italic"),
            bg="#f4f6f9",
            fg="#95a5a6",
        )
        footer_label.pack(pady=30)

    def handle_login(self):
        username = self.entry_user.get().strip().lower()
        password = self.entry_pass.get().strip()

        if (
            username in self.users
            and self.users[username]["password"] == password
        ):
            messagebox.showinfo(
                "Login Success",
                f"Welcome, {self.users[username]['name']}!",
            )
            self.show_main_dashboard()
        else:
            messagebox.showerror(
                "Login Failed", "Invalid username or password. Please try again."
            )

    def handle_forgot_password(self):
        messagebox.showinfo(
            "Password Recovery",
            "Password reset instructions have been sent to your registered email address.",
        )

    def show_main_dashboard(self):
        self.clear_container()

        title_label = tk.Label(
            self.container,
            text="Hospital Management System",
            font=("Arial", 18, "bold"),
            bg="#f4f6f9",
            fg="#2c3e50",
        )
        title_label.pack(pady=20)

        subtitle_label = tk.Label(
            self.container,
            text="Select a section to open:",
            font=("Arial", 15),
            bg="#f4f6f9",
            fg="#7f8c8d",
        )
        subtitle_label.pack(pady=(0, 20))

        menu_frame = tk.Frame(self.container, bg="#ffffff", padx=20, pady=20)
        menu_frame.pack(padx=30, pady=10, fill="both", expand=True)

        btn_reg = tk.Button(
            menu_frame,
            text=" Patient Registration",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            width=32,
            pady=10,
            command=lambda: self.open_module("patient_registration"),
        )
        btn_reg.pack(pady=10)

        btn_appt = tk.Button(
            menu_frame,
            text=" Appointment Booking",
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            width=32,
            pady=10,
            command=lambda: self.open_module("appointment_booking"),
        )
        btn_appt.pack(pady=10)

        btn_doc = tk.Button(
            menu_frame,
            text=" Doctor Dashboard",
            bg="#9b59b6",
            fg="white",
            font=("Arial", 11, "bold"),
            width=32,
            pady=10,
            command=lambda: self.open_module("doctor_dashboard"),
        )
        btn_doc.pack(pady=10)

        btn_bill = tk.Button(
            menu_frame,
            text=" Billing & Payment",
            bg="#f39c12",
            fg="white",
            font=("Arial", 11, "bold"),
            width=32,
            pady=10,
            command=lambda: self.open_module("billing"),
        )
        btn_bill.pack(pady=10)

        btn_logout = tk.Button(
            menu_frame,
            text="Log Out",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=32,
            pady=8,
            command=self.show_login_screen,
        )
        btn_logout.pack(pady=(15, 5))

        footer_label = tk.Label(
            self.container,
            text="FEYI GROUP LTD ",
            font=("Arial", 9, "italic"),
            bg="#f4f6f9",
            fg="#95a5a6",
        )
        footer_label.pack(pady=15)

    def open_module(self, module_name):
        """Function to launch individual sections as separate subprocesses."""
        try:
            subprocess.Popen([sys.executable, f"{module_name}.py"])
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not launch section {module_name}.\nError: {e}",
            )


if __name__ == "__main__":
    app = HospitalManagementSystem()
    app.mainloop()
