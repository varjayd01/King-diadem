from setuptools import setup, find_packages

setup(
    name="kingdiadem",
    version="0.1.0",
    description="KING DIADEM Survival Decision System",
    author="Nithikorn Bunsrang",
    packages=find_packages(),
    install_requires=[
        "deep-translator"
    ],
    python_requires=">=3.10",
)
