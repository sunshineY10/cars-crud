def test_post_car_returns_201_and_json(client):
    payload = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 2018,
        "color": "Black",
    }
    response = client.post("/api/cars", json=payload)
    assert response.status_code == 201
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert car["model"] == "Fiesta"
    assert response.headers["location"] == f"/api/cars/{car['id']}"
def test_invalid_year_is_not_saved(client):
    # 发送非法年份的创建请求
    payload = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 1800,
        "color": "Black",
    }
    response = client.post("/api/cars", json=payload)
    # 验证返回422状态码
    assert response.status_code == 422
    # 验证车辆列表为空
    get_response = client.get("/api/cars")
    assert get_response.json() == []