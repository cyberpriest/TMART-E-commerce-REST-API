

import base64 ,os 
import httpx 
import uuid
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv() 



MONNIFY_BASE_URL = "https://sandbox.monnify.com"  # switch to live when ready
MONNIFY_API_KEY = os.getenv('MONNIFY_API_KEY')
MONNIFY_SECRET_KEY = os.getenv('MONNIFY_SECRET_KEY')
MONNIFY_CONTRACT_CODE = os.getenv('MONNIFY_CONTRACT_CODE')
FRONTEND_URL = os.getenv('FRONTEND_URL')  # set in .env for production



def get_access_token()->str:
    if not MONNIFY_API_KEY or not MONNIFY_SECRET_KEY:
        raise HTTPException(status_code=500, detail='Monnify API credentials are not configured')

    creds = f'{MONNIFY_API_KEY}:{MONNIFY_SECRET_KEY}'
    encode_credss  = base64.b64encode(creds.encode()).decode()
    
    res = httpx.post(
        f'{MONNIFY_BASE_URL}/api/v1/auth/login',
        headers = {'Authorization':f'Basic {encode_credss}'},
        timeout=15.0)
    try:
        data = res.json()
    except ValueError as exc:
        raise HTTPException(status_code=502, detail='Monnify returned an invalid authentication response') from exc

    if not data.get('requestSuccessful'):
        raise HTTPException(status_code=400,detail='Monnify auth failed')

    response_body = data.get('responseBody') or {}
    access_token = response_body.get('accessToken')
    if not access_token:
        raise HTTPException(status_code=502, detail='Monnify auth response did not include an access token')
    return access_token


def initialize_payment(amount:float ,order_id:int,email:str,full_name:str):
    if not MONNIFY_CONTRACT_CODE:
        raise HTTPException(status_code=500, detail='Monnify contract code is not configured')

    token = get_access_token()

    unique_ref = f'TMART-ORDER-{order_id}-{uuid.uuid4().hex[:8]}'
    payload = {
        'amount': amount,
        'customerEmail': email,
        'customerName': full_name,
        'paymentReference': unique_ref,
        'paymentDescription': f'Payment for order {order_id}',
        'currencyCode': 'NGN',
        'contractCode': MONNIFY_CONTRACT_CODE,
        'redirectUrl': FRONTEND_URL,
        'paymentMethods': ['CARD', 'ACCOUNT_TRANSFER']
    }

    res = httpx.post(
        f'{MONNIFY_BASE_URL}/api/v1/merchant/transactions/init-transaction',
        headers = {'Authorization': f'Bearer {token}'},
        json=payload,
        timeout=15.0)
    try:
        data = res.json()
    except ValueError as exc:
        raise HTTPException(status_code=502, detail='Monnify returned an invalid initialization response') from exc

    if not data.get('requestSuccessful'):
        error_message = data.get('responseMessage') or data.get('message') or res.text
        raise HTTPException(status_code=400, detail=f'Monnify payment initialization failed: {error_message}')

    response_body = data.get('responseBody') or {}
    if not isinstance(response_body, dict):
        raise HTTPException(status_code=502, detail='Monnify returned an unexpected initialization payload')
    return response_body
    


