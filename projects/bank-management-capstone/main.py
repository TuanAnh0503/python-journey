"""Interactive command-line interface for the bank management capstone."""
from pathlib import Path

from src.bank import BankService, BankError
from src.storage import JsonBankStorage, StorageError

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "bank_data.json"


def read_positive_amount(prompt: str) -> int:
    """Read a positive whole-number amount of Vietnamese dong."""
    raw = input(prompt).strip()
    try:
        amount = int(raw)
    except ValueError as exc:
        raise ValueError("Số tiền phải là số nguyên.") from exc
    if amount <= 0:
        raise ValueError("Số tiền phải lớn hơn 0.")
    return amount


def print_accounts(bank: BankService) -> None:
    """Print all accounts in a compact table."""
    accounts = bank.list_accounts()
    if not accounts:
        print("Chưa có tài khoản nào.")
        return
    print("\nMÃ TÀI KHOẢN | CHỦ TÀI KHOẢN | SỐ DƯ (VND)")
    print("-" * 52)
    for account in accounts:
        print(f"{account['id']:<13} | {account['name']:<15} | {account['balance']:>12,}")


def run() -> None:
    """Run the menu until the user chooses to exit."""
    storage = JsonBankStorage(DATA_FILE)
    try:
        bank = BankService(storage.load())
    except (StorageError, BankError) as exc:
        print(f"Không thể đọc dữ liệu: {exc}")
        return

    while True:
        print("\n=== BANK MANAGEMENT CLI ===")
        print("1. Xem danh sách tài khoản")
        print("2. Tạo tài khoản")
        print("3. Nạp tiền")
        print("4. Rút tiền")
        print("5. Chuyển tiền")
        print("6. Xem lịch sử giao dịch")
        print("0. Thoát")
        choice = input("Chọn chức năng: ").strip()

        try:
            if choice == "1":
                print_accounts(bank)
            elif choice == "2":
                name = input("Tên chủ tài khoản: ").strip()
                account = bank.create_account(name)
                storage.save(bank.export_data())
                print(f"Đã tạo tài khoản {account['id']} cho {account['name']}.")
            elif choice == "3":
                account_id = input("Mã tài khoản: ").strip()
                amount = read_positive_amount("Số tiền cần nạp (VND): ")
                bank.deposit(account_id, amount)
                storage.save(bank.export_data())
                print("Nạp tiền thành công.")
            elif choice == "4":
                account_id = input("Mã tài khoản: ").strip()
                amount = read_positive_amount("Số tiền cần rút (VND): ")
                bank.withdraw(account_id, amount)
                storage.save(bank.export_data())
                print("Rút tiền thành công.")
            elif choice == "5":
                source = input("Tài khoản gửi: ").strip()
                target = input("Tài khoản nhận: ").strip()
                amount = read_positive_amount("Số tiền chuyển (VND): ")
                bank.transfer(source, target, amount)
                storage.save(bank.export_data())
                print("Chuyển tiền thành công.")
            elif choice == "6":
                account_id = input("Mã tài khoản: ").strip()
                transactions = bank.get_transactions(account_id)
                if not transactions:
                    print("Tài khoản chưa có giao dịch.")
                for item in transactions:
                    print(f"{item['timestamp']} | {item['type']} | {item['amount']:,} VND | {item['note']}")
            elif choice == "0":
                print("Đã thoát chương trình.")
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
        except (BankError, ValueError, StorageError) as exc:
            print(f"Không thể thực hiện: {exc}")


if __name__ == "__main__":
    run()
