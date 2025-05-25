import pytest
import tempfile
from pathlib import Path
from rsa_signature.key_manager import RSAKeyManager
from rsa_signature.signer import RSASigner
from rsa_signature.verifier import RSAVerifier

class TestSignerVerifier:
    def setup_method(self):
        """Thiết lập cho mỗi test"""
        self.temp_dir = tempfile.mkdtemp()
        self.key_manager = RSAKeyManager()
        self.key_manager.generate_keypair()

        # Tạo file test
        self.test_file = Path(self.temp_dir) / "test.txt"
        self.test_file.write_text("Hello, this is a test file for RSA signature!")

        # Lưu khóa
        self.private_key_path = Path(self.temp_dir) / "private.pem"
        self.public_key_path = Path(self.temp_dir) / "public.pem"

        self.key_manager.save_private_key(str(self.private_key_path))
        self.key_manager.save_public_key(str(self.public_key_path))

    def test_sign_and_verify_success(self):
        """Test ký và xác minh thành công"""
        signer = RSASigner()
        verifier = RSAVerifier()

        signature_path = signer.sign_and_save(
            str(self.test_file),
            str(self.private_key_path),
            format_type='binary'
        )

        is_valid = verifier.verify_file(
            str(self.test_file),
            signature_path,
            str(self.public_key_path)
        )

        assert is_valid == True

    def test_sign_base64_format(self):
        """Test ký với định dạng base64"""
        signer = RSASigner()
        verifier = RSAVerifier()

        signature_path = signer.sign_and_save(
            str(self.test_file),
            str(self.private_key_path),
            format_type='base64'
        )

        assert signature_path.endswith('.b64')

        is_valid = verifier.verify_file(
            str(self.test_file),
            signature_path,
            str(self.public_key_path)
        )

        assert is_valid == True

    def test_verify_tampered_file(self):
        """Test xác minh file bị thay đổi"""
        signer = RSASigner()
        verifier = RSAVerifier()

        signature_path = signer.sign_and_save(
            str(self.test_file),
            str(self.private_key_path)
        )

        self.test_file.write_text("This content has been tampered!")

        is_valid = verifier.verify_file(
            str(self.test_file),
            signature_path,
            str(self.public_key_path)
        )

        assert is_valid == False

    def test_sign_with_password_protected_key(self):
        """Test ký với khóa có mật khẩu"""
        password = "testpass123"

        password_private_key = Path(self.temp_dir) / "private_pwd.pem"
        self.key_manager.save_private_key(str(password_private_key), password)

        signer = RSASigner()
        verifier = RSAVerifier()

        signature_path = signer.sign_and_save(
            str(self.test_file),
            str(password_private_key),
            password=password
        )

        is_valid = verifier.verify_file(
            str(self.test_file),
            signature_path,
            str(self.public_key_path)
        )

        assert is_valid == True
