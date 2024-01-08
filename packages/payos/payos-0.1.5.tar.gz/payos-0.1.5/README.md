The payOS library provides convenient access to the payOS API from applications written in python.

## Documentation

See the [payOS API docs](https://payos.vn/docs/api/) for more infomation.

## Installation

Install the package with:

```bash
pip install payos==0.2.0
```

## Usage

### Initialize

You need to initialize the PayOS object with the Client ID, Api Key and Checksum Key of the payment channel you created.


```python
from payos import PayOS
import os

client_id = os.environ.get('PAYOS_CLIENT_ID')
api_key = os.environ.get('PAYOS_API_KEY')
checksum_key = os.environ.get('PAYOS_CHECKSUM_KEY')

payOS = PayOS(client_id=client_id, api_key=api_key, checksum_key=checksum_key)
```

### Methods included in the PayOS object

- **createPaymentLink**

Create a payment link for the order data

Syntax:

```python
payOS.createPaymentLink(requestData)
```

Parameter data type: **PaymentData**

```python

@dataclass
class PaymentData:
    orderCode: int
    amount: int
    description: str
    items: List[ItemData]
    cancelUrl: str
    returnUrl: str
    signature: str
    buyerName: str = None
    buyerEmail: str = None
    buyerPhone: str = None
    buyerAddress: str = None
    expiredAt: str = None
    def to_json(self):
    #Return a JSON object


@dataclass
class ItemData:
    name: str
    quantity: int
    price: int
    def to_json(self):
    #Return a JSON object


```

Return data type: **CreatePaymentResult**

```python
@dataclass
class CreatePaymentResult:
    bin: str
    accountNumber: str
    accountName: str
    amount: int
    description: str
    orderCode: int
    paymentLinkId: str
    status: str
    checkoutUrl: str
    qrCode: str
    def to_json(self):
    #Return a JSON object
```

Example:

```py
item = ItemData(name="Mì tôm hảo hảo ly", quantity=1, price=1000)

paymentData = PaymentData(orderCode=11, amount=1000, description="Thanh toan don hang",
     items=[item], cancelUrl="http://localhost:8000", returnUrl="http://localhost:8000")

paymentLinkData = payOS.createPaymentLink(paymentData)
```

- **getPaymentLinkInformation**

Get payment information of an order that has created a payment link.

Syntax:

```python
payOS.getPaymentLinkInformation(id)
```

Parameters:

- `id`: Store order code (`orderCode`) or payOS payment link id (`paymentLinkId`). Type of `id` is str or int.

Return data type: **PaymentLinkInformation**

```py
@dataclass
class PaymentLinkInformation:
    id: str
    orderCode: int
    amount: int
    amountPaid: int
    amountRemaining: int
    status: str
    createdAt: str
    transactions: List[Transaction]
    cancellationReason: str or None
    canceledAt: str or None
    def to_json(self):
    #Return a JSON object
```

Transaction type: 

```python
@dataclass
class Transaction:
    reference: str
    amount: int
    accountNumber: str
    description: str
    transactionDateTime: str
    virtualAccountName: str or None
    virtualAccountNumber: str or None
    counterAccountBankId: str or None
    counterAccountBankName: str or None
    counterAccountName: str or None
    counterAccountNumber: str or None
    def to_json(self):
    #Return a JSON object
```

Example:

```py
paymentLinkInfo = payOS.getPaymentLinkInformation(1234)
```

- **cancelPaymentLink**

Cancel the payment link of the order.

Syntax:

```python
payOS.cancelPaymentLink(orderCode, cancellationReason)
```

Parameters:

- `id`: Store order code (`orderCode`) or payOS payment link id (`paymentLinkId`). Type of `id` is str or int.

- `cancellationReason`: Reason for canceling payment link (optional).

Return data type: **PaymentLinkInformation**

```py
@dataclass
class PaymentLinkInformation:
    id: str
    orderCode: int
    amount: int
    amountPaid: int
    amountRemaining: int
    status: str
    createdAt: str
    transactions: List[Transaction]
    cancellationReason: str or None
    canceledAt: str or None
    def to_json(self):
    #Return a JSON object
```

Example:

```py
orderCode = 123
cancellationReason = "reason"

cancelledPaymentLinkInfo = payOS.cancelPaymentLink(orderCode, cancellationReason)

// If you want to cancel the payment link without reason:
cancelledPaymentLinkInfo = payOS.cancelPaymentLink(orderCode)
```

- **confirmWebhook**

Validate the Webhook URL of a payment channel and add or update the Webhook URL for that Payment Channel if successful.

Syntax:

```py
payOS.confirmWebhook("https://your-webhook-url/")
```

- **verifyPaymentWebhookData**

Verify data received via webhook after payment.

Syntax:

```py
webhookData = payOS.verifyPaymentWebhookData(webhookBody)
```

Return data type: **WebhookData**

```py
@dataclass
class WebhookData:
    orderCode: int
    amount: int
    description: str
    accountNumber: str
    reference: str
    transactionDateTime: str
    paymentLinkId: str
    code: str
    desc: str
    counterAccountBankId: str or None
    counterAccountBankName: str or None
    counterAccountName: str or None
    counterAccountNumber: str or None
    virtualAccountName: str or None
    virtualAccountNumber: str or None
    def to_json(self):
    #Return a JSON object
```
