from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rsa-signature-system",
    version="1.0.0",
    author="RSA Signature System",
    author_email="admin@example.com",
    description="Hệ thống chữ ký số RSA hoàn chỉnh với Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rsa-signature-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "cryptography>=41.0.0",
        "click>=8.1.0",
        "flask>=2.3.0",
        "werkzeug>=2.3.0",
    ],
    entry_points={
        "console_scripts": [
            "rsa-signature=rsa_signature.cli:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "rsa_signature": ["templates/*.html"],
    },
)