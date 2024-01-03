import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.md')
with open(readme_path, "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name = "testsmodules",
    version = "0.0.1",
    author = "Tan H. Nguyen, Thien Q. Tran, Pham Ha Hai, Nguyen Huy Tan",
    author_email = "huynhtannguyen.my@uopeople.edu",
    packages = find_packages(),
    long_description = long_description,
    description = "Talbots is a Python library for understanding, analyzing, and evaluating the content of text-generating systems through research papers published in scientific journals, with features such as downloading Bibtex information of research papers, downloading PDF files of research papers, data conversion, and supporting the detection of tortured phrases. In addition, it can assist you in developing and publishing your projects.",
    long_description_content_type = "text/markdown",
    url= "https://bitbucket.org/tanhuynhng/talbots",
    license = "GNU General Public License v3 or later (GPLv3+)",
    classifiers =[
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires =[
        "beautifulsoup4==4.11.2",
        "bs4==0.0.1",
        "certifi==2022.12.7",
        "charset-normalizer==3.1.0",
        "et-xmlfile==1.1.0",
        "idna==3.4",
        "openpyxl==3.1.1",
        "PyPDF2==3.0.1",
        "requests==2.28.2",
        "soupsieve==2.4",
        "typing_extensions==4.5.0",
        "urllib3==1.26.14"
    ],
    python_requires = ">=3.0"
)