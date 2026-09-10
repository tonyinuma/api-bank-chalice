from chalicelib.repositories.account_repository import AccountRepository
from chalicelib.schemas.account import AccountCreate


class AccountNotFoundError(Exception):
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