"""
Web Application cho hệ thống chữ ký số RSA
"""

import os
import tempfile
from pathlib import Path
from flask import Flask, request, render_template, flash, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from .key_manager import RSAKeyManager
from .signer import RSASigner
from .verifier import RSAVerifier
from .utils import setup_logging

logger = setup_logging()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Cấu hình upload
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'zip', 'py', 'js', 'html', 'css'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    """Đảm bảo thư mục upload tồn tại"""
    Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

@app.route('/generate-keys', methods=['GET', 'POST'])
def generate_keys():
    """Tạo cặp khóa RSA"""
    if request.method == 'POST':
        try:
            key_size = int(request.form.get('key_size', 2048))
            password = request.form.get('password', '').strip()
            
            # Tạo key manager
            key_manager = RSAKeyManager(key_size)
            key_manager.generate_keypair()
            
            # Tạo tên file tạm
            temp_dir = tempfile.mkdtemp()
            private_key_path = Path(temp_dir) / 'private_key.pem'
            public_key_path = Path(temp_dir) / 'public_key.pem'
            
            # Lưu khóa
            key_manager.save_private_key(str(private_key_path), password if password else None)
            key_manager.save_public_key(str(public_key_path))
            
            flash(f'Đã tạo cặp khóa RSA {key_size} bit thành công!', 'success')
            
            return render_template('keys_generated.html', 
                                 private_key_path=str(private_key_path),
                                 public_key_path=str(public_key_path))
            
        except Exception as e:
            flash(f'Lỗi khi tạo cặp khóa: {str(e)}', 'error')
    
    return render_template('generate_keys.html')

@app.route('/sign-file', methods=['GET', 'POST'])
def sign_file():
    """Ký file"""
    if request.method == 'POST':
        try:
            ensure_upload_folder()
            
            # Kiểm tra file upload
            if 'file' not in request.files or 'private_key' not in request.files:
                flash('Vui lòng chọn file và khóa riêng', 'error')
                return redirect(request.url)
            
            file = request.files['file']
            private_key_file = request.files['private_key']
            password = request.form.get('password', '').strip()
            format_type = request.form.get('format', 'binary')
            
            if file.filename == '' or private_key_file.filename == '':
                flash('Vui lòng chọn file hợp lệ', 'error')
                return redirect(request.url)
            
            # Lưu file tạm
            filename = secure_filename(file.filename)
            private_key_filename = secure_filename(private_key_file.filename)
            
            file_path = Path(UPLOAD_FOLDER) / filename
            private_key_path = Path(UPLOAD_FOLDER) / private_key_filename
            
            file.save(str(file_path))
            private_key_file.save(str(private_key_path))
            
            # Ký file
            signer = RSASigner()
            signature_path = signer.sign_and_save(
                str(file_path), 
                str(private_key_path), 
                password=password if password else None,
                format_type=format_type
            )
            
            flash('Đã ký file thành công!', 'success')
            
            return render_template('file_signed.html',
                                 original_file=filename,
                                 signature_file=Path(signature_path).name)
            
        except Exception as e:
            flash(f'Lỗi khi ký file: {str(e)}', 'error')
    
    return render_template('sign_file.html')

@app.route('/verify-signature', methods=['GET', 'POST'])
def verify_signature():
    """Xác minh chữ ký"""
    if request.method == 'POST':
        try:
            ensure_upload_folder()
            
            # Kiểm tra file upload
            required_files = ['file', 'signature', 'public_key']
            for field in required_files:
                if field not in request.files:
                    flash(f'Vui lòng chọn {field}', 'error')
                    return redirect(request.url)
            
            file = request.files['file']
            signature_file = request.files['signature']
            public_key_file = request.files['public_key']
            
            if any(f.filename == '' for f in [file, signature_file, public_key_file]):
                flash('Vui lòng chọn tất cả các file cần thiết', 'error')
                return redirect(request.url)
            
            # Lưu file tạm
            filename = secure_filename(file.filename)
            signature_filename = secure_filename(signature_file.filename)
            public_key_filename = secure_filename(public_key_file.filename)
            
            file_path = Path(UPLOAD_FOLDER) / filename
            signature_path = Path(UPLOAD_FOLDER) / signature_filename
            public_key_path = Path(UPLOAD_FOLDER) / public_key_filename
            
            file.save(str(file_path))
            signature_file.save(str(signature_path))
            public_key_file.save(str(public_key_path))
            
            # Xác minh chữ ký
            verifier = RSAVerifier()
            is_valid = verifier.verify_file(
                str(file_path),
                str(signature_path),
                str(public_key_path)
            )
            
            result = {
                'valid': is_valid,
                'message': 'Chữ ký hợp lệ - File chưa bị thay đổi' if is_valid 
                          else 'Chữ ký không hợp lệ - File có thể đã bị thay đổi',
                'file': filename
            }
            
            return render_template('verification_result.html', result=result)
            
        except Exception as e:
            flash(f'Lỗi khi xác minh chữ ký: {str(e)}', 'error')
    
    return render_template('verify_signature.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download file"""
    try:
        file_path = Path(UPLOAD_FOLDER) / filename
        if file_path.exists():
            return send_file(str(file_path), as_attachment=True)
        else:
            flash('File không tồn tại', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Lỗi khi download file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    flash('File quá lớn. Kích thước tối đa là 16MB', 'error')
    return redirect(request.url), 413

if __name__ == '__main__':
    ensure_upload_folder()
    # Chỉ chạy HTTP trong development, production nên dùng HTTPS
    app.run(debug=True, host='0.0.0.0', port=5000)