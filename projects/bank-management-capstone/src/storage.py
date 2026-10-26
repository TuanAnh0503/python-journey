"""JSON persistence for bank account data."""
import json
from pathlib import Path
from typing import Any


class StorageError(Exception):
    """Raised when bank data cannot be read or written safely."""


class JsonBankStorage:
    """Load and save bank data in UTF-8 JSON format."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def load(self) -> dict[str, Any]:
        """Return empty data for a first run; reject malformed JSON."""
        if not self.path.exists():
            return {"accounts": [], "transactions": []}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise StorageError(f"File JSON không đọc được: {exc}") from exc
        if not isinstance(data, dict):
            raise StorageError("Dữ liệu gốc phải là một JSON object.")
        accounts = data.get("accounts", [])
        transactions = data.get("transactions", [])
        if not isinstance(accounts, list) or not isinstance(transactions, list):
            raise StorageError("'accounts' và 'transactions' phải là danh sách.")
        return {"accounts": accounts, "transactions": transactions}

    def save(self, data: dict[str, Any]) -> None:
        """Write to a temporary file first to reduce the risk of partial data."""
        try:
            serialized = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
            temporary_path.write_text(serialized, encoding="utf-8")
            temporary_path.replace(self.path)
        except (OSError, TypeError, ValueError) as exc:
            raise StorageError(f"Không thể lưu dữ liệu: {exc}") from exc
