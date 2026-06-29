

import base64 ,os 
import httpx 
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv() 



MONNIFY_BASE_URL = "https://sandbox.monnify.com"  # switch to live when ready
MONNIFY_API_KEY = os.getenv('MONNIFY_API_KEY')
MONNIFY_SECRET_KEY = os.getenv('MONNIFY_SECRET_KEY')
MONNIFY_CONTRACT_CODE = os.getenv('MONNIFY_CONTRACT_CODE')



def get_access_token()->str:
    creds = f'{MONNIFY_API_KEY}:{MONNIFY_SECRET_KEY}'
    encode_credss  = base64.b64encode(creds.encode()).decode()
    
    res = httpx.post(
        f'{MONNIFY_BASE_URL}/api/v1/auth/login',
        headers = {'Authorization':f'Basic {encode_credss}'})
    data = res.json()
    if not data.get('requestSuccessful'):
        raise HTTPException(status_code=400,detail='Monnify auth failed')
    return data['responseBody']['accessToken']


def initialize_payment(amount:float ,order_id:int,email:str):
    token = get_access_token()

    res = httpx.post(
        f'{MONNIFY_BASE_URL}/api/v1/merchant/transactions/init-transaction',
        headers = {'AUTHORIZATION':f'Bearer {token}'},
       json =  {
        'amount': amount,
        'customerEmail': email,
        'paymentReference': f'TAMRT-ORDER-{order_id}',
        'paymentDescription': f'Payment for order {order_id}',
        'currencyCode': 'NGN',
        'contractCode': MONNIFY_CONTRACT_CODE,
        'redirectUrl': 'http://localhost:3000/payment/callback',
        'paymentMethods': ['CARD', 'ACCOUNT_TRANSFER']}
    )
    data = res.json()

    if not data.get('requestSuccessful'):
        raise HTTPException(status_code=400,detail='')
    return data['responseBody']
    


