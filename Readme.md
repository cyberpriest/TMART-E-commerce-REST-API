
# TMART API

E-commerce REST API built with FastAPI.

## Setup
```bash
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```

## Features
- JWT Auth + Refresh tokens
- Products & Categories
- Cart & Checkout
- Order state machine
- Monnify payments