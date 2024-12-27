from View import DriverFullView

class DriverController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.add_observer(self)
        self.refresh_drivers()

    def refresh_drivers(self):
        drivers = self.model.get_all_drivers()
        self.view.refresh(drivers)

    def refresh(self, drivers):
        self.view.refresh(drivers)

    def show_driver_details(self, driver_id):
        driver = self.model.get_driver_by_id(driver_id)
        if driver:
            self.view = DriverFullView(self, driver)
