"""
Các tiện ích chung cho hệ thống chữ ký số RSA
"""

import os
import base64
import hashlib
import logging
from pathlib import Path
from typing import Optional, Union

# Cấu hình logging an toàn
def setup_logging(level: str = "INFO") -> logging.Logger:
    """Thiết lập logging không ghi thông tin nhạy cảm"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('rsa_signature.log')
        ]
    )
    
    # Tạo filter để loại bỏ thông tin nhạy cảm
    class SensitiveDataFilter(logging.Filter):
        def filter(self, record):
            # Loại bỏ các từ khóa nhạy cảm khỏi log
            sensitive_keywords = ['password', 'private_key', 'secret']
            message = record.getMessage().lower()
            return not any(keyword in message for keyword in sensitive_keywords)
    
    logger = logging.getLogger('rsa_signature')
    logger.addFilter(SensitiveDataFilter())
    return logger

def ensure_directory(path: Union[str, Path]) -> Path:
    """Đảm bảo thư mục tồn tại"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def safe_file_read(file_path: Union[str, Path]) -> bytes:
    """Đọc file một cách an toàn"""
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File không tồn tại: {file_path}")
    except PermissionError:
        raise PermissionError(f"Không có quyền đọc file: {file_path}")
    except Exception as e:
        raise IOError(f"Lỗi khi đọc file {file_path}: {str(e)}")

def safe_file_write(file_path: Union[str, Path], data: bytes, mode: str = 'wb') -> None:
    """Ghi file một cách an toàn"""
    try:
        ensure_directory(Path(file_path).parent)
        with open(file_path, mode) as f:
            f.write(data)
    except PermissionError:
        raise PermissionError(f"Không có quyền ghi file: {file_path}")
    except Exception as e:
        raise IOError(f"Lỗi khi ghi file {file_path}: {str(e)}")

def encode_base64(data: bytes) -> str:
    """Mã hóa dữ liệu thành base64"""
    return base64.b64encode(data).decode('utf-8')

def decode_base64(data: str) -> bytes:
    """Giải mã dữ liệu từ base64"""
    try:
        return base64.b64decode(data)
    except Exception as e:
        raise ValueError(f"Lỗi giải mã base64: {str(e)}")

def hash_file(file_path: Union[str, Path]) -> bytes:
    """Hash file bằng SHA-256"""
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.digest()
    except Exception as e:
        raise IOError(f"Lỗi khi hash file {file_path}: {str(e)}")

def validate_file_path(file_path: Union[str, Path]) -> Path:
    """Kiểm tra và validate đường dẫn file"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File không tồn tại: {file_path}")
    if not path.is_file():
        raise ValueError(f"Đường dẫn không phải là file: {file_path}")
    return path