from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time

app = FastAPI()

# CORS enable to allow the frontend (React app at frontend-service:3000) to fetch data from a FastAPI backend which
# runs on a different port (i.e., inventory-service:8000).
app.add_middleware(
    CORSMiddleware,
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! frontend-service
    allow_origins=['http://inventory-frontend-service:3000', 'http://payment-frontend-deployment:3001'], # Allow requests from this origin.    
    allow_methods=['*'], # Allow all HTTP methods (GET, POST, PUT, etc.).
    allow_headers=['*'] # Allow all headers in requests.
)

redis_db = get_redis_connection(
    host="redis-14176.c331.us-west1-1.gce.redns.redis-cloud.com",
    port=14176,
    password="LepcKJVMfM0iyyL9UDCXlNvwdt1xwelK",
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis_db


@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)


@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):  # id, quantity
    body = await request.json()

    # Get information about the product from the inventory database => make a get request to the inventory db.
    # !!!!!!!!!!!!!!!!!!!!!!!!! inventory-service
    req = requests.get('http://inventory-service:8000/products/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()

    # FastAPI executes the function order_completed in the background, return a status "completed" when the order is completed.
    background_tasks.add_task(order_completed, order)

    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    # The payment service communicate asynchronously with inventory service through Redis Stream by sending an event, requesting the inventory
    # db to adjust the product's quantity once the order is completed. The last parameter '*' mean the id will be auto generated. 
    redis_db.xadd('order_completed', order.model_dump(), '*')