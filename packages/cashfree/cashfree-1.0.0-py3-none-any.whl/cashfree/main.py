import base64
import hashlib
import hmac
from typing import Optional

import requests
from pydantic import BaseModel

API_VERSIONS = {
    'v3': '2022-09-01'
}

PG_BASE_URLS = {
    'TEST': "https://sandbox.cashfree.com/pg",
    'LIVE': 'https://api.cashfree.com/pg'
}


class CustomerDetails(BaseModel):
    customer_id: str
    customer_phone: str
    customer_email: Optional[str] = None
    customer_name: Optional[str] = None
    customer_bank_account_number: Optional[str] = None
    customer_bank_ifsc: Optional[str] = None
    customer_bank_code: Optional[int] = None

    def get_dict(self):
        return {'customer_details': self.model_dump()}


class CashFreeOrder(BaseModel):
    order_id: str
    order_amount: float
    order_currency: Optional[str] = 'INR'
    order_note: Optional[str] = None
    order_tags: Optional[dict] = None
    order_splits: Optional[dict] = None

    def get_dict(self):
        return self.model_dump()


class OrderMeta(BaseModel):
    return_url: Optional[str] = None
    notify_url: Optional[str] = None
    payment_methods: Optional[str] = None

    def get_dict(self):
        return {'order_meta': self.model_dump()}


