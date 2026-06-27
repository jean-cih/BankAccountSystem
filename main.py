from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

BALANCE = {}


class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: float
    description: str | None = Field(None, max_length=255)

    @field_validator('amount')
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be positive")

        return v

    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError("Wallet name can not be empty")

        return v


class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: float = 0

    @field_validator('name')
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError("Wallet name can not be empty")

        return v

    @field_validator('initial_balance')
    def balance_not_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Initial balance can not be negetive")

        return v


@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    if wallet_name is None:
        return {"total_balance": sum(BALANCE.values())}

    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )

    return {"wallet": wallet_name, "balance": BALANCE[wallet_name]}


@app.post("/wallets")
def create_wallet(wallet: CreateWalletRequest):
    if wallet.name in BALANCE:
        return HTTPException(
                status_code=400,
                detail=f"Wallet '{wallet.name}' already exists"
                )

    BALANCE[wallet.name] = wallet.initial_balance

    return {
        "message": "Wallet is done",
        "name": wallet.name,
        "balance": wallet.initial_balance
            }


@app.post("/operations/income")
def add_income(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        return HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found"
                )

    BALANCE[operation.wallet_name] += operation.amount

    return {
        "message": "Income is toped up",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
            }


@app.post("/operations/expense")
def add_expense(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        return HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found"
                )

    if BALANCE[operation.wallet_name] < operation.amount:
        return HTTPException(
                status_code=404,
                detail=f"On wallet '{operation.wallet_name}' is not money enough"
                )

    BALANCE[operation.wallet_name] -= operation.amount

    return {
        "message": "Expense is subtracted",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
            }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
