from app import database
from app.schemas import CarInput

def test_saved_car_can_be_read_from_sqlite(database_path):
    database.initialize(database_path)
    saved = database.create_car(
        database_path,
        CarInput(make="Toyota", model="Yaris", year=2020, color="Blue"),
    )
    loaded = database.get_car(database_path, saved.id)

    assert loaded is not None
    assert loaded.id == saved.id
    assert loaded.make == "Toyota"
    assert loaded.year == 2020
def test_deleting_one_car_keeps_the_other(database_path):
    database.initialize(database_path)
    # 创建两辆不同的车
    car1 = database.create_car(
        database_path,
        CarInput(make="Toyota", model="Yaris", year=2020, color="Blue")
    )
    car2 = database.create_car(
        database_path,
        CarInput(make="Honda", model="Civic", year=2022, color="Red")
    )
    # 删除第一辆车
    database.delete_car(database_path, car1.id)
    # 验证第一辆已删除
    assert database.get_car(database_path, car1.id) is None
    # 验证第二辆仍存在
    assert database.get_car(database_path, car2.id) is not None
    # 验证列表只剩1辆车
    all_cars = database.list_cars(database_path)
    assert len(all_cars) == 1