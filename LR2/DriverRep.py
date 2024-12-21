import json
import yaml

class DriverRep:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._read()

    def _read(self):
        pass

    def _write(self):
        pass

    def get_by_id(self, driver_id):
        for key in self.data:
           if key['id'] == driver_id:
               return key
        return None

    def get_k_n_short_list(self, k, n):
        start = (k - 1) * n
        end = start + n
        return self.data[start:end]

    def sort_by_field(self, field):
        self.data.sort(key=lambda x: x.get(field, None))
        self._write()

    def add(self, driver):
        if any(item.get('phone_number') == driver.get('phone_number') for item in self.data):
            raise ValueError(f"Объект с номером телефона {driver.get('phone_number')} уже существует.")
        
        new_id = max((item.get('id', 0) for item in self.data), default=0) + 1

        driver['id'] = new_id
        self.data.append(driver)
        self._write()
        return new_id

    def update_by_id(self, driver_id, new_driver):
        if any(item.get('phone_number') == new_driver.get('phone_number') and item.get('id') != driver_id for item in self.data):
            raise ValueError(f"Объект с номером телефона {new_driver.get('phone_number')} уже существует.")
        
        for index, item in enumerate(self.data):
            if item.get('id') == driver_id:
                new_driver['id'] = driver_id
                self.data[index] = new_driver
                self._write()
                return True
        return False

    def delete_by_id(self, driver_id):
        self.data = [item for item in self.data if item.get('id') != driver_id]
        self._write()

    def get_count(self):
        return len(self.data)

class DriverRepJSON(DriverRep):
    def _read(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

class DriverRepYAML(DriverRep):
    def _read(self):
        try:
            with open(self.file_path, 'r') as file:
                return yaml.safe_load(file) or []
        except FileNotFoundError:
            return []

    def _write(self):
        with open(self.file_path, 'w') as file:
            yaml.dump(self.data, file, default_flow_style=False, allow_unicode=True)
