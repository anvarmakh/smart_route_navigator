# Управление связью компаний и водителей

class Driver:
    """Пример класса Driver без ORM (заглушка)"""
    def __init__(self, id, name, company_id):
        self.id = id
        self.name = name
        self.company_id = company_id

# Имитируем базу данных
drivers_db = [Driver(1, "John", 100), Driver(2, "Alice", 100)]

def get_drivers(company_id: int):
    """Возвращает список водителей, привязанных к указанной компании"""
    return [d.__dict__ for d in drivers_db if d.company_id == company_id]

def add_driver(company_id: int, driver_data: dict):
    """Создаёт нового водителя и добавляет его в имитированную БД"""
    new_id = max(d.id for d in drivers_db) + 1
    new_driver = Driver(new_id, driver_data["name"], company_id)
    drivers_db.append(new_driver)
    return new_driver.__dict__