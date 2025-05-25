"""
Chức năng timestamp cho chữ ký số (tùy chọn mở rộng)
"""

import time
import json
from datetime import datetime
from typing import Dict, Any

from .utils import setup_logging

logger = setup_logging()

class TimestampService:
    """Dịch vụ timestamp cho chữ ký số"""
    
    @staticmethod
    def create_timestamp() -> Dict[str, Any]:
        """
        Tạo timestamp cho chữ ký
        
        Returns:
            Dictionary chứa thông tin timestamp
        """
        now = datetime.now()
        return {
            'timestamp': now.isoformat(),
            'unix_time': int(time.time()),
            'timezone': str(now.tzinfo),
            'created_by': 'RSA Signature System'
        }
    
    @staticmethod
    def save_timestamp(timestamp_data: Dict[str, Any], file_path: str) -> None:
        """
        Lưu timestamp ra file JSON
        
        Args:
            timestamp_data: Dữ liệu timestamp
            file_path: Đường dẫn file để lưu
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(timestamp_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Đã lưu timestamp vào {file_path}")
        except Exception as e:
            logger.error(f"Lỗi khi lưu timestamp: {str(e)}")
            raise IOError(f"Không thể lưu timestamp: {str(e)}")
    
    @staticmethod
    def load_timestamp(file_path: str) -> Dict[str, Any]:
        """
        Tải timestamp từ file JSON
        
        Args:
            file_path: Đường dẫn file timestamp
            
        Returns:
            Dictionary chứa thông tin timestamp
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Lỗi khi tải timestamp: {str(e)}")
            raise IOError(f"Không thể tải timestamp: {str(e)}")
