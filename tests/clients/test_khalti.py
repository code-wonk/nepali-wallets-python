from datetime import datetime

from ..connectors import khalti_client


class TestKhalti:
    def test_khali_intent__success(self):
        current_timestamp = datetime.now().timestamp()
        response = khalti_client.create_intent(
            amount=1000,
            order_id=f'test_order_{current_timestamp}',
            order_name=f"Test Order {current_timestamp}",
            customer_info={
                'name': 'John Doe',
                'email': 'johndoe@example.com',
            }
        )
        assert response.status_code == 200
        assert 'pidx' in response

    def test_khalti_intent__duplicate_order(self):
        current_timestamp = datetime.now().timestamp()
        data = {
            'amount': 1000,
            'order_id': f'test_order_{current_timestamp}',
            'order_name': f"Test Order {current_timestamp}",
            'customer_info': {
                'name': 'John Doe',
                'email': 'johndoe@example.com',
            }
        }
        khalti_client.create_intent(**data)
        response = khalti_client.create_intent(**data)

        assert response != 200
