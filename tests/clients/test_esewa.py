from ..connectors import esewa_client

# from c


class TestEsewa:
    client = esewa_client

    def test_esewa_signature(self):
        message = self.client.sign_message(
            {
                "product_code": "EPAYTEST",
                "total_amount": "110",
                "transaction_uuid": "ab14a8f2b02c3",
            },
        )
        print(message)
        assert message["signed_field_names"] == 'product_code,total_amount,transaction_uuid'
        assert message["signature"] == "QyZKtzlGc9ytlPY2E0zJmBw/tAaFiD+jQ/yWIdR/xYs="

    def test_esewa_intent__success(self):
        pass
