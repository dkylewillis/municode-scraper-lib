"""Setup script for municode-lib package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="municode-lib",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for scraping and parsing municipal code data from Municode websites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/municode-lib",
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
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.0.0",
        "beautifulsoup4>=4.9.0",
        "webdriver-manager>=3.8.0",
        "htmlmin>=0.1.12",
        "lxml>=4.6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "municode-scraper=municode_lib.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
