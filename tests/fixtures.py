from uuid import uuid4

import pytest

from .connectors import khalti_client
from datetime import datetime

__all__ = [
    "khalti__intent",
    "esewa__order",
]


@pytest.fixture
def esewa__order():
    return {
        "amount": "110",
        "tax_amount": "0",
        "total_amount": "110",
        "transaction_uuid": str(uuid4()),
        "product_code": "EPAYTEST",
        "product_service_charge": "0",
        "product_delivery_charge": "0",
        "success_url": "https://esewa.com.np",
        "failure_url": "https://esewa.com.np",
    }


@pytest.fixture
def khalti__intent():
    current_timestamp = datetime.now().timestamp()
    intent = khalti_client.create_intent(
        amount=1000,
        order_id=f"order_{current_timestamp}",
        order_name="Test Order",
        customer_info={
            "name": "Customer 1",
            "email": "abc@email.com",
        },
    )
    return intent
