import re

class BaseDriver:
    def __init__(self, last_name, first_name, patronymic, phone_number, experience, driver_id=None):
        self.set_driver_id(driver_id)
        self.set_last_name(last_name)
        self.set_first_name(first_name)
        self.set_patronymic(patronymic)
        self.set_phone_number(phone_number)
        self.set_experience(experience)

    @staticmethod
    def validate_driver_id(driver_id):
        if not isinstance(driver_id, int) or driver_id <= 0:
            return False
        return True
    
    @staticmethod
    def validate_last_name(last_name):
        if not isinstance(last_name, str) or len(last_name.strip()) == 0:
            return False
        return True

    @staticmethod
    def validate_first_name(first_name):
        if not isinstance(first_name, str) or len(first_name.strip()) == 0:
            return False
        return True

    @staticmethod
    def validate_patronymic(patronymic):
        if not isinstance(patronymic, str) or len(patronymic.strip()) == 0:
            return False
        return True
    
    @staticmethod
    def validate_phone_number(phone_number):
        if not isinstance(phone_number, str) or not re.fullmatch(r'(8|\+7)\d{10}', phone_number):
            return False
        return True

    @staticmethod
    def validate_experience(experience):
        if not isinstance(experience, int) or experience <= 0:
            return False
        return True
    
    # Геттеры
    def get_driver_id(self):
        return self.__driver_id

    def get_last_name(self):
        return self.__last_name

    def get_first_name(self):
        return self.__first_name

    def get_patronymic(self):
        return self.__patronymic
    
    def get_phone_number(self):
        return self.__phone_number

    def get_experience(self):
        return self.__experience
    
    # Сеттеры
    def set_driver_id(self, driver_id):
        if driver_id is not None and not self.validate_driver_id(driver_id):
            raise ValueError("ID должен быть положительным числом.") 
        self.__driver_id = driver_id

    def set_last_name(self, last_name):
        if not self.validate_last_name(last_name):
            raise ValueError("Фамилия не должна быть пустой.")
        self.__last_name = last_name

    def set_first_name(self, first_name):
        if not self.validate_first_name(first_name):
            raise ValueError("Имя не должно быть пустым.")
        self.__first_name = first_name

    def set_patronymic(self, patronymic):
        if not self.validate_patronymic(patronymic):
            raise ValueError("Отчество не должно быть пустым.")
        self.__patronymic = patronymic

    def set_phone_number(self, phone_number):
        if not self.validate_phone_number(phone_number):
            raise ValueError("Номер телефона написан неккоректно.")
        self.__phone_number = phone_number

    def set_experience(self, experience):
        if not self.validate_experience(experience):
            raise ValueError("Стаж не может быть меньше 1.")
        self.__experience = experience

    def __eq__(self, other):
        return (
            self.get_driver_id() == other.get_driver_id()
            and self.get_last_name() == other.get_last_name()
            and self.get_first_name() == other.get_first_name()
            and self.get_patronymic() == other.get_patronymic()
            and self.get_phone_number() == other.get_phone_number()
            and self.get_experience() == other.get_experience()
        )

    def __str__(self):
        return (
            f"Driver ID: {self.get_driver_id()}, Name: {self.get_last_name()} "
            f"{self.get_first_name()} {self.get_patronymic()}, "
            f"Phone number: {self.get_phone_number()}, "
            f"Experience: {self.get_experience()} years"
        )

    def __repr__(self):
        return (
            f"Driver(driver_id={self.get_driver_id()}, last_name='{self.get_last_name()}', "
            f"first_name='{self.get_first_name()}', patronymic='{self.get_patronymic()}', "
            f"phone_number='{self.get_phone_number()}', experience={self.get_experience()})"
        )
