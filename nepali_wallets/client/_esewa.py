from ast import Dict
from typing import Any, TypedDict
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from .base import BasePaymentClient
import base64

__all__ = [
    "EsewaClient",
]

ESEWA_UAT_SECRET_KEY = "8gBm/:&EnhH.1/q"


class SignedMessage(TypedDict):
    signed_field_names: str
    signature: str


class EsewaClient(BasePaymentClient):
    username: str
    password: str
    success_url: str
    failure_url: str
    secret_key: str

    def sign_message(self, data: dict[str, str]) -> SignedMessage:
        """_summary_

        Args:
            data (dict): please pass all the field names and values as dictionary

        Returns:
            signature (str): The signature that gets hashed and encoded using base64
        """
        signed_field_names = ",".join(data.keys())
        message = bytes(
            ",".join(f"{k}={v}" for k, v in data.items()),
            "utf-8",
        )
        h = HMAC(bytes(self.secret_key, "utf-8"), SHA256())
        h.update(message)
        return {"signature": base64.b64encode(h.finalize()).decode("utf-8"), "signed_field_names": signed_field_names}

    def _get_request_headers(self) -> dict:
        return {}

    def _get_request_body(self) -> dict:
        return {}

    def create_intent(self, *args, **kwargs):
        raise NotImplementedError()

    def complete_payment(self, *args, **kwargs):
        raise NotImplementedError()

    def verify_payment(self, *args, **kwargs):
        raise NotImplementedError()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("secret_key", "8gBm/:&EnhH.1/q")  # this is the UAT secret key for E-pay v2
        super().__init__(*args, **kwargs)
        if self.sandbox:
            self.base_url = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
        else:
            self.base_url = "https://epay.esewa.com.np/api/epay/main/v2/form"
