# payments.py  
import uuid  
from yookassa import Configuration, Payment  # Ensure you have yookassa library installed  

class YooKassaPayment:  
    def __init__(self, account_id: str, secret_key: str):  
        Configuration.account_id = account_id  
        Configuration.secret_key = secret_key  

    def create_payment(self, amount: float, currency: str, description: str, return_url: str):  
        """Create a new payment."""  
        payment = Payment.create({  
            "amount": {  
                "value": str(amount),  
                "currency": currency  
            },  
            "confirmation": {  
                "type": "redirect",  
                "return_url": return_url  
            },  
            "capture": True,  
            "description": description  
        }, uuid.uuid4())  
        return payment  

    def capture_payment(self, payment_id: str, amount: float, currency: str):  
        """Capture a payment."""  
        idempotence_key = str(uuid.uuid4())  
        response = Payment.capture(  
            payment_id,  
            {  
                "amount": {  
                    "value": str(amount),  
                    "currency": currency  
                }  
            },  
            idempotence_key  
        )  
        return response  

    def cancel_payment(self, payment_id: str):  
        """Cancel a payment."""  
        idempotence_key = str(uuid.uuid4())  
        response = Payment.cancel(payment_id, idempotence_key)  
        return response