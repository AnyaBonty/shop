from fastapi import FastAPI
from backend.app.api.v1 import user,product,order


app = FastAPI(title="Shop API")

app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)