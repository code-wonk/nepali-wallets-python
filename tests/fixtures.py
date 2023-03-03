import pytest

from .connectors import khalti_client
from datetime import datetime

__all__ = [
    'khalti__intent',
]


@pytest.fixture
def khalti__intent():
    current_timestamp = datetime.now().timestamp()
    intent = khalti_client.create_intent(
        amount=1000,
        order_id=f'order_{current_timestamp}',
        order_name="Test Order",
        customer_info={
            'name': 'Customer 1',
            'email': 'abc@email.com',
        }
    )
    return intent
