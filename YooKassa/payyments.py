import uuid

from yookassa import Configuration, Payment

Configuration.account_id = <Shop ID>
Configuration.secret_key = <Secret Key>

payment = Payment.create({
    "amount": {
        "value": "100.00",
        "currency": "RUB"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "https://www.example.com/return_url"
    },
    "capture": True,
    "description": "Order No. 1"
}, uuid.uuid4())

payment_transaction = {
    "id": "23d93cac-000f-5000-8000-126628f15141",
    "status": "pending",
    "paid": False,
    "amount": {
        "value": "100.00",
        "currency": "RUB"
    },
    "confirmation": {
        "type": "redirect",
        "confirmation_url": "https://yoomoney.ru/api-pages/v2/payment-confirm/epl?orderId=23d93cac-000f-5000-8000-126628f15141"
    },
    "created_at": "2019-01-22T14:30:45.129Z",
    "description": "Order No. 1",
    "metadata": {},
    "recipient": {
        "account_id": "100500",
        "gateway_id": "100700"
    },
    "refundable": False,
    "test": False
}


payment_id = '215d8da0-000f-50be-b000-0003308c89be'
idempotence_key = str(uuid.uuid4())
response = Payment.capture(
  payment_id,
  {
    "amount": {
      "value": "2.00",
      "currency": "RUB"
    }
  },
  idempotence_key
)



payment_id = '215d8da0-000f-50be-b000-0003308c89be'
idempotence_key = str(uuid.uuid4())
response = Payment.cancel(
  payment_id,
  idempotence_key
)