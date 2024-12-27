import tkinter as tk
from tkinter import ttk

class DriverView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Управление водителями")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.table = ttk.Treeview(
            self,
            columns=("ID", "Фамилия", "Имя", "Отчество", "Телефон", "Стаж"),
            show="headings"
        )
        self.table.heading("ID", text="ID")
        self.table.heading("Фамилия", text="Фамилия")
        self.table.heading("Имя", text="Имя")
        self.table.heading("Отчество", text="Отчество")
        self.table.heading("Телефон", text="Телефон")
        self.table.heading("Стаж", text="Стаж")
        self.table.bind("<Double-1>", self.open_driver_details)
        self.table.pack(fill=tk.BOTH, expand=True)

    def refresh(self, drivers):
        for row in self.table.get_children():
            self.table.delete(row)

        for driver in drivers:
            self.table.insert("", "end", values=(
                driver.get_driver_id(),
                driver.get_last_name(),
                driver.get_first_name(),
                driver.get_patronymic(),
                driver.get_phone_number(),
                driver.get_experience()
            ))

    def open_driver_details(self, event):
        selected_item = self.table.selection()
        if not selected_item:
            return
        driver_id = self.table.item(selected_item)["values"][0]
        self.controller.show_driver_details(driver_id)

class DriverFullView(tk.Toplevel):
    def __init__(self, controller, driver):
        super().__init__()
        self.controller = controller
        self.title(f"Информация о водителе ID: {driver.get_driver_id()}")
        self.geometry("500x400")

        details = {
            "Фамилия": driver.get_last_name(),
            "Имя": driver.get_first_name(),
            "Отчество": driver.get_patronymic(),
            "Телефон": driver.get_phone_number(),
            "Стаж": driver.get_experience(),
            "Дата рождения": driver.get_birthday(),
            "Вод. удостоверение": driver.get_driver_license(),
            "ПТС": driver.get_vehicle_title(),
            "Страховка": driver.get_insurance_policy(),
            "Номер авто": driver.get_license_plate()
        }

        for i, (label, value) in enumerate(details.items()):
            tk.Label(self, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(self, text=value).grid(row=i, column=1, sticky=tk.W, padx=10, pady=5)
