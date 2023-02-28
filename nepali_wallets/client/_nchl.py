from .base import BasePaymentClient


class ConnectIPSClient(BasePaymentClient):
    username: str
    password: str
    success_url: str
    failure_url: str
    login_url: str

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
            self.base_url = 'https://uat.connectips.com:7443'
            self.login_url = "https://uat.connectips.com:7443/connectipswebgw/loginpage"
        else:
            self.base_url = 'https://login.connectips.com'
            self.login_url = "https://login.connectips.com/connectipswebgw/loginpage"
