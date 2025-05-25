"""
Quản lý khóa RSA: tạo, lưu trữ, tải khóa
"""

import os
from pathlib import Path
from typing import Tuple, Optional
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

from .utils import setup_logging, safe_file_write, safe_file_read, ensure_directory

logger = setup_logging()

class RSAKeyManager:
    """Quản lý khóa RSA"""
    
    def __init__(self, key_size: int = 2048):
        """
        Khởi tạo RSA Key Manager
        
        Args:
            key_size: Kích thước khóa (2048 hoặc 3072 bit)
        """
        if key_size not in [2048, 3072]:
            raise ValueError("Kích thước khóa phải là 2048 hoặc 3072 bit")
        
        self.key_size = key_size
        self.private_key = None
        self.public_key = None
    
    def generate_keypair(self) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """
        Tạo cặp khóa RSA mới
        
        Returns:
            Tuple chứa private key và public key
        """
        try:
            logger.info(f"Đang tạo cặp khóa RSA {self.key_size} bit...")
            
            # Tạo khóa riêng
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=self.key_size,
            )
            
            # Lấy khóa công khai
            public_key = private_key.public_key()
            
            self.private_key = private_key
            self.public_key = public_key
            
            logger.info("Tạo cặp khóa thành công")
            return private_key, public_key
            
        except Exception as e:
            logger.error(f"Lỗi khi tạo cặp khóa: {str(e)}")
            raise RuntimeError(f"Không thể tạo cặp khóa: {str(e)}")
    
    def save_private_key(self, file_path: str, password: Optional[str] = None) -> None:
        """
        Lưu khóa riêng ra file
        
        Args:
            file_path: Đường dẫn file để lưu khóa riêng
            password: Mật khẩu để mã hóa khóa riêng (tùy chọn)
        """
        if not self.private_key:
            raise ValueError("Chưa có khóa riêng để lưu")
        
        try:
            # Chuẩn bị encryption algorithm
            encryption_algorithm = serialization.NoEncryption()
            if password:
                encryption_algorithm = serialization.BestAvailableEncryption(
                    password.encode('utf-8')
                )
            
            # Serialize khóa riêng
            private_pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=encryption_algorithm
            )
            
            # Lưu file
            safe_file_write(file_path, private_pem)
            logger.info(f"Đã lưu khóa riêng vào {file_path}")
            
        except Exception as e:
            logger.error(f"Lỗi khi lưu khóa riêng: {str(e)}")
            raise IOError(f"Không thể lưu khóa riêng: {str(e)}")
    
    def save_public_key(self, file_path: str) -> None:
        """
        Lưu khóa công khai ra file
        
        Args:
            file_path: Đường dẫn file để lưu khóa công khai
        """
        if not self.public_key:
            raise ValueError("Chưa có khóa công khai để lưu")
        
        try:
            # Serialize khóa công khai
            public_pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            # Lưu file
            safe_file_write(file_path, public_pem)
            logger.info(f"Đã lưu khóa công khai vào {file_path}")
            
        except Exception as e:
            logger.error(f"Lỗi khi lưu khóa công khai: {str(e)}")
            raise IOError(f"Không thể lưu khóa công khai: {str(e)}")
    
    def load_private_key(self, file_path: str, password: Optional[str] = None) -> rsa.RSAPrivateKey:
        """
        Tải khóa riêng từ file
        
        Args:
            file_path: Đường dẫn file chứa khóa riêng
            password: Mật khẩu để giải mã khóa riêng (nếu có)
            
        Returns:
            RSA private key object
        """
        try:
            # Đọc file khóa
            private_pem = safe_file_read(file_path)
            
            # Parse khóa riêng
            password_bytes = password.encode('utf-8') if password else None
            private_key = serialization.load_pem_private_key(
                private_pem,
                password=password_bytes
            )
            
            if not isinstance(private_key, rsa.RSAPrivateKey):
                raise ValueError("File không chứa khóa RSA hợp lệ")
            
            self.private_key = private_key
            self.public_key = private_key.public_key()
            
            logger.info(f"Đã tải khóa riêng từ {file_path}")
            return private_key
            
        except ValueError as e:
            if "Bad decrypt" in str(e) or "could not deserialize" in str(e):
                raise ValueError("Mật khẩu không đúng hoặc file khóa bị lỗi")
            raise e
        except Exception as e:
            logger.error(f"Lỗi khi tải khóa riêng: {str(e)}")
            raise IOError(f"Không thể tải khóa riêng: {str(e)}")
    
    def load_public_key(self, file_path: str) -> rsa.RSAPublicKey:
        """
        Tải khóa công khai từ file
        
        Args:
            file_path: Đường dẫn file chứa khóa công khai
            
        Returns:
            RSA public key object
        """
        try:
            # Đọc file khóa
            public_pem = safe_file_read(file_path)
            
            # Parse khóa công khai
            public_key = serialization.load_pem_public_key(public_pem)
            
            if not isinstance(public_key, rsa.RSAPublicKey):
                raise ValueError("File không chứa khóa RSA công khai hợp lệ")
            
            self.public_key = public_key
            
            logger.info(f"Đã tải khóa công khai từ {file_path}")
            return public_key
            
        except Exception as e:
            logger.error(f"Lỗi khi tải khóa công khai: {str(e)}")
            raise IOError(f"Không thể tải khóa công khai: {str(e)}")