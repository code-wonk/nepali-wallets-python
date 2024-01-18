from typing import TypedDict
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.hashes import SHA256
import requests
from .base import BasePaymentClient, BasePaymentIntent
import base64

__all__ = ["EsewaClient", "EsewaIntent"]

ESEWA_UAT_SECRET_KEY = "8gBm/:&EnhH.1/q"


class SignedMessage(TypedDict):
    signed_field_names: str
    signature: str


class EsewaIntent(BasePaymentIntent):
    @classmethod
    def from_response(cls, response: requests.Response) -> "EsewaIntent":
        return cls(response)

    @classmethod
    def from_dict(cls, data: dict) -> "EsewaIntent":
        return cls(data)

    # def _get_intent_id(self) -> str:
    #     raise NotImplementedError
    #     # return self.data.get('pidx')


class EsewaClient(BasePaymentClient):
    username: str
    password: str
    success_url: str
    failure_url: str
    secret_key: str

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("secret_key", "8gBm/:&EnhH.1/q")  # this is the UAT secret key for E-pay v2
        super().__init__(*args, **kwargs)
        if self.sandbox:
            self.base_url = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
        else:
            self.base_url = "https://epay.esewa.com.np/api/epay/main/v2/form"

    def _sign_message(self, message, secret=None) -> SignedMessage:
        if not secret:
            secret = self.secret_key
        h = HMAC(bytes(secret, "utf-8"), SHA256())
        h.update(bytes(message, "utf-8"))
        return base64.b64encode(h.finalize()).decode("utf-8")

    def sign_order(self, data: dict[str, str], signed_field_names: list[str] = None) -> SignedMessage:
        """_summary_

        Args:
            data (dict): please pass all the field names and values as dictionary
            signed_field_names (list[str]): keys od the dictionary(data) that needs to be signed.
                if No arguments passed, it automatically

        Returns:
            signature (str): The signature that gets hashed and encoded using base64
        """
        if signed_field_names is None:
            signed_field_names = ["product_code", "total_amount", "transaction_uuid"]
        message = ",".join(f"{k}={data[k]}" for k in signed_field_names)
        signed_field_names = ",".join(signed_field_names)

        return {
            **data,
            "signature": self._sign_message(message),
            "signed_field_names": signed_field_names,
        }

    def _get_request_headers(self) -> dict:
        return {}

    def _get_request_body(self) -> dict:
        return {}

    def create_intent(
        self,
        signed_field_names: str,
        signature,
        *args,
        **kwargs,
    ):
        if signed_field_names is None:
            signed_field_names = []
        signed_message = self.sign_order({k: kwargs[k] for k in signed_field_names})
        return EsewaIntent.from_response(
            requests.post(
                self.base_url,
                {**kwargs, **signed_message},
            )
        )

    def render_form(self, data: dict[str, str], style: str = None) -> str:
        if not style:
            style = "font-size:16px; border-radius: 1rem; padding: 5px 10px;"
        form_data = "\n ".join(
            '<input name="{}", value="{}" style="{}" required/>'.format(k, v, style) for k, v in data.items()
        )
        return f"""
<form method="POST" action="{self.base_url}" style="display:flex;flex-direction:column; gap:10px;">
 {form_data}
 <input value="Submit" type="submit" style="{style}">
</form>"""

    def complete_payment(self, *args, **kwargs):
        raise NotImplementedError()

    def verify_payment(self, *args, **kwargs):
        raise NotImplementedError()
