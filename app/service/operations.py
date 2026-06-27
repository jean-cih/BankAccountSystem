from fastapi import HTTPException
from app.schemas import OperationRequest
from app.repository.wallets import BALANCE


def add_income(operation: OperationRequest):

    if operation.wallet_name not in BALANCE:
        return HTTPException(
            status_code=404, detail=f"Wallet '{operation.wallet_name}' not found"
        )

    BALANCE[operation.wallet_name] += operation.amount

    return {
        "message": "Income is toped up",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name],
    }


def add_expense(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        return HTTPException(
            status_code=404, detail=f"Wallet '{operation.wallet_name}' not found"
        )

    if BALANCE[operation.wallet_name] < operation.amount:
        return HTTPException(
            status_code=404,
            detail=f"On wallet '{operation.wallet_name}' is not money enough",
        )

    BALANCE[operation.wallet_name] -= operation.amount

    return {
        "message": "Expense is subtracted",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name],
    }
