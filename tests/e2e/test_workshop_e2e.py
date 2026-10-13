import re
from playwright.sync_api import expect

def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()


def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 创建一辆 Honda Civic 2022
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_label("Color", exact=False).fill("Black")
    page.get_by_role("button", name="Create car").click()

    # 2. 点击编辑链接
    page.get_by_role("link", name="Edit car").click()

    # 等待编辑表单从服务器加载完成（避免异步填充覆盖后续输入）
    expect(page.get_by_label("Model", exact=True)).to_have_value("Civic")
    expect(page.get_by_label("Year", exact=True)).to_have_value("2022")

    # 3. 修改型号和年份
    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")
    page.get_by_role("button", name="Save changes").click()

    # 4. 验证页面标题更新
    expect(page.get_by_role("heading", name="Honda Accord")).to_be_visible()

    # 5. 刷新页面，验证修改仍然保留
    page.reload()
    expect(page.get_by_role("heading", name="Honda Accord")).to_be_visible()
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")