"""Business rules for a small educational bank management system."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class BankError(Exception):
    """Raised when a banking operation violates a business rule."""


class BankService:
    """Manage accounts and transactions without depending on the CLI or files."""

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        data = data or {}
        self._accounts: dict[str, dict[str, Any]] = {}
        self._transactions: list[dict[str, Any]] = []
        self._next_id = 1
        for raw in data.get("accounts", []):
            account_id = str(raw["id"])
            name = str(raw["name"]).strip()
            balance = raw["balance"]
            if not name or not isinstance(balance, int) or isinstance(balance, bool) or balance < 0:
                raise BankError("Dữ liệu tài khoản không hợp lệ.")
            if account_id in self._accounts:
                raise BankError("Dữ liệu có mã tài khoản trùng lặp.")
            self._accounts[account_id] = {"id": account_id, "name": name, "balance": balance}
            if account_id.isdigit():
                self._next_id = max(self._next_id, int(account_id) + 1)
        transactions = data.get("transactions", [])
        if not isinstance(transactions, list) or any(not isinstance(item, dict) for item in transactions):
            raise BankError("Dữ liệu lịch sử giao dịch không hợp lệ.")
        self._transactions = [dict(item) for item in transactions]

    def create_account(self, name: str) -> dict[str, Any]:
        """Create an account with a zero balance and return a copy."""
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
        try:
            return dict(self._accounts[account_id.strip()])
        except KeyError as exc:
            raise BankError(f"Không tìm thấy tài khoản '{account_id}'.") from exc

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
        if source_id.strip() == target_id.strip():
            raise BankError("Tài khoản gửi và nhận phải khác nhau.")
        source = self._require_account(source_id)
        target = self._require_account(target_id)
        if source["balance"] < amount:
            raise BankError("Số dư không đủ để chuyển tiền.")
        source["balance"] -= amount
        target["balance"] += amount
        self._record(source_id, "CHUYỂN ĐI", amount, f"Chuyển đến {target_id.strip()}")
        self._record(target_id, "NHẬN TIỀN", amount, f"Nhận từ {source_id.strip()}")

    def get_transactions(self, account_id: str) -> list[dict[str, Any]]:
        """Return the transaction history for a known account."""
        self._require_account(account_id)
        return [dict(item) for item in self._transactions if item["account_id"] == account_id.strip()]

    def export_data(self) -> dict[str, Any]:
        """Return a JSON-serializable snapshot."""
        return {
            "accounts": self.list_accounts(),
            "transactions": [dict(item) for item in self._transactions],
        }

    def _require_account(self, account_id: str) -> dict[str, Any]:
        clean_id = account_id.strip()
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
