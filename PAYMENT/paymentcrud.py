from sqlalchemy.orm import Session 
from fastapi import HTTPException,status
import httpx

from models import User,Order
from enums import OrderStatus
from .monnify import get_access_token,initialize_payment,MONNIFY_BASE_URL



def init_payment(db:Session,order_id,user:User):
    order = db.query(Order).filter(Order.id == order_id ,Order.user_id == user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail='order not found')
    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail=' order is not in pending ')
    
    init_pay = initialize_payment(
        amount=order.total,
        order_id = order_id,
        email = user.email
        )
    return  {
        'redirectUrl':init_pay['redirectUrl'],
        'paymentReference':init_pay['paymentReference'],
        'transactionReference':init_pay['transactionReference']


    }
    
    

def verify_payment(db:Session,transaction_reference:str):
    token = get_access_token()
    res = httpx.get(
        f'{MONNIFY_BASE_URL}/api/v1/merchant/transactions/query"',
        headers = {'Authorization':f'Bearer {token}'},
        params={'paymentReference':transaction_reference}

        )
    data = res.json()
    if not data.get('requestSuccessful'):
        raise HTTPException(status_code=400,detail='Monnify auth failed')


    body = data["responseBody"]
    if body["paymentStatus"] == "PAID":
        # update order status
        ref = body["paymentReference"]
        order_id = int(ref.replace("TMART-ORDER-", ""))
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = OrderStatus.PAID
            db.commit()
    return body



    
    


