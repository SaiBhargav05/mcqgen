from setuptools import find_packages, setup

setup(
    name='macqgenerator',
    version='0.0.1',
    author='Sai Bhargav',
    author_email='saibhargav052000@gmail.com',
    install_requires=[
        "openai",
        "langchain==0.1.14",
        "langchain-community==0.0.38",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],
    packages=find_packages()
)
