from datetime import datetime

from ..connectors import khalti_client


class TestKhalti:
    def test_khali_intent__success(self):
        current_timestamp = datetime.now().timestamp()
        intent = khalti_client.create_intent(
            amount=1000,
            order_id=f'test_order_{current_timestamp}',
            order_name=f"Test Order {current_timestamp}",
            customer_info={
                'name': 'John Doe',
                'email': 'johndoe@example.com',
            }
        )
        assert intent.id is not None
        assert 'pidx' in intent.data

    def test_khalti_intent__status(self, khalti__intent):
        print(khalti__intent.id)
        data = khalti_client.verify_payment(khalti__intent)
        print(data.text)

    def test_khalti__payment(self, khalti__intent):
        """
        To run this test case, you must provide -s argument since this test case needs user interaction

        example 1: pytest -s
        example 2: pytest -s -k khalti__payment

        Once this test starts, the payment intent is created, at the time, you need to click the link generated
        by khalti and complete payment with credentials as follows:

        phone: 9800000000 / 9800000001 ... 9800000005
        mpin: 1111
        OTP: 987654
        """
        print(khalti__intent.data)
        print("Click the link, pay and continue")
        intent = input(f'intent id [{khalti__intent.id}]: ')
        data = khalti_client.verify_payment(intent or khalti__intent)
        assert data.json()['status'] == 'Completed'

