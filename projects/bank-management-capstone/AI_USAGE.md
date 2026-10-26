# AI Usage

## Tôi đã dùng AI cho việc gì?

- Hỗ trợ phác thảo cấu trúc module, rà soát các tình huống biên và tạo bộ test ban đầu.
- Hỗ trợ soạn tài liệu setup, usage, thiết kế và giới hạn của ứng dụng.

## Tôi đã tự viết hoặc thay đổi phần nào?

- Người học cần ghi rõ các phần đã tự triển khai, điều chỉnh hoặc không sử dụng sau khi review mã nguồn này.
- Không nên giữ nguyên mục này nếu chưa tự đọc và hiểu toàn bộ project.

## Tôi đã kiểm chứng câu trả lời của AI như thế nào?

- Chạy `python -m pytest -q tests` và readiness checker; điền kết quả thực tế sau khi chạy.
- Thử các trường hợp số tiền âm/0, số dư không đủ, tài khoản không tồn tại, file dữ liệu chưa tồn tại và JSON bị hỏng.
- Đối chiếu số dư trước/sau khi chuyển tiền và kiểm tra lịch sử của cả hai tài khoản.

## Một điều tôi hiểu rõ hơn

Sau khi tự chạy và xem lại project, hãy viết bằng lời của bạn cách `BankService` tách khỏi `JsonBankStorage` giúp kiểm thử logic mà không phụ thuộc file.
