from Model import DriverModel
from Controller import DriverController
from View import DriverView
from DriverRepDB import DriverRepDB

if __name__ == "__main__":
    # Инициализация базы данных
    db_path = "drivers.db"
    repository = DriverRepDB(db_path)

    # Создание модели
    model = DriverModel(repository)

    # Создание окна приложения
    app = DriverView

    # Создание контроллера
    app = DriverView(None)  
    controller = DriverController(model, app)  
    app.controller = controller 

    app.mainloop()
