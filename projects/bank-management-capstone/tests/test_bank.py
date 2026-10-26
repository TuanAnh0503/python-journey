"""Tests for bank business rules and JSON persistence."""
import json

import pytest

from src.bank import BankError, BankService
from src.storage import JsonBankStorage, StorageError


def make_bank() -> BankService:
    bank = BankService()
    bank.create_account("An")
    bank.create_account("Bình")
    bank.deposit("0001", 100_000)
    return bank


def test_create_account_rejects_empty_name() -> None:
    with pytest.raises(BankError, match="Tên"):
        BankService().create_account("   ")


def test_deposit_updates_balance_and_records_history() -> None:
    bank = BankService()
    bank.create_account("An")
    bank.deposit("0001", 25_000)
    assert bank.get_account("0001")["balance"] == 25_000
    assert len(bank.get_transactions("0001")) == 1


def test_withdraw_rejects_insufficient_funds_without_mutation() -> None:
    bank = make_bank()
    with pytest.raises(BankError, match="không đủ"):
        bank.withdraw("0001", 100_001)
    assert bank.get_account("0001")["balance"] == 100_000


def test_zero_or_negative_amount_is_rejected() -> None:
    bank = make_bank()
    for amount in (0, -1):
        with pytest.raises(BankError, match="số nguyên dương"):
            bank.deposit("0001", amount)


def test_transfer_moves_funds_and_records_both_sides() -> None:
    bank = make_bank()
    bank.transfer("0001", "0002", 30_000)
    assert bank.get_account("0001")["balance"] == 70_000
    assert bank.get_account("0002")["balance"] == 30_000
    assert len(bank.get_transactions("0001")) == 2
    assert len(bank.get_transactions("0002")) == 1


def test_transfer_to_same_account_is_rejected() -> None:
    bank = make_bank()
    with pytest.raises(BankError, match="phải khác nhau"):
        bank.transfer("0001", "0001", 10_000)
    assert bank.get_account("0001")["balance"] == 100_000


def test_unknown_account_is_reported() -> None:
    with pytest.raises(BankError, match="Không tìm thấy"):
        BankService().get_account("9999")


def test_storage_missing_file_returns_empty_data(tmp_path) -> None:
    storage = JsonBankStorage(tmp_path / "bank.json")
    assert storage.load() == {"accounts": [], "transactions": []}


def test_storage_round_trip_preserves_vietnamese(tmp_path) -> None:
    storage = JsonBankStorage(tmp_path / "nested" / "bank.json")
    data = {"accounts": [{"id": "0001", "name": "Nguyễn An", "balance": 500}], "transactions": []}
    storage.save(data)
    assert storage.load() == data


def test_storage_rejects_malformed_json(tmp_path) -> None:
    path = tmp_path / "bank.json"
    path.write_text("{bad json", encoding="utf-8")
    with pytest.raises(StorageError, match="JSON"):
        JsonBankStorage(path).load()


def test_storage_rejects_unexpected_json_shape(tmp_path) -> None:
    path = tmp_path / "bank.json"
    path.write_text(json.dumps(["unexpected"]), encoding="utf-8")
    with pytest.raises(StorageError, match="object"):
        JsonBankStorage(path).load()
