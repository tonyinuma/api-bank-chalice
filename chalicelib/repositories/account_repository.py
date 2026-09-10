from decimal import Decimal

from chalicelib.schemas.account import (
    AccountCreate,
    AccountStatus,
)


class AccountRepository:
    def __init__(self) -> None:
        self._accounts: list[dict] = []
        self._current_id = 0

    def create(self, data: AccountCreate) -> dict:
        self._current_id += 1

        account = {
            "id": self._current_id,
            "customer_name": data.customer_name,
            "currency": data.currency,
            "status": AccountStatus.ACTIVE,
            "balance": Decimal("0.00"),
        }

        self._accounts.append(account)

        return account

    def find_all(self) -> list[dict]:
        return self._accounts

    def find_by_id(self, account_id: int) -> dict | None:
        return next(
            (
                account
                for account in self._accounts
                if account["id"] == account_id
            ),
            None,
        )