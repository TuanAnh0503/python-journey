# Kịch bản demo capstone (5–8 phút)

Tài liệu này là gợi ý luyện tập. Khi bảo vệ, hãy dùng lời của bạn và chỉ trình bày những phần bạn đã tự chạy, kiểm tra và hiểu.

## Kịch bản 6 phút

### 0:00–0:40 — Nêu vấn đề

“Đây là chương trình dòng lệnh mô phỏng quản lý tài khoản ngân hàng. Mục tiêu là thực hành chia module, kiểm tra dữ liệu đầu vào, lưu dữ liệu JSON và viết test; chương trình không kết nối ngân hàng thật.”

### 0:40–1:20 — Giới thiệu cấu trúc

- `main.py`: menu, nhập dữ liệu và hiển thị kết quả.
- `src/bank.py`: luật nghiệp vụ tài khoản, nạp/rút/chuyển tiền, lịch sử.
- `src/storage.py`: tải/lưu dữ liệu JSON.
- `tests/test_bank.py`: kiểm thử hành vi bình thường và trường hợp lỗi.

Nhấn mạnh rằng tách nghiệp vụ khỏi lưu trữ giúp kiểm thử `BankService` mà không cần tạo file dữ liệu cho mọi test.

### 1:20–3:20 — Demo luồng chính

1. Chạy `python main.py`.
2. Tạo tài khoản chủ tài khoản `An`.
3. Nạp `100000` VND vào tài khoản `0001`.
4. Tạo tài khoản `Bình` (`0002`).
5. Chuyển `25000` VND từ `0001` sang `0002`.
6. Xem danh sách tài khoản và lịch sử giao dịch.

Kết quả cần đối chiếu: tài khoản `0001` còn `75000` VND, tài khoản `0002` có `25000` VND. Nếu dữ liệu đã có từ lần chạy trước, hãy dùng file dữ liệu thử riêng hoặc xóa file dữ liệu demo trước khi diễn tập; không xóa dữ liệu quan trọng của bạn.

### 3:20–4:20 — Chứng minh xử lý lỗi

Thử một vài trường hợp:

- Nhập số tiền `0` hoặc số âm.
- Rút nhiều hơn số dư hiện có.
- Tra cứu mã tài khoản không tồn tại.

Giải thích thông báo lỗi có ý nghĩa gì và vì sao số dư không nên bị thay đổi khi thao tác bị từ chối.

### 4:20–5:20 — Chạy test

Từ thư mục project:

```bash
python -m pytest -q tests
```

Hoặc từ root repository:

```bash
python -m pytest -q projects/bank-management-capstone/tests
```

Nói ngắn gọn test nào kiểm tra chuyển tiền, số dư không đủ, dữ liệu JSON hỏng và giao dịch không hợp lệ. Chỉ nêu kết quả vừa quan sát được trên máy.

### 5:20–6:00 — Quyết định thiết kế và cải tiến

Giải thích:

- Vì sao tiền dùng số nguyên VND thay vì số thực.
- Vì sao tài khoản được lưu trong `dict`, còn lịch sử là `list`.
- Một giới hạn hiện tại: nếu ghi file thất bại sau thao tác nghiệp vụ, trạng thái trong bộ nhớ có thể đã thay đổi. Có thể cải tiến bằng cơ chế lưu giao dịch/rollback chặt chẽ hơn.

## Câu hỏi nên tự luyện

1. **Tại sao tách `BankService` và `JsonBankStorage`?**  
   Vì nghiệp vụ không cần phụ thuộc file, dễ kiểm thử riêng và dễ thay cách lưu dữ liệu.

2. **Tại sao số tiền phải là số nguyên dương?**  
   Chặn số 0, số âm, chuỗi và kiểu `bool`; ứng dụng mô phỏng dùng đơn vị VND nguyên để tránh sai số số thực.

3. **Nếu JSON sai định dạng thì sao?**  
   Lớp lưu trữ chuyển lỗi đọc/giải mã thành `StorageError`; cấu trúc bản ghi sai được `BankService` báo bằng `BankError`.

4. **Test khác demo thế nào?**  
   Demo cho thấy luồng dùng thực tế; test chạy tự động để kiểm tra nhiều tình huống và dễ phát hiện lỗi khi sửa code.

5. **Những gì chưa được giải quyết?**  
   Chưa có đăng nhập/phân quyền, khóa file cho nhiều tiến trình, rollback khi ghi file thất bại hay các yêu cầu bảo mật của hệ thống ngân hàng thật.
