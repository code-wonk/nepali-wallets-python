from nepali_wallets.client import KhaltiClient, EsewaClient
from decouple import config

__all__ = [
    'khalti_client',
    'esewa_client',
]

khalti_client = KhaltiClient(
    public_key=config('KHALTI_PUBLIC_KEY'),
    secret_key=config('KHALTI_SECRET_KEY'),
    return_url=config('KHALTI_SUCCESS_URL'),
    website_url=config('KHALTI_FAILURE_URL'),
    sandbox=True
)

esewa_client = EsewaClient(
    sandbox=True,
)
