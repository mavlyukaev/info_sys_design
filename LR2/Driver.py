import re
import json
from BaseDriver import BaseDriver

class Driver(BaseDriver):
    def __init__(self, last_name, first_name, patronymic, phone_number, experience, birthday, driver_license, vehicle_title, insurance_policy, license_plate, driver_id = None):
        super().__init__(last_name, first_name, patronymic, phone_number, experience, driver_id)
        self.set_birthday(birthday) # Дата рождения
        self.set_driver_license(driver_license) # Водительское удостоверение
        self.set_vehicle_title(vehicle_title) # ПТС
        self.set_insurance_policy(insurance_policy) # Страховой полис
        self.set_license_plate(license_plate) # Номер машины
        
    # Классовый метод создания водителя из JSON
    @classmethod
    def from_json(cls, data_json):
        try:
            data = json.loads(data_json)
            return cls(
                last_name=data['last_name'],
                first_name=data['first_name'],
                patronymic=data['patronymic'],
                phone_number=data['phone_number'],
                experience=data['experience'],
                birthday=data['birthday'],
                driver_license=data['driver_license'],
                vehicle_title=data['vehicle_title'],
                insurance_policy=data['insurance_policy'],
                license_plate=data['license_plate'],
                driver_id=data.get('driver_id')
            )
        except KeyError as e:
            raise ValueError(f"Отсутствует обязательное поле: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Некорректный формат JSON: {e}")
        except Exception as e:
            raise ValueError(f"Ошибка при обработке JSON: {e}")

    @staticmethod
    def validate_birthday(birthday):
        if not isinstance(birthday, str) or not re.fullmatch(r'\d{2}\.\d{2}\.\d{4}', birthday):
            return False
        return True

    @staticmethod
    def validate_driver_license(driver_license):
        if not isinstance(driver_license, str) or not re.fullmatch(r"^\d{2} \d{2} \d{6}$", driver_license):
            return False
        return True

    @staticmethod
    def validate_vehicle_title(vehicle_title):
        if not isinstance(vehicle_title, str) or not re.fullmatch(r"^\d{2} \d{2} \d{6}$", vehicle_title):
            return False
        return True

    @staticmethod
    def validate_insurance_policy(insurance_policy):
        if not isinstance(insurance_policy, str) or not re.fullmatch(r"^\d{3} \d{12}$", insurance_policy):
            return False
        return True

    @staticmethod
    def validate_license_plate(license_plate):
        if not isinstance(license_plate, str) or not re.fullmatch(r"^[А-Я]{1}\d{3}[А-Я]{2}\s?\d{2,3}$", license_plate):
            return False
        return True

    @property
    def full_version(self):
        return (
            f"{self.get_last_name()} {self.get_first_name()} {self.get_patronymic()}",
            self.get_phone_number(),
            self.get_experience(),
            self.get_birthday(),
            self.get_driver_license(),
            self.get_vehicle_title(),
            self.get_insurance_policy(),
            self.get_license_plate(),
        )

    @property
    def short_version(self):
        return (
            f"{self.get_last_name()} {self.get_first_name()} {self.get_patronymic()}",
            self.get_phone_number(),
            self.get_experience()
        )

    # Геттеры
    def get_birthday(self):
        return self.__birthday

    def get_driver_license(self):
        return self.__driver_license

    def get_vehicle_title(self):
        return self.__vehicle_title

    def get_insurance_policy(self):
        return self.__insurance_policy

    def get_license_plate(self):
        return self.__license_plate

    # Сеттеры
    def set_birthday(self, birthday):
        if not self.validate_birthday(birthday):
            raise ValueError("Дата рождения должна быть в формате 'ДД.ММ.ГГГГ'.")
        self.__birthday = birthday

    def set_driver_license(self, driver_license):
        if not self.validate_driver_license(driver_license):
            raise ValueError("Водительское удостоверение должно быть в формате 'XX XX XXXXXX'.")
        self.__driver_license = driver_license

    def set_vehicle_title(self, vehicle_title):
        if not self.validate_vehicle_title(vehicle_title):
            raise ValueError("ПТС должен быть в формате 'XX XX XXXXXX'.")
        self.__vehicle_title = vehicle_title
        
    def set_insurance_policy(self, insurance_policy):
        if not self.validate_insurance_policy(insurance_policy):
            raise ValueError("Страховой полис должен быть в формате 'XXX XXXXXXXXXXXX'.")
        self.__insurance_policy = insurance_policy

    def set_license_plate(self, license_plate):
        if not self.validate_license_plate(license_plate):
            raise ValueError("Номера машины должны быть в формате 'Х111ХХ 111'.")
        self.__license_plate = license_plate
