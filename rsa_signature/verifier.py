"""
Chức năng xác minh chữ ký RSA-PSS
"""

from pathlib import Path
from typing import Union, Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

from .utils import setup_logging, hash_file, safe_file_read, decode_base64
from .key_manager import RSAKeyManager

logger = setup_logging()

class RSAVerifier:
    """Xác minh chữ ký RSA-PSS"""
    
    def __init__(self, key_manager: Optional[RSAKeyManager] = None):
        """
        Khởi tạo RSA Verifier
        
        Args:
            key_manager: RSA Key Manager (tùy chọn)
        """
        self.key_manager = key_manager or RSAKeyManager()
    
    def load_signature(self, signature_path: Union[str, Path]) -> bytes:
        """
        Tải chữ ký từ file
        
        Args:
            signature_path: Đường dẫn file chữ ký
            
        Returns:
            Chữ ký dưới dạng bytes
        """
        try:
            signature_path = Path(signature_path)
            
            if signature_path.suffix.lower() == '.b64':
                # Đọc và decode base64
                signature_b64 = safe_file_read(signature_path).decode('utf-8')
                return decode_base64(signature_b64)
            else:
                # Đọc binary
                return safe_file_read(signature_path)
                
        except Exception as e:
            logger.error(f"Lỗi khi tải chữ ký: {str(e)}")
            raise IOError(f"Không thể tải chữ ký: {str(e)}")
    
    def verify_signature(self, file_path: Union[str, Path],
                        signature: bytes,
                        public_key_path: str) -> bool:
        """
        Xác minh chữ ký file
        
        Args:
            file_path: Đường dẫn file gốc
            signature: Chữ ký
            public_key_path: Đường dẫn khóa công khai
            
        Returns:
            True nếu chữ ký hợp lệ, False nếu không
        """
        try:
            logger.info(f"Đang xác minh chữ ký cho file: {file_path}")
            
            # Tải khóa công khai
            public_key = self.key_manager.load_public_key(public_key_path)
            
            # Hash file
            file_hash = hash_file(file_path)
            
            # Xác minh chữ ký bằng RSA-PSS
            public_key.verify(
                signature,
                file_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            logger.info("Chữ ký hợp lệ")
            return True
            
        except InvalidSignature:
            logger.warning("Chữ ký không hợp lệ")
            return False
        except Exception as e:
            logger.error(f"Lỗi khi xác minh chữ ký: {str(e)}")
            raise RuntimeError(f"Không thể xác minh chữ ký: {str(e)}")
    
    def verify_file(self, file_path: Union[str, Path],
                   signature_path: Union[str, Path],
                   public_key_path: str) -> bool:
        """
        Xác minh file với chữ ký từ file
        
        Args:
            file_path: Đường dẫn file gốc
            signature_path: Đường dẫn file chữ ký
            public_key_path: Đường dẫn khóa công khai
            
        Returns:
            True nếu chữ ký hợp lệ, False nếu không
        """
        try:
            # Tải chữ ký
            signature = self.load_signature(signature_path)
            
            # Xác minh
            return self.verify_signature(file_path, signature, public_key_path)
            
        except Exception as e:
            logger.error(f"Lỗi trong quá trình xác minh file: {str(e)}")
            raise RuntimeError(f"Không thể xác minh file: {str(e)}")