from DriverRepDB import DriverRepDB

class DriverModel:
    def __init__(self, repository):
        self.repository = repository
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        drivers = self.get_all_drivers()
        for observer in self.observers:
            observer.refresh(drivers)

    def get_all_drivers(self):
        return self.repository.get_all_drivers()

    def get_driver_by_id(self, driver_id):
        return self.repository.get_by_id(driver_id)
