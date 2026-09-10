from decimal import Decimal

from chalicelib.repositories.account_repository import AccountRepository
from chalicelib.schemas.account import (
    AccountCreate,
    AccountStatus,
)


class AccountNotFoundError(Exception):
    pass


class AccountNotActiveError(Exception):
    pass


class AccountService:
    def __init__(self, repository: AccountRepository) -> None:
        self.repository = repository

    def create_account(self, data: AccountCreate) -> dict:
        return self.repository.create(data)

    def get_accounts(self) -> list[dict]:
        return self.repository.find_all()

    def get_account(self, account_id: int) -> dict:
        account = self.repository.find_by_id(account_id)

        if account is None:
            raise AccountNotFoundError()

        return account

    def deposit(
        self,
        account_id: int,
        amount: Decimal,
    ) -> dict:
        account = self.repository.find_by_id(account_id)

        if account is None:
            raise AccountNotFoundError()

        if account["status"] != AccountStatus.ACTIVE:
            raise AccountNotActiveError()

        new_balance = account["balance"] + amount

        return self.repository.update_balance(
            account_id=account_id,
            new_balance=new_balance,
        )