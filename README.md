# Dating App

Ứng dụng web hẹn hò được xây dựng bằng Django.

## Tính năng

- Trang chủ giới thiệu ứng dụng
- Đăng ký và đăng nhập người dùng
- Hồ sơ người dùng
- Tìm kiếm và kết nối với người dùng khác

## Cài đặt

1. Tạo môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Cài đặt các dependencies:
```bash
pip install -r requirements.txt
```

3. Chạy migrations:
```bash
python manage.py migrate
```

4. Khởi động server:
```bash
python manage.py runserver
```

## Công nghệ sử dụng

- Django 5.0.2
- Bootstrap 5
- Crispy Forms
- SQLite (development) 