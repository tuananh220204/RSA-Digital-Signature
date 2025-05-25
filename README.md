# RSA Digital Signature System

🔐 **Hệ thống chữ ký số RSA hoàn chỉnh với Python** - Tạo, ký và xác minh chữ ký số một cách an toàn và hiệu quả.

<!-- Chèn ảnh minh họa tại đây -->
![image](https://github.com/user-attachments/assets/6963b6af-4486-4b6b-bf47-a3943a2477bb)

*Giao diện web của hệ thống chữ ký số RSA*

## 🚀 Tính năng chính

### ✨ Tính năng cốt lõi
- **Tạo cặp khóa RSA**: Hỗ trợ khóa 2048-bit và 3072-bit
- **Ký số RSA-PSS**: Ký file với thuật toán RSA-PSS an toàn
- **Xác minh chữ ký**: Kiểm tra tính toàn vẹn và xác thực file
- **Bảo vệ khóa riêng**: Mã hóa khóa riêng bằng mật khẩu
- **Đa định dạng**: Hỗ trợ chữ ký binary (.sig) và base64 (.b64)

### 🌐 Giao diện đa dạng
- **Command Line Interface (CLI)**: Sử dụng qua terminal
- **Web Application**: Giao diện web thân thiện với Flask
- **Python API**: Tích hợp vào các dự án Python khác

### 🔒 Tính năng bảo mật
- Sử dụng thư viện `cryptography` chuẩn công nghiệp
- Hash file bằng SHA-256
- Thuật toán RSA-PSS với salt ngẫu nhiên
- Logging an toàn không ghi thông tin nhạy cảm
- Timestamp cho chữ ký (tùy chọn)

## 📋 Yêu cầu hệ thống

### Phần mềm cần thiết
- **Python**: 3.8 trở lên
- **pip**: Để cài đặt các thư viện phụ thuộc
- **Visual Studio Code** (khuyến nghị) hoặc IDE Python khác

### Thư viện phụ thuộc
```
cryptography>=41.0.0    # Mã hóa và chữ ký số
click>=8.1.0           # Command line interface
flask>=2.3.0           # Web application
werkzeug>=2.3.0        # Web server utilities
```

## 🛠️ Cài đặt & Chạy chương trình

### 1. Clone repository
```bash
git clone https://github.com/tuananh220204/RSA-Digital-Signature.git
cd RSA-Digital-Signature
```

### 2. Tạo môi trường ảo (khuyến nghị)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 4. Cài đặt package
```bash
pip install -e .
```

## 🖥️ Cách sử dụng

### Command Line Interface (CLI)

#### Tạo cặp khóa RSA
```bash
rsa-signature genkey --key-size 2048 --private-key private.pem --public-key public.pem --password
```

#### Ký file
```bash
rsa-signature sign document.pdf --private-key private.pem --password --format binary --timestamp
```

#### Xác minh chữ ký
```bash
rsa-signature verify document.pdf document.pdf.sig --public-key public.pem
```

### Web Application

#### Khởi động web server
```bash
python -m rsa_signature.webapp
```

Truy cập: `http://localhost:5000`

### Python API

```python
from rsa_signature import RSAKeyManager, RSASigner, RSAVerifier

# Tạo cặp khóa
key_manager = RSAKeyManager(key_size=2048)
key_manager.generate_keypair()
key_manager.save_private_key("private.pem", password="your_password")
key_manager.save_public_key("public.pem")

# Ký file
signer = RSASigner()
signature_path = signer.sign_and_save("document.pdf", "private.pem", password="your_password")

# Xác minh
verifier = RSAVerifier()
is_valid = verifier.verify_file("document.pdf", signature_path, "public.pem")
print(f"Chữ ký hợp lệ: {is_valid}")
```

## 📁 Cấu trúc dự án

```
RSA Digital Signature/
├── README.md                          # Tài liệu hướng dẫn dự án
├── requirements.txt                   # Danh sách thư viện phụ thuộc
├── setup.py                           # File cấu hình cài đặt package
├── rsa_signature.log                  # File log của ứng dụng
│
├── rsa_signature/                     # Package chính của dự án
│   ├── __init__.py                    # File khởi tạo package
│   ├── cli.py                         # Giao diện dòng lệnh (CLI)
│   ├── key_manager.py                 # Module quản lý khóa RSA
│   ├── signer.py                      # Module ký số
│   ├── verifier.py                    # Module xác thực chữ ký
│   ├── utils.py                       # Các hàm tiện ích
│   ├── timestamp.py                   # Module xử lý timestamp
│   ├── webapp.py                      # Ứng dụng web Flask
│   │
│   └── templates/                     # Thư mục chứa template HTML
│       ├── base.html                  # Template cơ sở
│       ├── index.html                 # Trang chủ
│       ├── generate_keys.html         # Trang tạo khóa
│       ├── keys_generated.html        # Trang hiển thị khóa đã tạo
│       ├── sign_file.html             # Trang ký file
│       ├── file_signed.html           # Trang hiển thị file đã ký
│       ├── verify_signature.html      # Trang xác thực chữ ký
│       └── verification_result.html   # Trang kết quả xác thực
│
├── tests/                             # Thư mục chứa test cases
│   ├── test_key_manager.py            # Test cho key_manager
│   └── test_signer_verifier.py        # Test cho signer và verifier
│
└── rsa_signature_system.egg-info/     # Thông tin package (tự động tạo)
    ├── PKG-INFO                       # Thông tin package
    ├── SOURCES.txt                    # Danh sách source files
    ├── dependency_links.txt           # Liên kết dependencies
    ├── entry_points.txt               # Entry points
    ├── requires.txt                   # Requirements
    └── top_level.txt                  # Top level packages
```

## ✅ Công nghệ sử dụng

- **Python**: Ngôn ngữ lập trình chính
- **Flask**: Framework web cho giao diện web
- **RSA Cryptography**: Thuật toán mã hóa RSA cho chữ ký số
- **HTML Templates**: Giao diện web thân thiện với người dùng

## 🎨 Giao diện sử dụng

### Tạo cặp khóa RSA
![image](https://github.com/user-attachments/assets/7a8766b0-9f2e-4920-b995-382f3cd2f346)


### Ký file bằng RSA-PSS
![image](https://github.com/user-attachments/assets/481534a8-a970-460c-b426-f909be7bd916)

### Xác minh chữ ký RSA-PSS
![image](https://github.com/user-attachments/assets/7634a39f-45f4-436d-8fe1-0258b0045d32)


## 🧪 Chạy Tests

```bash
# Chạy tất cả tests
python -m pytest tests/

# Chạy test cụ thể
python -m pytest tests/test_key_manager.py -v

# Test với coverage
python -m pytest tests/ --cov=rsa_signature
```

## 🔐 Bảo mật

### Khuyến nghị bảo mật
- Luôn sử dụng mật khẩu mạnh cho khóa riêng
- Lưu trữ khóa riêng ở nơi an toàn
- Không chia sẻ khóa riêng qua kênh không bảo mật
- Sử dụng HTTPS khi triển khai web application
- Thường xuyên cập nhật thư viện cryptography

### Thuật toán sử dụng
- **RSA Key Generation**: 2048/3072 bit với exponent 65537
- **Signature Algorithm**: RSA-PSS với MGF1
- **Hash Function**: SHA-256
- **Salt Length**: Maximum length (PSS.MAX_LENGTH)

## 👥 Tác giả

**Hà Tuấn Anh**
- GitHub: [@tuananh220204](https://github.com/tuananh220204)
- Email: tuananh22022004@gmail.com

## 🤝 Đóng góp

Tôi hoan nghênh mọi đóng góp! Vui lòng:

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Tạo Pull Request

## 📄 Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

```
MIT License

Copyright (c) 2025 Hà Tuấn Anh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📞 Hỗ trợ

Nếu bạn gặp vấn đề hoặc có câu hỏi:

- Tạo [Issue](https://github.com/tuananh220204/RSA-Digital-Signature/issues) trên GitHub
- Gửi email: tuananh22022004@gmail.com
- Xem [Wiki](https://github.com/tuananh220204/RSA-Digital-Signature/wiki) để có thêm tài liệu

---

⭐ **Nếu dự án này hữu ích, hãy cho tôi một ngôi sao trên GitHub!** ⭐
