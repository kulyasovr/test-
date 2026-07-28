import pytest
from api_client import send_request

@pytest.fixture
def new_order():
    resp = send_request("POST", "/orders", {"product_id": 42, "quantity": 5})
    assert resp.status_code == 201
    yield resp.json()["order_id"]


def test_can_pay_for_existing_order(new_order):
    pay_resp = send_request("POST", f"/orders/{new_order}/pay")
    assert pay_resp.status_code == 200
    assert pay_resp.json()["paid"] is True

    check_resp = send_request("GET", f"/orders/{new_order}")
    assert check_resp.json()["status"] == "paid"


@pytest.mark.parametrize("bad_quantity", [0, -5, 99999])
def test_cannot_create_order_with_bad_quantity(bad_quantity):
    resp = send_request("POST", "/orders", {
        "product_id": 1,
        "quantity": bad_quantity
    })
    
    assert resp.status_code == 400
    
    error_text = resp.text.lower()
    if bad_quantity <= 0:
        assert "must be greater than 0" in error_text
    elif bad_quantity > 1000:
        assert "out of stock" in error_text