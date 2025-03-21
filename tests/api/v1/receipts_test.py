from decimal import Decimal
from uuid import uuid4

from tests.conftest import client


def test_create_receipt():
    response = client.post(
        "api/v1/receipts",
        headers=client.app_state["auth_headers"],
        json={
            "products": [
                {
                  "name": "Apple",
                  "price": 7.2,
                  "quantity": 3
                },
                {
                    "name": "Banana",
                    "price": 9.1,
                    "quantity": 4
                }
            ],
            "payment": {
                "type": "cash",
                "amount": 65.5
            }
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert Decimal(data["products"][0]["total"]) == Decimal('21.6')
    assert Decimal(data["products"][1]["total"]) == Decimal('36.4')
    assert Decimal(data["total"]) == Decimal('58.0')
    assert Decimal(data["rest"]) == Decimal('7.5')

    client.app_state["receipt"] = data
    client.app_state["receipt_id"] = data["id"]

    client.post(
        "api/v1/receipts",
        headers=client.app_state["auth_headers"],
        json={
            "products": [
                {
                    "name": "Apple",
                    "price": 7.2,
                    "quantity": 3
                },
                {
                    "name": "Banana",
                    "price": 900.1,
                    "quantity": 4
                }
            ],
            "payment": {
                "type": "cash",
                "amount": 6500.5
            }
        }
    )


def test_get_all_receipts():
    response = client.get(
        "api/v1/receipts?limit=1",
        headers=client.app_state["auth_headers"]
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["results"]) == 1
    assert data["results"][0] == client.app_state["receipt"]

    response = client.get(
        "api/v1/receipts?filters=total__gt=1000",
        headers=client.app_state["auth_headers"]
    )

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1


def test_get_receipt_by_id():
    response = client.get(
        f"api/v1/receipts/{client.app_state['receipt_id']}"
    )

    assert response.status_code == 200


def test_bad_requests():
    response = client.post(
        "api/v1/receipts",
        headers=client.app_state["auth_headers"],
        json={
            "product": [],
            "payments": {}
        }
    )

    assert response.status_code == 422

    response = client.post(
        "api/v1/receipts",
        headers=client.app_state["auth_headers"],
        json={
            "products": [
                {
                    "name": "Apple",
                    "price": 7.2,
                    "quantity": 3
                },
                {
                    "name": "Banana",
                    "price": 9.1,
                    "quantity": 4
                }
            ],
            "payment": {
                "type": "cash",
                "amount": 50
            }
        }
    )

    assert response.status_code == 400

    response = client.get(
        f"api/v1/receipts/{uuid4()}",
        headers=client.app_state["auth_headers"]
    )

    assert response.status_code == 404
