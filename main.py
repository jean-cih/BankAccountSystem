from fastapi import FastAPI

from app.api.v1.wallets import router as wallet_router
from app.api.v1.operations import router as operation_router
from app.api.v1.users import router as user_router

from app.database import engine, Base

app = FastAPI()

app.include_router(wallet_router, prefix="/api/v1", tags=["wallet"])
app.include_router(operation_router, prefix="/api/v1", tags=["operations"])
app.include_router(user_router, prefix="/api/v1", tags=["users"])

Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
