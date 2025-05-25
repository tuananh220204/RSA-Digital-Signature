import pytest
import tempfile
import os
from pathlib import Path
from rsa_signature.key_manager import RSAKeyManager

class TestRSAKeyManager:
    def test_generate_keypair_2048(self):
        key_manager = RSAKeyManager(2048)
        private_key, public_key = key_manager.generate_keypair()
        
        assert private_key is not None
        assert public_key is not None
        assert private_key.key_size == 2048
    
    def test_generate_keypair_3072(self):
        key_manager = RSAKeyManager(3072)
        private_key, public_key = key_manager.generate_keypair()
        
        assert private_key is not None
        assert public_key is not None
        assert private_key.key_size == 3072
    
    def test_invalid_key_size(self):
        with pytest.raises(ValueError):
            RSAKeyManager(1024)
    
    def test_save_and_load_private_key_without_password(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            key_manager = RSAKeyManager()
            key_manager.generate_keypair()
            
            private_key_path = Path(temp_dir) / "private.pem"
            
            # Lưu khóa
            key_manager.save_private_key(str(private_key_path))
            
            # Tải khóa
            new_key_manager = RSAKeyManager()
            loaded_key = new_key_manager.load_private_key(str(private_key_path))
            
            assert loaded_key.key_size == key_manager.private_key.key_size
    
    def test_save_and_load_private_key_with_password(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            key_manager = RSAKeyManager()
            key_manager.generate_keypair()
            
            private_key_path = Path(temp_dir) / "private.pem"
            password = "test123"
            
            # Lưu khóa với mật khẩu
            key_manager.save_private_key(str(private_key_path), password)
            
            # Tải khóa với mật khẩu
            new_key_manager = RSAKeyManager()
            loaded_key = new_key_manager.load_private_key(str(private_key_path), password)
            
            assert loaded_key.key_size == key_manager.private_key.key_size
    
    def test_load_private_key_wrong_password(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            key_manager = RSAKeyManager()
            key_manager.generate_keypair()
            
            private_key_path = Path(temp_dir) / "private.pem"
            password = "test123"
            wrong_password = "wrong"
            
            # Lưu khóa với mật khẩu
            key_manager.save_private_key(str(private_key_path), password)
            
            # Thử tải với mật khẩu sai
            new_key_manager = RSAKeyManager()
            with pytest.raises(ValueError):
                new_key_manager.load_private_key(str(private_key_path), wrong_password)

if __name__ == "__main__":
    pytest.main([__file__])