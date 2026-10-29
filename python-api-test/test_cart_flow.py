
import requests

from config import BASE_URL


def test_cart_flow(login_token):  #这里是一个测试用例，最后判断paased也是这个测试用例
    headers = {"token": login_token}

    # 1. 添加商品到购物车
    #请求地址
    add_url = f"{BASE_URL}/api/v1/shop-cart"
    #请求参数，payload传的是json格式的请求体，里面包含商品id和数量
    payload = {
        "goodsId": 10893,
        "goodsCount": 1
    }

    add_response = requests.post(
        add_url,
        json=payload,
        headers=headers,
        timeout=10
    )

    assert add_response.status_code == 200
    assert add_response.json()["resultCode"] == 200

    # 2. 查询购物车
    page_url = f"{BASE_URL}/api/v1/shop-cart/page"
    params = {"pageNumber": 1}

    page_response = requests.get(
        page_url,
        params=params,
        headers=headers,
        timeout=10
    )

    assert page_response.status_code == 200

    page_data = page_response.json()
    assert page_data["resultCode"] == 200

    cart_items = page_data["data"]["list"]
    
    """
    生成器是一种特殊的迭代器，它可以在迭代过程中动态生成值，而不是一次性生成所有值。
    生成器表达式类似于列表推导式，但它使用圆括号而不是方括号，并且不会立即计算所有值，而是按需生成值。这使得生成器在处理大量数据时更加高效，因为它们不会占用大量内存。
    
    在这个例子中，生成器表达式 `(x for x in cart_items if x["goodsId"] == 10893)` 会遍历 `cart_items` 列表
    并在每次迭代时检查每个购物项的 `goodsId` 是否等于 `10893`， 如果条件为真，它会生成该购物项 `x`
    `next()` 函数会返回生成器的下一个值，如果没有更多的值可生成，则返回 `None`（通过指定默认值）
    
    等价于for循环遍历cart_items，找到goodsId为10893的商品，如果找到了就返回该商品，否则返回None
    """
    
    item = next(
        (x for x in cart_items if x["goodsId"] == 10893),   #生成器表达式，找到购物车中goodsId为10893的商品
        None
    )
    assert item is not None, "添加后未在购物车中找到商品"

    # 3. 删除购物项
    cart_item_id = item["cartItemId"]
    delete_url = f"{BASE_URL}/api/v1/shop-cart/{cart_item_id}"

    delete_response = requests.delete(
        delete_url,
        headers=headers,
        timeout=10
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["resultCode"] == 200

    # 4. 再次查询，验证商品已删除
    verify_response = requests.get(
        page_url,
        params=params,
        headers=headers,
        timeout=10
    )

    assert verify_response.status_code == 200

    verify_data = verify_response.json()
    assert verify_data["resultCode"] == 200

    remaining_items = verify_data["data"]["list"]
    assert not any(
        x["cartItemId"] == cart_item_id
        for x in remaining_items
    ), "删除后购物项仍然存在"
