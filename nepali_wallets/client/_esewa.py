from .base import BasePaymentClient

class EsewaClient(BasePaymentClient):
    username: str
    password: str
    success_url: str
    failure_url: str

    def _get_request_headers(self) -> dict:
        return {}

    def _get_request_body(self) -> dict:
        return {}

    def create_intent(self, *args, **kwargs):
        raise NotImplementedError()

    def complete_payment(self, *args, **kwargs):
        raise NotImplementedError()

    def verify_payment(self, *args, **kwargs) -> dict:
        raise NotImplementedError()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.sandbox:
            self.base_url = 'https://uat.esewa.com.np'
        else:
            self.base_url = 'https://esewa.com.np'
