import requests


def test_login():
    url = "http://localhost:28019/api/v1/user/login"

    payload = {
        "loginName": "15768091392",
        "passwordMd5": "e10adc3949ba59abbe56e057f20f883e"
    }

    response = requests.post(url, json=payload, timeout=10)


    print("HTTP状态码：", response.status_code)
    print("响应内容：", response.text)

    assert response.status_code == 200

    data = response.json()

    assert data["resultCode"] == 200
    assert data["message"] == "SUCCESS"
    assert isinstance(data["data"], str)
    assert len(data["data"]) == 32
