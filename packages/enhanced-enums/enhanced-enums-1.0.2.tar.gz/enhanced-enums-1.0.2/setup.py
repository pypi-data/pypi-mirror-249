import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


long_description = open("README.rst").read()

infos = {}
with open(
    os.path.join(here, "enhanced_enums", "infos.py"), mode="r", encoding="utf-8"
) as f:
    exec(f.read(), infos)

setup(
    name="enhanced-enums",
    version=infos["VERSION"],
    url=infos["URL"],
    author=infos["AUTHOR_NO_EMAIL"],
    author_email=infos["EMAIL"],
    maintainer=infos["MAINTAINER"],
    maintainer_email=infos["EMAIL"],
    keywords=infos["KEYWORDS"],
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "main.py", ".vscode"]
    ),
    license="MIT",
    license_files=["LICENSE"],
    description="A package that provides enhanced enums for Python.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=[],
    python_requires=">=3.10",  # Specifica la versione di Python richiesta
    include_package_data=True,
    classifiers=[
        # Classificatori che danno informazioni sul tuo pacchetto
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    project_urls={  # Optional
        "Bug Reports": infos["ISSUES_URL"],
        "Source": infos["URL"],
    },
)

# python3.10 setup.py sdist bdist_wheel
