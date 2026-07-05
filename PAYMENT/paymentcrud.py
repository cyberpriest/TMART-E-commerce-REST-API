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
    # if order.status != OrderStatus.PENDING:
    #     raise HTTPException(status_code=400, detail=' order is not in pending ')
    
    init_pay = initialize_payment(
        amount=order.total,
        order_id = order.id,
        email = user.email,
        full_name = user.full_name
        )
    if not init_pay:
        raise HTTPException(status_code=502, detail='Monnify did not return a payment initialization payload')

    checkout_url = init_pay.get('checkoutUrl')
    payment_reference = init_pay.get('paymentReference')
    transaction_reference = init_pay.get('transactionReference')

    if not checkout_url or not payment_reference or not transaction_reference:
        raise HTTPException(status_code=502, detail='Monnify returned an incomplete payment initialization payload')

    order.payment_reference = payment_reference
    db.commit()
    db.refresh(order)

    return  {
        'checkoutUrl': checkout_url,
        'paymentReference': payment_reference,
        'transactionReference': transaction_reference
    }
    
    

def verify_payment(db:Session,transaction_reference:str):
    token = get_access_token()
    res = httpx.get(
        f'{MONNIFY_BASE_URL}/api/v1/merchant/transactions/query',
        headers = {'Authorization':f'Bearer {token}'},
        params={'paymentReference':transaction_reference}

        )
    data = res.json()
    if not data.get('requestSuccessful'):
        raise HTTPException(status_code=400,detail='Monnify auth failed')


    body = data.get("responseBody") or {}
    if body.get("paymentStatus") == "PAID":
        # update order status
        ref = body.get("paymentReference")
        if ref:
            order = db.query(Order).filter(Order.payment_reference == ref).first()
            if not order:
                # fall back to older reference format
                try:
                    order_id = int(ref.replace("TMART-ORDER-", "").split("-")[0])
                except (ValueError, AttributeError):
                    order_id = None
                if order_id:
                    order = db.query(Order).filter(Order.id == order_id).first()
            if order:
                order.status = OrderStatus.PAID
                db.commit()
    return body



    
    


