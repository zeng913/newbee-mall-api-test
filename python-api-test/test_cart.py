import requests
import pytest

"""测试购物车相关接口,将接口拆开成多个测试函数，方便后续维护和扩展"""

from config import BASE_URL


def test_add_cart(login_token,cart_clean):
    """正常添加商品"""
    response = requests.post(
        f"{BASE_URL}/api/v1/shop-cart",
        json={"goodsId": 10893, "goodsCount": 1},
        headers={"token": login_token},
        timeout=10
    )

    assert response.status_code == 200
    assert response.json()["resultCode"] == 200

def test_add_cart_without_token():
    """未登录添加商品"""
    response = requests.post(
        f"{BASE_URL}/api/v1/shop-cart",
        json={"goodsId": 10893, "goodsCount": 1},
        #这里不传token，模拟未登录的情况
        timeout=10
    )

    assert response.json()["resultCode"] == 416   #不传token，返回的resultCode是416

def test_add_cart_invalid_goods(login_token):
    """添加不存在的商品"""
    response = requests.post(
        f"{BASE_URL}/api/v1/shop-cart",
        json={"goodsId": 99999999, "goodsCount": 1},
        headers={"token": login_token},
        timeout=10
    )

    assert response.status_code == 200
    assert response.json()["resultCode"] == 500
    assert response.json()["message"] == "商品不存在！"

def test_add_cart_invalid_count(login_token):
    """添加商品数量为负数"""
    response = requests.post(
        f"{BASE_URL}/api/v1/shop-cart",
        json={"goodsId": 10894, "goodsCount": -1},
        headers={"token": login_token},
        timeout=10
    )

    assert response.status_code == 200
    assert response.json()["resultCode"] == 500
    assert response.json()["message"] == "商品数量不能小于 1 ！"

def test_add_cart_invalid_goods_and_count(login_token):
    """添加不存在的商品，数量为负数"""
    response = requests.post(
        f"{BASE_URL}/api/v1/shop-cart",
        json={"goodsId": 99999999, "goodsCount": -1},
        headers={"token": login_token},
        timeout=10
    )

    assert response.status_code == 200
    assert response.json()["resultCode"] == 500
    assert response.json()["message"] == "商品不存在！"

def test_query_cart(login_token):
    """查询购物车"""
    response = requests.get(
        f"{BASE_URL}/api/v1/shop-cart/page",
        params={"pageNumber": 1},
        headers={"token": login_token},
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()
    assert data["resultCode"] == 200
    assert isinstance(data["data"]["list"], list)

def test_query_cart_without_token():
    """未登录查询购物车"""
    response = requests.get(
        f"{BASE_URL}/api/v1/shop-cart/page",
        params={"pageNumber": 1},
        #这里不传token，模拟未登录的情况
        timeout=10
    )

    assert response.json()["resultCode"] == 416   #不传token，返回的resultCode是416

def test_query_cart_invalid_page(login_token):
    """查询购物车，页码为负数，自动校正到第一页"""
    response = requests.get(
        f"{BASE_URL}/api/v1/shop-cart/page",
        params={"pageNumber": -1},
        headers={"token": login_token},
        timeout=10
    )
    print("响应json：", response.json())

    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == 200
    assert data["data"]["currPage"] == 1


def test_delete_cart(login_token, cart_clean):
    """删除购物项：先添加，再找到对应 ID，最后删除"""
    headers = {"token": login_token}

    # 先添加一个测试商品
    requests.post(
        f"{BASE_URL}/api/v1/shop-cart",
        json={"goodsId": 10893, "goodsCount": 1},
        headers=headers,
        timeout=10
    ).raise_for_status()

    # 查询并找到对应购物项
    response = requests.get(
        f"{BASE_URL}/api/v1/shop-cart/page",
        params={"pageNumber": 1},
        headers=headers,
        timeout=10
    )
    assert response.status_code == 200

    items = response.json()["data"]["list"]
    item = next(
        (x for x in items if x["goodsId"] == 10893),
        None
    )
    assert item is not None, "未找到刚添加的购物项"

    cart_item_id = item["cartItemId"]

    # 删除购物项
    delete_response = requests.delete(
        f"{BASE_URL}/api/v1/shop-cart/{cart_item_id}",
        headers=headers,
        timeout=10
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["resultCode"] == 200

def test_delete_cart_without_token():
    """未登录删除购物项"""
    response = requests.delete(
        f"{BASE_URL}/api/v1/shop-cart/1",  #这里随便传一个购物项ID，模拟未登录的情况
        timeout=10
    )

    assert response.json()["resultCode"] == 416   #不传token，返回的resultCode是416

def test_delete_cart_invalid_id(login_token):
    """删除不存在的购物项"""
    response = requests.delete(
        f"{BASE_URL}/api/v1/shop-cart/99999999",  #这里传一个不存在的购物项ID
        headers={"token": login_token},
        timeout=10
    )

    assert response.status_code == 200
    assert response.json()["resultCode"] == 500
    assert response.json()["message"] == "未查询到记录！"