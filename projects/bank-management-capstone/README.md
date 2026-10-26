# Bank Management CLI

## Vấn đề và phạm vi

Ứng dụng dòng lệnh mô phỏng các thao tác ngân hàng cơ bản để luyện Python, chia module, xử lý lỗi, lưu file và kiểm thử. Đây là **mô hình học tập**, không phải phần mềm ngân hàng thật; không xử lý xác thực, mã hóa, lãi suất hoặc giao dịch với tổ chức tài chính.

Không thuộc phạm vi: giao diện đồ họa/web, đăng nhập và phân quyền, kết nối ngân hàng thật, nhiều người dùng đồng thời.

## Chức năng

1. Tạo tài khoản mới với số dư ban đầu bằng 0.
2. Xem danh sách tài khoản và số dư.
3. Nạp tiền và rút tiền; từ chối số tiền không hợp lệ hoặc số dư không đủ.
4. Chuyển tiền giữa hai tài khoản khác nhau.
5. Xem lịch sử giao dịch theo tài khoản.
6. Lưu và tải tài khoản/giao dịch từ JSON.

## Setup

Yêu cầu Python 3.12 trở lên. Tạo môi trường ảo nếu muốn, sau đó cài pytest để chạy test:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
python -m pip install pytest
```

Ứng dụng chính chỉ dùng thư viện chuẩn của Python.

## Usage

Từ thư mục `projects/bank-management-capstone`, chạy:

```bash
python main.py
```

Dữ liệu được tạo ở `data/bank_data.json` sau giao dịch lưu đầu tiên. Ví dụ: tạo tài khoản `An` (mã `0001`), nạp `100000`, tạo tài khoản `Bình` (mã `0002`), chuyển `25000` từ `0001` sang `0002`. Số dư cuối lần lượt là `75000` và `25000` VND.

## Test

```bash
python -m pytest -q
```

Bộ test bao gồm tạo tài khoản, nạp tiền, rút vượt số dư, số tiền bằng 0/âm, chuyển tiền, tài khoản không tồn tại, file chưa có, JSON hợp lệ và dữ liệu JSON hỏng/sai cấu trúc.

## Cấu trúc chính

- `main.py`: menu CLI, nhập liệu và hiển thị thông báo.
- `src/bank.py`: quy tắc nghiệp vụ và lịch sử giao dịch.
- `src/storage.py`: đọc/ghi JSON, xử lý lỗi file.
- `tests/test_bank.py`: kiểm thử nghiệp vụ và persistence.
- `data/`: nơi lưu dữ liệu phát sinh.

## Quyết định thiết kế

- Dùng `dict` để truy cập tài khoản theo mã và `list` để lưu lịch sử giao dịch.
- Tách `BankService` khỏi `JsonBankStorage` để test nghiệp vụ mà không cần đọc/ghi file.
- Số tiền biểu diễn bằng số nguyên VND, tránh sai số số thực trong phép tính tiền đơn giản.
- Lưu qua file tạm rồi thay thế file đích để giảm rủi ro dữ liệu bị ghi dở.

## Evidence

- Test cục bộ trong lúc dựng project: **11 passed**.
- Chạy readiness checker từ root repository:

```bash
python weeks/week-15-capstone-project/checks/check_capstone_readiness.py projects/bank-management-capstone
```

- Kết quả chạy trực tiếp trên repository cần được xác nhận riêng trước khi nộp.

## Known limitations

- Đây là ứng dụng học tập, không phải hệ thống tài chính an toàn.
- Chưa có xác thực người dùng, khóa file cho nhiều tiến trình, hoàn tác giao dịch hoặc cơ chế khôi phục từ bản sao lưu.
- ID được sinh theo dữ liệu hiện tại; không dùng làm mã định danh production.

## AI usage

Xem file `AI_USAGE.md`. Người nộp cần đọc, chạy thử và giải thích được các quyết định trong mã nguồn trước khi bảo vệ.
