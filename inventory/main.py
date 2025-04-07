from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

# CORS enable to allow the frontend (React app at localhost:3000) to fetch data from a FastAPI backend which
# runs on a different port (i.e., localhost:8000).
app.add_middleware(
    CORSMiddleware,
    
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


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis_db


@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post('/products')
def create(product: Product):
    return product.save()


@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)