class CashFree:
    """
        Provides methods to interact with the Cashfree Payment Gateway APIs for managing orders, payments,
        payment links, token vault, reconciliation, etc.

        Args:
        - client_id (str): The merchant's application ID.
        - client_secret (str): The secret key for authentication. It should be securely stored.
        - environment (str, optional): Defines the environment, either "TEST" or "LIVE". Default is "TEST".
        - api_version (str, optional): Specifies the API version. Default is 'v3'.

        Merchant Authentication:
        - Standard authentication uses `x-client-id` and `x-client-secret` headers. Pass the `client_id`
          and `client_secret` obtained from the Cashfree dashboard.
        - Ensure the secret key is securely stored and not accessible by unauthorized individuals.
        - Avoid calling authenticated APIs from the client-side to prevent exposing the secret key.

        Methods:
        - create_order: Create orders with Cashfree from your backend and get the payment link.
        - get_order_details: View all details of a specific order.
        - create_payment_link: Create a new payment link.
        - get_payment_details: View all payment details for an order.
        - create_refund: Initiate a refund for a specific order.
        - (And more methods for handling payments, payment links, token vault, reconciliation, etc.)
    """

    def __init__(self, client_id, client_secret, environment="TEST", api_version='v3'):
        self._client_id = client_id
        self._client_secret = client_secret
        self._pg_base_url = PG_BASE_URLS.get(environment, "https://sandbox.cashfree.com/pg")
        self._headers = {
            "accept": "application/json",
            "x-api-version": API_VERSIONS.get('api_version', '2022-09-01'),
            "content-type": "application/json",
            "x-client-id": self._client_id,
            "x-client-secret": self._client_secret
        }

    def _create_order(self, order_data: CashFreeOrder, customer_data: CustomerDetails,
                      order_meta: OrderMeta = None, order_expiry_time: str = None,
                      order_note: str = None, order_tags: dict = None, order_splits: dict = None) -> list:
        payload = {**order_data.get_dict(), **customer_data.get_dict()}

        if order_meta:
            payload['order_meta'] = order_meta.model_dump()
        if order_expiry_time:
            payload['order_expiry_time'] = order_expiry_time
        if order_note:
            payload['order_note'] = order_note
        if order_tags:
            payload['order_tags'] = order_tags
        if order_splits:
            payload['order_splits'] = order_splits

        response = requests.post(f'{self._pg_base_url}/orders', json=payload, headers=self._headers)
        return response.json()

    # Orders Module
    def create_order(self, order_data: CashFreeOrder, customer_data: CustomerDetails,
                     order_meta: OrderMeta = None, order_expiry_time: str = None,
                     order_note: str = None, order_tags: dict = None, order_splits: dict = None):
        """
            Use this API to create orders with Cashfree from your backend to get a payment_sessions_id.
            You can use the payment_sessions_id to create a transaction for the order.

            Parameters:
            - order_data (CashFreeOrder): Details of the order (order_id, amount, currency, etc.).
            - customer_data (CustomerDetails): Customer-related details necessary for the order.
            - order_meta (OrderMeta | None): Optional meta details controlling the payment journey.
            - order_expiry_time (str | None): Time after which the order expires (ISO 8601 format).
            - order_note (str | None): Reference note for the order.
            - order_tags (dict | None): Custom tags in the form of {"key": "value"}. Max 10 tags allowed.
            - order_splits (dict | None): For Easy split enabled accounts, split the order amount.

            Payload Structure:
            Refer to Cashfree's documentation for payload structure:
            https://docs.cashfree.com/reference/pgcreateorder

            Returns:
            - dict: JSON response containing details of the created order.
        """
        return self._create_order(order_data, customer_data, order_meta, order_expiry_time, order_note,
                                  order_tags, order_splits)

    def get_order_details(self, order_id: str) -> dict:
        """
            Retrieves details of a specific order.

            Parameters:
            - order_id (str): Identifier of the order for which details are requested.

            Returns:
            - dict: JSON response containing details related to the specified order.

            Note:
            The returned dictionary includes comprehensive information about the order,
            such as order status, amount, customer details, payment-related information,
            and any additional metadata associated with the order.
            Refer To https://docs.cashfree.com/reference/pgfetchorder

        """
        response = requests.get(f"{self._pg_base_url}/orders/{order_id}", headers=self._headers)
        return response.json()

    # Payments Module
    def get_payment_details(self, order_id: str) -> dict:
        """
            Use this API to view all payment details associated with a particular order.

            Parameters:
            - order_id (str): Identifier of the order for which payment details are requested.

            Returns:
            - dict: JSON response containing payment details related to the specified order.

            Note:
            The returned dictionary includes information such as payment status, transaction details,
            payment mode, amount, and other relevant payment-related data.
        """
        return requests.get(f'{self._pg_base_url}/orders/{order_id}/payments', headers=self._headers).json()

    # offers Module
    def create_offer(self, offer_data: dict) -> dict:
        """
            Creates offers with Cashfree from your backend.

            Parameters:
            - offer_data (dict): Request body to create an offer at Cashfree.
              Refer to Cashfree's documentation for payload structure:
              https://docs.cashfree.com/reference/pgfetchorder

            Returns:
            - dict: JSON response containing details of the created offer.

            Note: The offer_data parameter should contain nested objects for offer_meta, offer_tnc, offer_details,
            and offer_validations to provide essential details required to create an offer

        """
        return requests.post(f'{self._pg_base_url}/offers', json=offer_data, headers=self._headers).json()

    def get_offer_details(self, offer_id: str):
        """
            Retrieves details of a specific offer.

            Args:
                offer_id (str): Identifier of the offer for which details are requested.

            Returns:
                dict: JSON response containing details related to the specified offer.

            Description:
                Use this API to fetch details of a particular offer using its identifier.

            Note:
                The returned dictionary includes comprehensive information about the offer,
                such as offer type, terms and conditions, validation details,
                and any additional metadata associated with the offer.
                Refer to: https://docs.cashfree.com/reference/pgfetchoffer
        """
        return requests.get(f'{self._pg_base_url}/offers/{offer_id}', headers=self._headers).json()

    # Token Vault
    def fetch_saved_cards(self, customer_id, instrument_type: str = 'card'):
        """
            Retrieves saved payment instruments/cards associated with a specific customer.
            Refer to: https://docs.cashfree.com/reference/pgcustomerfetchinstruments

            Parameters:
            - customer_id (str): Identifier of the customer to fetch saved payment instruments/cards.
            - instrument_type (str, optional): Type of payment instrument to retrieve (default is 'card').

            Returns:
            - dict: JSON response containing saved payment instruments/cards linked to the specified customer.

            Description:
            Use this API to retrieve saved payment instruments/cards associated with a specific customer
            by providing the customer identifier.
            The 'instrument_type' parameter allows filtering by a specific type of payment instrument (e.g., 'card').

            Note:
            The returned dictionary contains information about the saved payment instruments/cards
            associated with the specified customer.

        """
        return requests.get(f'{self._pg_base_url}/customers/{customer_id}/instruments?instrument_type{instrument_type}',
                            headers=self._headers).json()

    def fetch_single_card(self, customer_id, instrument_id):
        """
            Retrieves details of a specific saved payment instrument/card for a customer.
            Refer to: https://docs.cashfree.com/reference/pgcustomerfetchinstrument

            Parameters:
            - customer_id (str): Identifier of the customer associated with the saved payment instrument/card.
            - instrument_id (str): Identifier of the specific saved payment instrument/card to retrieve.

            Returns:
            - dict: JSON response containing details of the specified saved payment instrument/card.

            Description:
            Use this API to retrieve details of a specific saved payment instrument/card associated with a customer
            by providing both the customer identifier and the instrument identifier.

            Note:
            The returned dictionary contains detailed information about the specified saved payment instrument/card
            associated with the provided customer and instrument identifiers.

        """
        return requests.get(f'{self._pg_base_url}/customers/{customer_id}/instruments/{instrument_id}',
                            headers=self._headers).json()

    def delete_saved_instrument(self, customer_id, instrument_id):
        """
            Deletes a specific saved payment instrument/card associated with a customer.
            refer to: https://docs.cashfree.com/reference/pgcustomerdeleteinstrument

            Parameters:
            - customer_id (str): Identifier of the customer associated with the saved payment instrument/card.
            - instrument_id (str): Identifier of the specific saved payment instrument/card to delete.

            Returns:
            - dict: JSON response confirming the deletion of the specified saved payment instrument/card.

            Description:
            Use this API to delete a specific saved payment instrument/card associated with a customer
            by providing both the customer identifier and the instrument identifier.

            Note:
            The returned dictionary confirms the successful deletion of the specified saved payment instrument/card
            associated with the provided customer and instrument identifiers.

        """
        return requests.delete(f'{self._pg_base_url}/customers/{customer_id}/instruments/{instrument_id}',
                               headers=self._headers).json()

    def fetch_cryptogram_from_saved_card(self, customer_id: str, instrument_id: str):
        """
            Retrieves the cryptogram for a specific saved card associated with a customer.
            refer to: https://docs.cashfree.com/reference/pgcustomerinstrumentsfetchcryptogram

            Parameters:
            - customer_id (str): Identifier of the customer associated with the saved card.
            - instrument_id (str): Identifier of the specific saved card to retrieve the cryptogram.

            Returns:
            - dict: JSON response containing the cryptogram of the specified saved card.

            Description:
            Use this API to retrieve the cryptogram for a specific saved card associated with a customer
            by providing both the customer identifier and the card's instrument identifier.

            Note:
            The returned dictionary contains the cryptogram of the specified saved card
            associated with the provided customer and card's instrument identifiers.

        """
        return requests.delete(f'{self._pg_base_url}/customers/{customer_id}/instruments/{instrument_id}/cryptogram',
                               headers=self._headers).json()

    # Payment Link
    def create_payment_link(self, link_id: str, link_amount: float,
                            link_purpose: str, customer_details: dict,
                            link_currency: str = "INR", link_partial_payments: bool = False,
                            link_minimum_partial_amount: float = None, link_expiry_time=None,
                            link_notify: dict = None, link_auto_reminders: bool = False, link_notes: dict = None,
                            link_meta: dict = None) -> dict:
        """
        Creates a new payment link with Cashfree.
        Refer to: https://docs.cashfree.com/reference/pgcreatelink

        Description:
        Use this API to create a new payment link. The created payment link URL will be available
        in the API response parameter 'link_url'.

        Parameters:
            - link_id (str): Unique Identifier (provided by merchant) for the link. Alphanumeric, '-', and '_' allowed.
            - link_amount (float): Amount to be collected using this link (provide up to two decimals for paise).
            - link_purpose (str): Brief description for which payment must be collected (shown to the customer).
            - customer_details (dict): Payment link customer entity.
            - link_currency (str, optional): Currency for the payment link (default is INR).
            - link_partial_payments (bool, optional): If "true", allows customer to make partial payments for the link.
            - link_minimum_partial_amount (float, optional): Minimum amount for the first installment if partial
              payments are enabled.
            - link_expiry_time (str, optional): Time after which the link expires in ISO 8601 format
              (default is 30 days).
            - link_notify (dict, optional): Payment link Notify Object for SMS and Email.
            - link_auto_reminders (bool, optional): If "true", reminders will be sent to customers for collecting
              payments.
            - link_notes (dict, optional): Key-value pair to store additional information about the entity
              (max 5 key-value pairs).
            - link_meta (dict, optional): Payment link meta information object.

        Returns:
        - dict: JSON response containing details of the created payment link.
        """
        payload = {
            'link_id': link_id, 'link_amount': link_amount, 'link_purpose': link_purpose,
            'link_currency': link_currency,
            'customer_details': customer_details, 'link_partial_payments': link_partial_payments,
            'link_auto_reminders': link_auto_reminders,
        }
        if link_minimum_partial_amount:
            payload['link_minimum_partial_amount'] = link_minimum_partial_amount
        if link_expiry_time:
            payload['link_expiry_time'] = link_expiry_time
        if link_notify:
            payload['link_notify'] = link_notify
        if link_notes:
            payload['link_notes'] = link_notes
        if link_notes:
            payload['link_meta'] = link_meta

        return requests.post(f'{self._pg_base_url}/links', json=payload, headers=self._headers).json()

    def fetch_payment_link(self, link_id):
        """
        Fetches details and status of a specific payment link.
        Refer to: https://docs.cashfree.com/reference/pgfetchlink

        Description:
        Use this API to view all details and status of a specific payment link using its identifier.

        Parameters:
        - link_id (str): Identifier of the payment link for which details are requested.

        Returns:
        - dict: JSON response containing details and status related to the specified payment link.

        Note:
        The returned dictionary includes comprehensive information about the payment link,
        including its status, amount, expiry time, customer details, and any associated metadata.
        """
        return requests.get(f'{self._pg_base_url}/links/{link_id}', headers=self._headers).json()

    def cancel_payment_link(self, link_id):
        """
        Cancels a specific payment link.
        Refer to: https://docs.cashfree.com/reference/pgcancellink

        Parameters:
        - link_id (str): Identifier of the payment link to be canceled.

        Returns:
        - dict: JSON response confirming the cancellation of the specified payment link.

        Description:
        Use this API to cancel a specific payment link by providing its identifier.

        Note:
        Upon successful cancellation, the method returns a confirmation in JSON format.

        """
        return requests.post(f'{self._pg_base_url}/links/{link_id}/cancel', headers=self._headers).json()

    def get_order_from_payment_link(self, link_id):
        """
        Retrieves order details associated with a specific payment link.

        Parameters:
        - link_id (str): Identifier of the payment link to fetch associated order details.

        Returns:
        - dict: JSON response containing order details linked to the specified payment link.

        Description:
        Use this API to retrieve order details associated with a specific payment link
        by providing its identifier.

        Note:
        The returned dictionary contains information related to the order linked with the payment link.

        """
        return requests.post(f'{self._pg_base_url}/links/{link_id}/orders', headers=self._headers).json()

    # Refunds
    def create_refund(self, order_id, refund_amount: float, refund_id: str,
                      refund_note=None, refund_speed: str = 'STANDARD', refund_splits: dict = None) -> dict:
        """
            Initiates a refund for a specific order.
            refer to: https://docs.cashfree.com/reference/pgordercreaterefund

            Parameters:
            - order_id (str): Identifier of the order for which the refund is initiated.
            - refund_amount (float): Amount to be refunded.
            - refund_id (str): Identifier for the refund transaction.
            - refund_note (str, optional): Note/reference for the refund.
            - refund_speed (str, optional): Speed of the refund process (default is 'STANDARD').
            - refund_splits (dict, optional): Dictionary specifying how the refund amount is split (if applicable).

            Returns:
            - dict: JSON response confirming the initiation of the refund.

            Description:
            Use this API to initiate a refund for a specific order by providing the order identifier,
            refund amount, and refund ID.

            Note:
            The returned dictionary confirms the initiation of the refund transaction.

        """
        payload = {
            'refund_amount': refund_amount,
            'refund_id': refund_id,
            'refund_speed': refund_speed
        }
        if refund_note:
            payload['refund_note'] = refund_note
        if refund_splits:
            payload['refund_splits'] = refund_splits

        return requests.post(f'{self._pg_base_url}/orders/{order_id}/refunds', json=payload,
                             headers=self._headers).json()

    def get_refund_from_order(self, order_id):
        """
            Retrieves refund details associated with a specific order.
            Refer to: https://docs.cashfree.com/reference/pgorderfetchrefunds

            Parameters:
            - order_id (str): Identifier of the order to fetch associated refund details.

            Returns:
            - dict: JSON response containing refund details linked to the specified order.

            Description:
            Use this API to retrieve refund details associated with a specific order
            by providing its identifier.

            Note:
            The returned dictionary contains information related to the refunds associated with the specified order.

        """
        return requests.get(f'{self._pg_base_url}/orders/{order_id}/refunds', headers=self._headers).json()

    def get_single_refund(self, order_id, refund_id):
        """
            Retrieves details of a specific refund associated with an order.
            Refer to: https://docs.cashfree.com/reference/pgorderfetchrefund

            Parameters:
            - order_id (str): Identifier of the order associated with the refund.
            - refund_id (str): Identifier of the specific refund to retrieve.

            Returns:
            - dict: JSON response containing details of the specified refund.

            Description:
            Use this API to retrieve details of a specific refund associated with an order
            by providing both the order identifier and the refund identifier.

            Note:
            The returned dictionary contains detailed information about the specified refund.

        """
        return requests.get(f'{self._pg_base_url}/orders/{order_id}/refunds/{refund_id}', headers=self._headers).json()

    # Settlement Module
    def get_settlement(self, order_id):
        """
            Retrieves settlement details associated with a specific order.
            refer to: https://docs.cashfree.com/reference/pgorderfetchsettlement

            Parameters:
            - order_id (str): Identifier of the order to fetch associated settlement details.

            Returns:
            - dict: JSON response containing settlement details linked to the specified order.

            Description:
            Use this API to retrieve settlement details associated with a specific order
            by providing its identifier.

            Note:
            The returned dictionary contains information related to settlements associated with the specified order.

        """
        return requests.get(f'{self._pg_base_url}/orders/{order_id}/settlements', headers=self._headers).json()

    # Reconciliation Module
    def payment_reconciliation(self, start_date: str, end_date: str, limit=10, cursor: str = None):
        """
            Retrieve a payment reconciliation process within a specified date range.
            Refer to: https://docs.cashfree.com/reference/pgfetchrecon

            Parameters:
            - start_date (str): Start date (YYYY-MM-DD format) for the reconciliation period.
            - end_date (str): End date (YYYY-MM-DD format) for the reconciliation period.
            - limit (int, optional): Maximum number of reconciliation records to fetch (default is 10, maximum is 1000).
            - cursor (str, optional): Cursor used for pagination if more records are available.

            Returns:
            - dict: JSON response containing payment reconciliation details for the specified date range.

            Description:
            Use this API to initiate a payment reconciliation process within a specific date range.
            The reconciliation records are filtered based on the provided start and end dates.
            Pagination can be applied using the 'limit' parameter and 'cursor' for fetching more records.

            Note:
            The returned dictionary contains payment reconciliation details for the specified date range.

            """
        payload = {
            'filters': {
                'start_date': start_date,
                'end_date': end_date
            },
            'pagination': {
                'limit': min(max(limit, 10), 1000),

            }
        }
        if cursor:
            payload['pagination']['cursor'] = cursor

        return requests.post(f'{self._pg_base_url}/recon', headers=self._headers).json()

    # Webhook Module
    def validate_webhook_signature(self, payload: str, timestamp: str, signature: str):
        signed_payload = f"{timestamp}{payload}"
        hashed = hmac.new(
            key=bytes(self._client_secret, 'utf-8'),
            msg=bytes(signed_payload, 'utf-8'),
            digestmod=hashlib.sha256
        )
        expected_hash = base64.b64encode(hashed.digest()).decode('utf-8')
        print(expected_hash)
        return signature == expected_hash
