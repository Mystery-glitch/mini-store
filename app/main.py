from contextlib import asynccontextmanager

from fastapi import FastAPI,Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import InsufficientStockException,OrderNotFoundException,ProductNotFoundException
from app.db.base import Base
from app.db.database import engine
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.timing import TimingMiddleware

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Starting Mini Store API...")
    Base.metadata.create_all(bind=engine)
    yield
    print("Shutting down Mini Store API...")

app=FastAPI(title=settings.app_name,version=settings.app_version,description="A complete FastAPI learning project",lifespan=lifespan)

# cors
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origin,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

# custom middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimingMiddleware)

# static files
app.mount("/static",StaticFiles(directory="app/static"),name="static")

# routers
app.include_router(api_router)

# basic routes
@app.get("/",tags=["System"])
def root():
    return {
        "application":settings.app_name,
        "version":settings.app_version,
        "message":"API is running"
    }

@app.get("/health",tags=["System"])
def health():
    return {
        "status":"healthy"
    }

# exception handlers
@app.exception_handler(ProductNotFoundException)
async def product_not_found_handler(request:Request,exc:ProductNotFoundException):
    return JSONResponse(status_code=404,content={
        "error":"PRODUCT_NOT_FOUND",
        "message":(f"Product {exc.product_id} " "does not exist")
    })

@app.exception_handler(OrderNotFoundException)
async def order_not_found_handler(request:Request,exc:OrderNotFoundException):
    return JSONResponse(status_code=404,content={
        "error":"ORDER_NOT_FOUND",
        "message":(f"Order {exc.order_id} " "does not exist")
    })

@app.exception_handler(InsufficientStockException)
async def insufficient_stock_handler(request:Request,exc:InsufficientStockException):
    return JSONResponse(status_code=409,content={
        "error":"INSUFFICIENT_STOCK",
        "message":(f"Product {exc.product_id} " "does not have enough stock")
    })

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request:Request,exc:RequestValidationError):
    return JSONResponse(status_code=422,content={
        "error":"VALIDATION_ERROR",
        "details":exc.errors()
    })