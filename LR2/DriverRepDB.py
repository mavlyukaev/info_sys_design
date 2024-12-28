import sqlite3
from Driver import Driver

class DatabaseManager:
    _instance = None

    def __new__(cls, db_path):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_path = db_path
            cls._instance._initialize_db()
        return cls._instance

    def __init__(self, db_path):
        self.db_path = db_path

    def _initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS drivers (
                    driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    last_name TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    patronymic TEXT NOT NULL,
                    phone_number TEXT NOT NULL UNIQUE,
                    experience INTEGER NOT NULL,
                    birthday TEXT NOT NULL,
                    driver_license TEXT NOT NULL,
                    vehicle_title TEXT NOT NULL,
                    insurance_policy TEXT NOT NULL,
                    license_plate TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def execute(self, query, parameters=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters or ())
            conn.commit()
            return cursor

    def fetchall(self, query, parameters=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters or ())
            return cursor.fetchall()

    def fetchone(self, query, parameters=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters or ())
            return cursor.fetchone()


class DriverRepDB:
    def __init__(self, db_path):
        self.db = DatabaseManager(db_path)
        
    def get_all_drivers(self):
        query = "SELECT * FROM drivers"
        rows = self.db.fetchall(query)
        return [
            Driver.from_dict({
                "driver_id": row[0],
                "last_name": row[1],
                "first_name": row[2],
                "patronymic": row[3],
                "phone_number": row[4],
                "experience": row[5],
                "birthday": row[6],
                "driver_license": row[7],
                "vehicle_title": row[8],
                "insurance_policy": row[9],
                "license_plate": row[10],
            }) for row in rows
        ]

    def get_by_id(self, driver_id):
        query = "SELECT * FROM drivers WHERE driver_id = ?"
        row = self.db.fetchone(query, (driver_id,))
        if row:
            return Driver.from_dict({
                "driver_id": row[0],
                "last_name": row[1],
                "first_name": row[2],
                "patronymic": row[3],
                "phone_number": row[4],
                "experience": row[5],
                "birthday": row[6],
                "driver_license": row[7],
                "vehicle_title": row[8],
                "insurance_policy": row[9],
                "license_plate": row[10],
            })
        return None

    def get_k_n_short_list(self, k, n):
        start = (k - 1) * n
        query = "SELECT last_name, first_name, patronymic, phone_number, experience FROM drivers LIMIT ? OFFSET ?"
        rows = self.db.fetchall(query, (n, start))
        return [(row[0], row[1], row[2], row[3], row[4]) for row in rows]

    def add(self, driver):
        query = """
        INSERT INTO drivers (
            last_name, first_name, patronymic, phone_number,
            experience, birthday, driver_license, vehicle_title,
            insurance_policy, license_plate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        parameters = (
            driver.get_last_name(),
            driver.get_first_name(),
            driver.get_patronymic(),
            driver.get_phone_number(),
            driver.get_experience(),
            driver.get_birthday(),
            driver.get_driver_license(),
            driver.get_vehicle_title(),
            driver.get_insurance_policy(),
            driver.get_license_plate(),
        )
        cursor = self.db.execute(query, parameters)
        return cursor.lastrowid

    def update_by_id(self, driver_id, new_driver):
        query = """
        UPDATE drivers
        SET last_name = ?, first_name = ?, patronymic = ?, phone_number = ?,
            experience = ?, birthday = ?, driver_license = ?, vehicle_title = ?,
            insurance_policy = ?, license_plate = ?
        WHERE driver_id = ?
        """
        parameters = (
            new_driver.get_last_name(),
            new_driver.get_first_name(),
            new_driver.get_patronymic(),
            new_driver.get_phone_number(),
            new_driver.get_experience(),
            new_driver.get_birthday(),
            new_driver.get_driver_license(),
            new_driver.get_vehicle_title(),
            new_driver.get_insurance_policy(),
            new_driver.get_license_plate(),
            driver_id,
        )
        cursor = self.db.execute(query, parameters)
        if cursor.rowcount == 0:
            raise ValueError(f"Водитель с ID {driver_id} не найден.")

    def delete_by_id(self, driver_id):
        query = "DELETE FROM drivers WHERE driver_id = ?"
        cursor = self.db.execute(query, (driver_id,))
        if cursor.rowcount == 0:
            raise ValueError(f"Водитель с ID {driver_id} не найден.")

    def get_count(self):
        query = "SELECT COUNT(*) FROM drivers"
        return self.db.fetchone(query)[0]
