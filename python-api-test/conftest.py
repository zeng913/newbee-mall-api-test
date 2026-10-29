"""
pytest的特殊配置文件，可以定义供多个测试复用的 Fixture
pytest 特殊文件，放在同目录，里面的 fixture 不用 import，所有测试文件直接拿来用
"""

import pytest
import requests


from config import BASE_URL, TEST_LOGIN_NAME, TEST_PASSWORD_MD5

@pytest.fixture   #定义一个可复用步骤，所有用例共用同一个 token，不用每个用例都登录一遍，效率高
def login_token(scope="session"):   #这里scope="session"表示整个测试会话只执行一次，返回的 token 会被同一个测试会话中的所有测试用例复用
    #组装接口地址、账号密码参数、发送post请求
    url = f"{BASE_URL}/api/v1/user/login"

    payload = {
        "loginName": TEST_LOGIN_NAME,
        "passwordMd5": TEST_PASSWORD_MD5
    }

    response = requests.post(url, json=payload, timeout=10)

    #登录接口前置校验，如果校验失败直接跳过后面依赖login_token的测试用例，避免后续报错
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == 200
    assert data["message"] == "SUCCESS"

    #额外校验token是否符合预期，长度32位
    token = data["data"]
    assert isinstance(token, str) and len(token) == 32
    #返回token给依赖的测试用例使用
    return token


@pytest.fixture   #定义一个可复用步骤，所有用例共用同一个购物车清理逻辑，不用每个用例都写清理逻辑，效率高
def cart_clean(login_token):
    """记录原有购物项，并在测试结束后清理新增购物项。"""
    headers = {"token": login_token}
    page_url = f"{BASE_URL}/api/v1/shop-cart/page"

    def get_cart_items():
        """获取购物车第一页，并检查响应。"""
        response = requests.get(
            page_url,
            params={"pageNumber": 1},
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        assert data["resultCode"] == 200, (
            f"查询购物车失败：{data}"
        )
        return data["data"]["list"]

    # 前置：记录测试前已有的购物项 ID
    before_ids = {
        item["cartItemId"]
        for item in get_cart_items()
    }

    yield   # 这里的 yield 表示前置步骤执行完毕，去跑测试，测试用例执行完毕后会继续执行 yield 后面的清理逻辑

    # 后置：只清理测试期间新增的购物项
    after_items = get_cart_items()
    new_ids = {
        item["cartItemId"]
        for item in after_items
        if item["cartItemId"] not in before_ids
    }

    for cart_item_id in new_ids:
        response = requests.delete(
            f"{BASE_URL}/api/v1/shop-cart/{cart_item_id}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        result = response.json()
        assert result["resultCode"] == 200, (
            f"清理购物项 {cart_item_id} 失败：{result}"
        )