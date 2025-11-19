from fastapi import FastAPI
from backend.app.api.v1 import user,product,order,role,auth


app = FastAPI(title="Shop API")

app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(role.router)
app.include_router(auth.router)