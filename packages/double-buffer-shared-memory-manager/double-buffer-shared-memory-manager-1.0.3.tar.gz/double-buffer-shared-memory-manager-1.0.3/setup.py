import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
long_description = open("README.rst").read()

infos = {}
with open(
    os.path.join(here, "double_buffer_shared_memory", "infos.py"),
    mode="r",
    encoding="utf-8",
) as f:
    exec(f.read(), infos)

setup(
    name=infos["NAME"],
    version=infos["VERSION"],
    url=infos["URL"],
    author=infos["AUTHOR_NO_EMAIL"],
    author_email=infos["EMAIL"],
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "main.py", ".vscode"]
    ),
    license=infos["LICENSE"],
    description=infos["DESCRIPTION"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=["colorlog>=6.8.0", "numpy>=1.26.2", "readerwriterlock>=1.0.9"],
    python_requires=">=3.10",  # Specifica la versione di Python richiesta
    include_package_data=True,
    classifiers=[
        # Classificatori che danno informazioni sul tuo pacchetto
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

# python3.10 setup.py sdist bdist_wheel
