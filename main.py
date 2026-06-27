from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

BALANCE = {}


class OperationRequest(BaseModel):
    wallet_name: str
    amount: float
    description: str | None = None


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


@app.post("/wallets/{name}")
def create_wallet(name: str, initial_balance: float = 0):
    if name in BALANCE:
        return HTTPException(
                status_code=400,
                detail=f"Wallet '{name}' already exists"
                )

    BALANCE[name] = initial_balance

    return {
        "message": "Wallet is done",
        "name": name,
        "balance": initial_balance
            }


@app.post("/operations/income")
def add_income(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        return HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found"
                )

    if operation.amount <= 0:
        return HTTPException(
                status_code=404,
                detail=f"Amount '{operation.amount}' is less or equal than 0"
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

    if operation.amount <= 0:
        return HTTPException(
                status_code=404,
                detail=f"Amount '{operation.amount}' must be positive"
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
