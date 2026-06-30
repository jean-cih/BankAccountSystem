from fastapi import HTTPException
from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User


def add_income(db: Session, current_user: User, operation: OperationRequest):
    if not wallets_repository.is_wallet_exist(
        db, current_user.id, operation.wallet_name
    ):
        return HTTPException(
            status_code=404, detail=f"Wallet '{operation.wallet_name}' not found"
        )

    wallet = wallets_repository.add_income(
        db, current_user.id, operation.wallet_name, operation.amount
    )
    db.commit()

    return {
        "message": "Income is toped up",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": wallet.balance,
    }


def add_expense(db: Session, current_user: User, operation: OperationRequest):
    if not wallets_repository.is_wallet_exist(
        db, current_user.id, operation.wallet_name
    ):
        return HTTPException(
            status_code=404, detail=f"Wallet '{operation.wallet_name}' not found"
        )

    wallet = wallets_repository.get_balance_by_name(
        db, current_user.id, operation.wallet_name
    )

    if wallet.balance < operation.amount:
        return HTTPException(
            status_code=404,
            detail=f"On wallet '{operation.wallet_name}' is not money enough",
        )

    wallet = wallets_repository.add_expense(
        db, current_user.id, operation.wallet_name, operation.amount
    )
    db.commit()

    return {
        "message": "Expense is subtracted",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": wallet.balance,
    }
