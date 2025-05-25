"""
Command Line Interface cho hệ thống chữ ký số RSA
"""

import click
import getpass
from pathlib import Path

from .key_manager import RSAKeyManager
from .signer import RSASigner
from .verifier import RSAVerifier
from .timestamp import TimestampService
from .utils import setup_logging

logger = setup_logging()

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Hệ thống chữ ký số RSA - RSA Digital Signature System"""
    pass

@cli.command()
@click.option('--key-size', default=2048, help='Kích thước khóa (2048 hoặc 3072)')
@click.option('--private-key', required=True, help='Đường dẫn lưu khóa riêng')
@click.option('--public-key', required=True, help='Đường dẫn lưu khóa công khai')
@click.option('--password', is_flag=True, help='Sử dụng mật khẩu để bảo vệ khóa riêng')
def genkey(key_size, private_key, public_key, password):
    """Tạo cặp khóa RSA mới"""
    try:
        click.echo(f"Đang tạo cặp khóa RSA {key_size} bit...")
        
        # Tạo key manager
        key_manager = RSAKeyManager(key_size)
        
        # Tạo cặp khóa
        key_manager.generate_keypair()
        
        # Lấy mật khẩu nếu cần
        key_password = None
        if password:
            key_password = getpass.getpass("Nhập mật khẩu cho khóa riêng: ")
            confirm_password = getpass.getpass("Xác nhận mật khẩu: ")
            if key_password != confirm_password:
                click.echo("Mật khẩu không khớp!", err=True)
                return
        
        # Lưu khóa
        key_manager.save_private_key(private_key, key_password)
        key_manager.save_public_key(public_key)
        
        click.echo(f"✓ Đã tạo và lưu cặp khóa:")
        click.echo(f"  - Khóa riêng: {private_key}")
        click.echo(f"  - Khóa công khai: {public_key}")
        
    except Exception as e:
        click.echo(f"Lỗi: {str(e)}", err=True)

@cli.command()
@click.argument('file_path')
@click.option('--private-key', required=True, help='Đường dẫn khóa riêng')
@click.option('--signature', help='Đường dẫn lưu chữ ký (tự động nếu không có)')
@click.option('--format', 'format_type', default='binary', 
              type=click.Choice(['binary', 'base64']), help='Định dạng chữ ký')
@click.option('--password', is_flag=True, help='Khóa riêng có mật khẩu')
@click.option('--timestamp', is_flag=True, help='Tạo timestamp cho chữ ký')
def sign(file_path, private_key, signature, format_type, password, timestamp):
    """Ký file bằng RSA-PSS"""
    try:
        click.echo(f"Đang ký file: {file_path}")
        
        # Lấy mật khẩu nếu cần
        key_password = None
        if password:
            key_password = getpass.getpass("Nhập mật khẩu khóa riêng: ")
        
        # Tạo signer
        signer = RSASigner()
        
        # Ký và lưu file
        signature_path = signer.sign_and_save(
            file_path, private_key, signature, key_password, format_type
        )
        
        click.echo(f"✓ Đã ký file thành công:")
        click.echo(f"  - File gốc: {file_path}")
        click.echo(f"  - Chữ ký: {signature_path}")
        
        # Tạo timestamp nếu cần
        if timestamp:
            timestamp_data = TimestampService.create_timestamp()
            timestamp_path = Path(signature_path).with_suffix('.timestamp.json')
            TimestampService.save_timestamp(timestamp_data, str(timestamp_path))
            click.echo(f"  - Timestamp: {timestamp_path}")
        
    except Exception as e:
        click.echo(f"Lỗi: {str(e)}", err=True)

@cli.command()
@click.argument('file_path')
@click.argument('signature_path')
@click.option('--public-key', required=True, help='Đường dẫn khóa công khai')
@click.option('--timestamp', help='Đường dẫn file timestamp (tùy chọn)')
def verify(file_path, signature_path, public_key, timestamp):
    """Xác minh chữ ký file"""
    try:
        click.echo(f"Đang xác minh chữ ký cho file: {file_path}")
        
        # Tạo verifier
        verifier = RSAVerifier()
        
        # Xác minh chữ ký
        is_valid = verifier.verify_file(file_path, signature_path, public_key)
        
        if is_valid:
            click.echo("✓ Chữ ký hợp lệ - File chưa bị thay đổi")
            
            # Hiển thị thông tin timestamp nếu có
            if timestamp and Path(timestamp).exists():
                timestamp_data = TimestampService.load_timestamp(timestamp)
                click.echo(f"  - Thời gian ký: {timestamp_data.get('timestamp', 'N/A')}")
            
        else:
            click.echo("✗ Chữ ký không hợp lệ - File có thể đã bị thay đổi", err=True)
        
    except Exception as e:
        click.echo(f"Lỗi: {str(e)}", err=True)

if __name__ == '__main__':
    cli()