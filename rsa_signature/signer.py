"""
Chức năng ký file bằng RSA-PSS
"""

import hashlib
from pathlib import Path
from typing import Union, Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

from .utils import setup_logging, hash_file, safe_file_write, encode_base64
from .key_manager import RSAKeyManager

logger = setup_logging()

class RSASigner:
    """Ký file bằng RSA-PSS"""
    
    def __init__(self, key_manager: Optional[RSAKeyManager] = None):
        """
        Khởi tạo RSA Signer
        
        Args:
            key_manager: RSA Key Manager (tùy chọn)
        """
        self.key_manager = key_manager or RSAKeyManager()
    
    def sign_file(self, file_path: Union[str, Path], 
                  private_key_path: str, 
                  password: Optional[str] = None,
                  output_format: str = 'binary') -> bytes:
        """
        Ký file bằng RSA-PSS
        
        Args:
            file_path: Đường dẫn file cần ký
            private_key_path: Đường dẫn khóa riêng
            password: Mật khẩu khóa riêng (nếu có)
            output_format: Định dạng output ('binary' hoặc 'base64')
            
        Returns:
            Chữ ký dưới dạng bytes
        """
        try:
            logger.info(f"Đang ký file: {file_path}")
            
            # Tải khóa riêng
            private_key = self.key_manager.load_private_key(private_key_path, password)
            
            # Hash file bằng SHA-256
            file_hash = hash_file(file_path)
            logger.info("Đã hash file bằng SHA-256")
            
            # Ký hash bằng RSA-PSS
            signature = private_key.sign(
                file_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            logger.info("Đã ký file thành công")
            return signature
            
        except Exception as e:
            logger.error(f"Lỗi khi ký file: {str(e)}")
            raise RuntimeError(f"Không thể ký file: {str(e)}")
    
    def save_signature(self, signature: bytes, 
                      output_path: Union[str, Path],
                      format_type: str = 'binary') -> None:
        """
        Lưu chữ ký ra file
        
        Args:
            signature: Chữ ký
            output_path: Đường dẫn file output
            format_type: Định dạng ('binary' cho .sig, 'base64' cho .b64)
        """
        try:
            if format_type == 'base64':
                # Lưu dưới dạng base64
                signature_b64 = encode_base64(signature)
                safe_file_write(output_path, signature_b64, 'w')

            else:
                # Lưu dưới dạng binary
                safe_file_write(output_path, signature)
            
            logger.info(f"Đã lưu chữ ký vào {output_path}")
            
        except Exception as e:
            logger.error(f"Lỗi khi lưu chữ ký: {str(e)}")
            raise IOError(f"Không thể lưu chữ ký: {str(e)}")
    
    def sign_and_save(self, file_path: Union[str, Path],
                     private_key_path: str,
                     signature_path: Optional[Union[str, Path]] = None,
                     password: Optional[str] = None,
                     format_type: str = 'binary') -> str:
        """
        Ký file và lưu chữ ký
        
        Args:
            file_path: Đường dẫn file cần ký
            private_key_path: Đường dẫn khóa riêng
            signature_path: Đường dẫn lưu chữ ký (tự động nếu None)
            password: Mật khẩu khóa riêng
            format_type: Định dạng chữ ký ('binary' hoặc 'base64')
            
        Returns:
            Đường dẫn file chữ ký đã lưu
        """
        try:
            # Ký file
            signature = self.sign_file(file_path, private_key_path, password)
            
            # Tự động tạo tên file chữ ký nếu không có
            if signature_path is None:
                file_path = Path(file_path)
                if format_type == 'base64':
                    signature_path = file_path.with_suffix(file_path.suffix + '.b64')
                else:
                    signature_path = file_path.with_suffix(file_path.suffix + '.sig')
            
            # Lưu chữ ký
            self.save_signature(signature, signature_path, format_type)
            
            return str(signature_path)
            
        except Exception as e:
            logger.error(f"Lỗi trong quá trình ký và lưu: {str(e)}")
            raise RuntimeError(f"Không thể ký và lưu file: {str(e)}")