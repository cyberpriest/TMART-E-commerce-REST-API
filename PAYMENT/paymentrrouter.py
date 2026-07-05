from fastapi import APIRouter ,Depends,HTTPException,status
import auth,schema,database,models,auth
from sqlalchemy.orm import Session
from PAYMENT.paymentcrud import init_payment,verify_payment

payment_router = APIRouter(prefix='/payment',tags=['PAYMENT'])

@payment_router.post('/ini-pay/{order_id}')
def ini_payment(order_id:int,db:Session = Depends(database.get_db),user:models.User = Depends(auth.get_current_user)):
    return init_payment(db,order_id,user)


@payment_router.get('/verify/{transaction_reference}')
def verify(
    transaction_reference: str,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(auth.get_current_user)
):
    return verify_payment(db, transaction_reference)





