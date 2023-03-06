import json
from abc import ABC, abstractmethod
from typing import Union

import requests

__all__ = [
    'BasePaymentIntent',
    'BasePaymentClient',
    'PaymentClientError'
]

from requests import JSONDecodeError


class PaymentClientError(BaseException):
    pass


class BasePaymentIntent(ABC):
    """
    **BasePaymentIntent** is used by a ``BasePaymentClient`` instance to track the
     response of the intent
    `response`
    :cvar response: a ``requests.Response`` instance  used to track the original response from the server exists
    :cvar data: ``dict`` used only when there is no ``requests.Response`` instance exist
    """
    response: Union[requests.Response, None]
    data: dict

    @classmethod
    @abstractmethod
    def from_response(cls, response: requests.Response) -> 'BasePaymentIntent':
        """
        This is a builder method that returns the BasePaymentIntent object from
        the requests.Response object
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'BasePaymentIntent':
        """
        This is a builder method that returns the BasePaymentIntent object from
        the user-defined data type.
        Example intent for khalti:

        intent = BasePaymentIntent({"pidx": "A1B2C3"})
        """
        pass

    def __init__(self, response: Union[requests.Response, dict], **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if isinstance(response, requests.Response):
            self.response = response
            try:
                self.data = response.json()
            except JSONDecodeError:
                self.data = {}
        else:
            self.data = response
            self.response = None

    @abstractmethod
    def _get_intent_id(self) -> str:
        pass

    @property
    def id(self):
        return self._get_intent_id()

    @property
    def text(self):
        if self.response:
            return self.response.text
        elif self.data:
            return json.dumps(self.data)
        return None


class BasePaymentClient(ABC):
    base_url: str
    merchant_id: str
    public_key: str
    secret_key: str
    sandbox: str

    def __init__(self, *args, **kwargs):
        """
        It accepts all the keys and values from keyword arguments and
        sets instance attributes to the instance.
        """
        self.session = requests.Session()

        for k, v in kwargs.items():
            # initializing initial values
            setattr(self, k, v)

    @abstractmethod
    def _get_request_headers(self) -> dict:
        """
        It returns the dictionary with all request headers if needed
        """
        pass

    @abstractmethod
    def _get_request_body(self) -> dict:
        """
        It returns the default payload data
        """
        pass

    @abstractmethod
    def create_intent(self, *args, **kwargs) -> BasePaymentIntent:
        """
        It creates the payment intent for specific payment gateway
        """
        pass

    @abstractmethod
    def complete_payment(self, *args, **kwargs):
        """
        It performs the payment transaction so that the amount is deducted from the client's account
        """
        pass

    @abstractmethod
    def verify_payment(self, *args, **kwargs):
        """
        It is used for verifying the transaction
        """
        pass
