import pytest
import requests

#把服务基础地址抽成变量，后面拼接接口路径(见url）方便后续改环境，不用到处改 IP 端口
#这里的 BASE_URL 从config.py 配置文件里导入
from config import BASE_URL

#pytest 的**参数化装饰器**
#自动循环跑 3 次下面这个测试函数，每次传给 `goods_id` 一个值：
#参数后面是我们设置的预期结果
@pytest.mark.parametrize(
    "goods_id, expected_message",
    [
        (10893, "SUCCESS"),
        (99999999, "商品不存在！"),
        (-1, "参数异常"),
    ],
)

#定义测试函数，函数名以 `test_` 开头，pytest 才会识别它是测试用例
def test_goods_detail(goods_id, expected_message, login_token):
    url = f"{BASE_URL}/api/v1/goods/detail/{goods_id}"

    headers = {
        "token": login_token
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )
    
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == expected_message

    #返回的data里面取message判断是否和预期一致

