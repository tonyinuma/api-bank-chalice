from chalice import (
    BadRequestError,
    Chalice,
    ConflictError,
    NotFoundError,
)
from pydantic import ValidationError

from chalicelib.repositories.account_repository import AccountRepository
from chalicelib.schemas.account import (
    AccountCreate,
    DepositRequest,
    WithdrawRequest,
)
from chalicelib.services.account_service import (
    AccountNotActiveError,
    AccountNotFoundError,
    AccountService,
    InsufficientFundsError,
)

app = Chalice(app_name="banking-api")

repository = AccountRepository()
service = AccountService(repository)


def serialize_account(account: dict) -> dict:
    return {
        "id": account["id"],
        "customer_name": account["customer_name"],
        "currency": account["currency"].value,
        "status": account["status"].value,
        "balance": str(account["balance"]),
    }


@app.route("/api/v1/accounts", methods=["POST"])
def create_account():
    try:
        data = AccountCreate(
            **app.current_request.json_body
        )
    except ValidationError as exc:
        raise BadRequestError(str(exc))

    account = service.create_account(data)

    return serialize_account(account)


@app.route("/api/v1/accounts", methods=["GET"])
def get_accounts():
    accounts = service.get_accounts()

    return [
        serialize_account(account)
        for account in accounts
    ]


@app.route("/api/v1/accounts/{account_id}", methods=["GET"])
def get_account(account_id):
    try:
        account = service.get_account(
            int(account_id)
        )
    except AccountNotFoundError:
        raise NotFoundError("Account not found")

    return serialize_account(account)

@app.route(
    "/api/v1/accounts/{account_id}/deposit",
    methods=["POST"],
)
def deposit(account_id):
    try:
        data = DepositRequest(
            **app.current_request.json_body
        )
    except ValidationError as exc:
        raise BadRequestError(str(exc))

    try:
        account = service.deposit(
            account_id=int(account_id),
            amount=data.amount,
        )
    except AccountNotFoundError:
        raise NotFoundError("Account not found")
    except AccountNotActiveError:
        raise ConflictError("Account is not active")

    return serialize_account(account)

@app.route(
    "/api/v1/accounts/{account_id}/withdraw",
    methods=["POST"],
)
def withdraw(account_id):
    try:
        data = WithdrawRequest(
            **app.current_request.json_body
        )
    except ValidationError as exc:
        raise BadRequestError(str(exc))

    try:
        account = service.withdraw(
            account_id=int(account_id),
            amount=data.amount,
        )
    except AccountNotFoundError:
        raise NotFoundError("Account not found")
    except AccountNotActiveError:
        raise ConflictError("Account is not active")
    except InsufficientFundsError:
        raise BadRequestError("Insufficient funds")

    return serialize_account(account)