from setuptools import setup, find_packages

setup(
    name="files",
    version="0.11",
    description="A command-line file explorer with advanced features",
    author="Your Name",  # Replace with your name
    author_email="your.email@example.com",  # Replace with your email
    packages=find_packages(),
    include_package_data=True,  # Includes config.ini
    package_data={
        "files": ["config.ini"],
    },
    install_requires=[],  # No external dependencies needed
    entry_points={
        "console_scripts": [
            "files = files.main:run",
        ],
    },
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust license as needed
        "Operating System :: OS Independent",
    ],
)