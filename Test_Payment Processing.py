import unittest
from unittest import mock
import re
import hashlib

# PaymentProcessing Class
class PaymentProcessing:
    def __init__(self):
        self.valid_payment_methods = ["credit_card", "paypal", "apple_pay"]

    def validate_payment_method(self, payment_method):
        if payment_method not in self.valid_payment_methods:
            raise ValueError(f"{payment_method} is not a valid payment method.")

    def validate_card_details(self, card_number, expiry_date, cvv):
        if not re.match(r"^[0-9]{16}$", card_number):
            raise ValueError("Invalid card number.")
        if not re.match(r"^(0[1-9]|1[0-2])/[0-9]{2}$", expiry_date):
            raise ValueError("Invalid expiry date.")
        if not re.match(r"^[0-9]{3,4}$", cvv):
            raise ValueError("Invalid CVV.")

    def process_credit_card_payment(self, amount, card_number, expiry_date, cvv):
        self.validate_card_details(card_number, expiry_date, cvv)
        # Simulate payment gateway interaction
        return {"status": "success", "message": "Payment successful"}

    def process_paypal_payment(self, amount, paypal_id):
        # Simulate PayPal API interaction
        return {"status": "success", "message": "Payment successful"}

    def process_payment(self, payment_method, amount, **kwargs):
        self.validate_payment_method(payment_method)
        if payment_method == "credit_card":
            return self.process_credit_card_payment(amount, kwargs['card_number'], kwargs['expiry_date'], kwargs['cvv'])
        elif payment_method == "paypal":
            return self.process_paypal_payment(amount, kwargs['paypal_id'])
        else:
            raise ValueError("Payment method not supported.")


# Unit tests for PaymentProcessing class
class TestPaymentProcessing(unittest.TestCase):
    def setUp(self):
        self.payment_processing = PaymentProcessing()

    def test_validate_payment_method_success(self):
        result = self.payment_processing.validate_payment_method("credit_card")
        self.assertTrue(result is None)  # validate_payment_method does not return anything

    def test_validate_payment_method_invalid_gateway(self):
        with self.assertRaises(ValueError):
            self.payment_processing.validate_payment_method("bitcoin")

    def test_validate_credit_card_invalid_details(self):
        with self.assertRaises(ValueError):
            self.payment_processing.validate_card_details("1234", "12/25", "12")

    def test_process_payment_success(self):
        result = self.payment_processing.process_payment("credit_card", 100.00, card_number="1234567812345678", expiry_date="12/25", cvv="123")
        self.assertEqual(result["status"], "success")

    def test_process_payment_failure(self):
        with mock.patch.object(self.payment_processing, 'process_credit_card_payment', return_value={"status": "failure"}):
            result = self.payment_processing.process_payment("credit_card", 100.00, card_number="1234567812345678", expiry_date="12/25", cvv="123")
            self.assertEqual(result["status"], "failure")

    def test_process_payment_invalid_method(self):
        with self.assertRaises(ValueError):
            self.payment_processing.process_payment("bitcoin", 100.00, card_number="1234567812345678", expiry_date="12/25", cvv="123")


if __name__ == '__main__':
    unittest.main()