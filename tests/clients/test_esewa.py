import os
from uuid import uuid4

from ..connectors import esewa_client


# from c


class TestEsewa:
    client = esewa_client

    def test_esewa_sign_message(self):
        order = {
            "product_code": "EPAYTEST",
            "total_amount": "110",
            # "transaction_uuid": uuid4(),
            "transaction_uuid": "5a0f365d-2c11-41a2-a2d1-ccba63abfe11",
        }

        message = self.client.sign_order(order)
        print({**order, **message})
        assert message["signed_field_names"] == "product_code,total_amount,transaction_uuid"
        assert message["signature"] == "Gbp01DHzov80qFFDIYYgwPik0Z6K7KrOPDw9351mCDk="

    def test_esewa_form_render(self, esewa__order):
        message = self.client.sign_order(esewa__order)
        print(message)
        if "tmp" not in os.listdir():
            os.makedirs("tmp")
        with open("tmp/esewa.html", "w") as f:
            f.write(self.client.render_form(message))

    def test_sign_message(self):
        assert self.client._sign_message("Message", "secret") == "qnR8UCqJggD55PohusaBNviGoOJ67HC6Btry4qXLVZc="
