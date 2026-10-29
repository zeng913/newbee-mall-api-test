import requests


def test_home_index_infos():
    url = "http://localhost:28019/api/v1/index-infos"

    response = requests.get(url, timeout=10)

    assert response.status_code == 200

    data = response.json()

    assert data["resultCode"] == 200
    assert data["message"] == "SUCCESS"
    assert data.get("data") is not None
