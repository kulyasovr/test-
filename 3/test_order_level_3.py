import pytest
from api_client import send_request

@pytest.fixture
def paid_order():
    created = send_request("POST", "/orders", {"product_id": 10, "quantity": 1})
    oid = created.json()["order_id"]

    send_request("POST", f"/orders/{oid}/pay")
    
    yield oid

def test_payment_is_idempotent(paid_order):
    oid = paid_order

    retry_1 = send_request("POST", f"/orders/{oid}/pay")
    assert retry_1.status_code == 200
    assert retry_1.json()["detail"] == "Order was already paid"

    retry_2 = send_request("POST", f"/orders/{oid}/pay")
    assert retry_2.status_code == 200
    assert retry_2.json()["detail"] == "Order was already paid"

    final_state = send_request("GET", f"/orders/{oid}").json()
    assert final_state["status"] == "paid"
    assert final_state["payment_attempts"] == 3 
