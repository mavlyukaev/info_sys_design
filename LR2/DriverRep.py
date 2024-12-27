import json
import yaml
from Driver import Driver
from DriverRepDB import DriverRepDB

class DriverRep:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read()

    def read(self):
        pass

    def write(self):
        pass

    def get_by_id(self, driver_id):
        for driver in self.data:
            if driver.get_driver_id() == driver_id:
                return driver
        return None

    def get_k_n_short_list(self, k, n):
        start = (k - 1) * n
        end = start + n
        return [
            driver.short_version
            for driver in self.data[start:end]
        ]

    def sort_by_field(self, field):
        if not self.data:
            raise ValueError("Сортировка невозможна, так как список водителей пуст.")
        try:
            self.data.sort(key=lambda driver: getattr(driver, f"get_{field}")())
        except AttributeError:
            raise ValueError(f"Поле {field} не существует в классе Driver.")
        self.write()

    def is_unique(self, driver, exclude_id=None):
        for current_driver in self.data:
            if exclude_id is not None and current_driver.get_driver_id() == exclude_id:
                continue
            if current_driver == driver:
                return False
        return True

    def add(self, driver):
        if not isinstance(driver, Driver):
            raise ValueError("Ожидается объект класса Driver.")
        if not self.is_unique(driver):
            raise ValueError(f"Объект с номером телефона {driver.get_phone_number()} уже существует.")

        new_id = max((driver.get_driver_id() for driver in self.data), default=0) + 1
        driver.set_driver_id(new_id)
        self.data.append(driver)
        self.write()
        return new_id
    
    def update_by_id(self, driver_id, new_driver):
        if not isinstance(new_driver, Driver):
            raise ValueError("Ожидается объект класса Driver.")
        if not self.is_unique(new_driver, exclude_id=driver_id):
            raise ValueError(f"Объект с номером телефона {new_driver.get_phone_number()} уже существует.")

        for index, driver in enumerate(self.data):
            if driver.get_driver_id() == driver_id:
                new_driver.set_driver_id(driver_id)
                self.data[index] = new_driver
                self.write()
                return True
        raise ValueError(f"Водитель с ID {driver_id} не найден.")

    def delete_by_id(self, driver_id):
        self.data = [driver for driver in self.data if driver.get_driver_id() != driver_id]
        self.write()

    def get_count(self):
        return len(self.data)

class DriverRepJSON(DriverRep):
    def read(self):
        try:
            with open(self.file_path, 'r') as file:
                raw_data = json.load(file)
                return [Driver.from_dict(item) for item in raw_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump([driver.to_dict() for driver in self.data], file, indent=4, ensure_ascii=False)

class DriverRepYAML(DriverRep):
    def read(self):
        try:
            with open(self.file_path, 'r') as file:
                raw_data = yaml.safe_load(file) or []
                return [Driver.from_dict(item) for item in raw_data]
        except FileNotFoundError:
            return []

    def write(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            yaml.dump([driver.to_dict() for driver in self.data], file, default_flow_style=False, allow_unicode=True)
            
class DriverRepDBAdapter(DriverRep):
    def __init__(self, db_path):
        self.driver_rep_db = DriverRepDB(db_path)

    def read(self):
        return [
            self.driver_rep_db.get_by_id(driver_id)
            for driver_id in range(1, self.driver_rep_db.get_count() + 1)
        ]

    def write(self):
        pass

    def get_by_id(self, driver_id):
        return self.driver_rep_db.get_by_id(driver_id)

    def get_k_n_short_list(self, k, n):
        return self.driver_rep_db.get_k_n_short_list(k, n)

    def add(self, driver):
        return self.driver_rep_db.add(driver)

    def update_by_id(self, driver_id, new_driver):
        return self.driver_rep_db.update_by_id(driver_id, new_driver)

    def delete_by_id(self, driver_id):
        return self.driver_rep_db.delete_by_id(driver_id)

    def get_count(self):
        return self.driver_rep_db.get_count()
