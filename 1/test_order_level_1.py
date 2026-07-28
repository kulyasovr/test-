from api_client import send_request

def test_create_and_check_order():
    create_resp = send_request("POST", "/orders", {
        "product_id": 1,
        "quantity": 2
    })
    assert create_resp.status_code == 201
    
    data = create_resp.json()
    assert "order_id" in data
    
    order_id = data["order_id"]
    get_resp = send_request("GET", f"/orders/{order_id}")
    assert get_resp.status_code == 200

    order_data = get_resp.json()
    assert order_data["id"] == order_id
    assert order_data["product_id"] == 1
    assert order_data["quantity"] == 2

    assert order_data["status"] == "new"
