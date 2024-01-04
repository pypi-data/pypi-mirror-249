# CashFree API Python Package

This Python package provides a simple interface to the CashFree APIs. It can be used to create orders, payment links, check the status of transactions, and refund orders etc
##### Note: Refer to the [cashfree api docs](https://docs.cashfree.com/reference/pg-new-apis-endpoint) for detailed payload instructions, API references, and examples.
## Installation

To install the package, run the following command:

```bash
pip install cashfree
```

## Usage

#### The following code shows how to create a CashFree Payment Session:
* Initiate Cashfree Object

```python
from cashfree import CashFree

# Instantiate CashFree object for the sandbox environment (TEST)
cashfree_client = CashFree(client_id, client_secret, environment="TEST", api_version='v3')
```

* Create A Customer Object
```python
from cashfree import CustomerDetails
customer = CustomerDetails(customer_id='CF_7768', customer_phone='7778989987')
```
* Create A Order Object
```python
from cashfree import CashFreeOrder
order = CashFreeOrder(order_id='your-order-id', order_amount=120.3)
```
### Now you can use the client to interact with CashFree APIs

* Create an order payment session
```python
# You can pass the order & customer object inside create_order method
order = cashfree_client.create_order(order, customer)
payment_session_id = order.get('payment_session_id')
```
* Get Payment Details Of A Single Order
```python
order_details = cashfree_client.get_payment_details('your_order_id')
```

* Webhook Signature validation
```python
# Get The raw Payload data
raw_payload = request.get_data(as_text=True)
timestamp = request.headers.get('x-webhook-timestamp')
received_signature = request.headers.get('x-webhook-signature')
is_valid_webhook = cashfree_client.validate_webhook_signature(raw_payload, timestamp, received_signature)
```

### Contributing:
Contributions are always welcome! If you find any issues or have suggestions, please open an issue or create a pull request on GitHub.

### License:

This project is licensed under the MIT License

### Support:
For api related support please contact support@cashfree.com.

Pending Feature:
* Easy Split Module
* Payouts Module
* Cashgram Module
* Verification Suite