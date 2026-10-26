"""Business rules for a small educational bank management system."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class BankError(Exception):
    """Raised when a banking operation violates a business rule."""


class BankService:
    """Manage accounts and transactions without depending on the CLI or files."""

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        if data is None:
            data = {}
        if not isinstance(data, dict):
            raise BankError("Dữ liệu ngân hàng phải là một object.")

        raw_accounts = data.get("accounts", [])
        raw_transactions = data.get("transactions", [])
        if not isinstance(raw_accounts, list):
            raise BankError("'accounts' phải là một danh sách.")
        if not isinstance(raw_transactions, list):
            raise BankError("'transactions' phải là một danh sách.")

        self._accounts: dict[str, dict[str, Any]] = {}
        self._transactions: list[dict[str, Any]] = []
        self._next_id = 1

        for raw in raw_accounts:
            if not isinstance(raw, dict):
                raise BankError("Mỗi tài khoản phải là một object.")
            if not {"id", "name", "balance"}.issubset(raw):
                raise BankError("Dữ liệu tài khoản bị thiếu trường bắt buộc.")

            raw_id = raw["id"]
            if not isinstance(raw_id, (str, int)) or isinstance(raw_id, bool):
                raise BankError("Mã tài khoản không hợp lệ.")
            account_id = str(raw_id).strip()
            name = raw["name"]
            balance = raw["balance"]
            if (
                not account_id
                or not isinstance(name, str)
                or not name.strip()
                or not isinstance(balance, int)
                or isinstance(balance, bool)
                or balance < 0
            ):
                raise BankError("Dữ liệu tài khoản không hợp lệ.")
            if account_id in self._accounts:
                raise BankError("Dữ liệu có mã tài khoản trùng lặp.")

            self._accounts[account_id] = {
                "id": account_id,
                "name": name.strip(),
                "balance": balance,
            }
            if account_id.isdigit():
                self._next_id = max(self._next_id, int(account_id) + 1)

        for item in raw_transactions:
            if not isinstance(item, dict):
                raise BankError("Mỗi giao dịch phải là một object.")
            required = {"account_id", "type", "amount", "note", "timestamp"}
            if not required.issubset(item):
                raise BankError("Dữ liệu giao dịch bị thiếu trường bắt buộc.")

            account_id = item["account_id"]
            transaction_type = item["type"]
            amount = item["amount"]
            note = item["note"]
            timestamp = item["timestamp"]
            if (
                not isinstance(account_id, str)
                or account_id.strip() not in self._accounts
                or not isinstance(transaction_type, str)
                or not transaction_type.strip()
                or not isinstance(amount, int)
                or isinstance(amount, bool)
                or amount <= 0
                or not isinstance(note, str)
                or not isinstance(timestamp, str)
                or not timestamp.strip()
            ):
                raise BankError("Dữ liệu lịch sử giao dịch không hợp lệ.")
            normalized = dict(item)
            normalized["account_id"] = account_id.strip()
            self._transactions.append(normalized)

    def create_account(self, name: str) -> dict[str, Any]:
        """Create an account with a zero balance and return a copy."""
        if not isinstance(name, str):
            raise BankError("Tên chủ tài khoản phải là chuỗi.")
        clean_name = name.strip()
        if not clean_name:
            raise BankError("Tên chủ tài khoản không được để trống.")
        account_id = f"{self._next_id:04d}"
        self._next_id += 1
        account = {"id": account_id, "name": clean_name, "balance": 0}
        self._accounts[account_id] = account
        return dict(account)

    def list_accounts(self) -> list[dict[str, Any]]:
        """Return account copies sorted by ID."""
        return [dict(self._accounts[key]) for key in sorted(self._accounts)]

    def get_account(self, account_id: str) -> dict[str, Any]:
        """Return one account or raise a clear business error."""
        return dict(self._require_account(account_id))

    def deposit(self, account_id: str, amount: int) -> None:
        """Add a positive amount to an account."""
        self._validate_amount(amount)
        account = self._require_account(account_id)
        account["balance"] += amount
        self._record(account_id, "NẠP TIỀN", amount, "Nạp tiền vào tài khoản")

    def withdraw(self, account_id: str, amount: int) -> None:
        """Withdraw money only when the account has sufficient funds."""
        self._validate_amount(amount)
        account = self._require_account(account_id)
        if account["balance"] < amount:
            raise BankError("Số dư không đủ để thực hiện giao dịch.")
        account["balance"] -= amount
        self._record(account_id, "RÚT TIỀN", amount, "Rút tiền khỏi tài khoản")

    def transfer(self, source_id: str, target_id: str, amount: int) -> None:
        """Transfer money between two distinct existing accounts."""
        self._validate_amount(amount)
        source_key = self._clean_account_id(source_id)
        target_key = self._clean_account_id(target_id)
        if source_key == target_key:
            raise BankError("Tài khoản gửi và nhận phải khác nhau.")
        source = self._require_account(source_key)
        target = self._require_account(target_key)
        if source["balance"] < amount:
            raise BankError("Số dư không đủ để chuyển tiền.")
        source["balance"] -= amount
        target["balance"] += amount
        self._record(source_key, "CHUYỂN ĐI", amount, f"Chuyển đến {target_key}")
        self._record(target_key, "NHẬN TIỀN", amount, f"Nhận từ {source_key}")

    def get_transactions(self, account_id: str) -> list[dict[str, Any]]:
        """Return the transaction history for a known account."""
        clean_id = self._clean_account_id(account_id)
        self._require_account(clean_id)
        return [
            dict(item)
            for item in self._transactions
            if item["account_id"] == clean_id
        ]

    def export_data(self) -> dict[str, Any]:
        """Return a JSON-serializable snapshot."""
        return {
            "accounts": self.list_accounts(),
            "transactions": [dict(item) for item in self._transactions],
        }

    @staticmethod
    def _clean_account_id(account_id: str) -> str:
        if not isinstance(account_id, str):
            raise BankError("Mã tài khoản phải là chuỗi.")
        clean_id = account_id.strip()
        if not clean_id:
            raise BankError("Mã tài khoản không được để trống.")
        return clean_id

    def _require_account(self, account_id: str) -> dict[str, Any]:
        clean_id = self._clean_account_id(account_id)
        if clean_id not in self._accounts:
            raise BankError(f"Không tìm thấy tài khoản '{clean_id}'.")
        return self._accounts[clean_id]

    @staticmethod
    def _validate_amount(amount: int) -> None:
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            raise BankError("Số tiền phải là số nguyên dương.")

    def _record(self, account_id: str, transaction_type: str, amount: int, note: str) -> None:
        self._transactions.append({
            "account_id": account_id.strip(),
            "type": transaction_type,
            "amount": amount,
            "note": note,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })
