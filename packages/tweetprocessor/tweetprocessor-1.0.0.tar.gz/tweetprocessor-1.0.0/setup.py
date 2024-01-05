from setuptools import setup, find_packages


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()


setup(
    name="tweetprocessor",
    version="1.0.0",
    packages=find_packages(include=['text_processing', 'text_processing.*']),
    url="",
    author="Jhonatan Camasca",
    description="This is my text processor that will process text using 10 NLP processing tehcniques for the ML SPECIALIZATION",
    long_description=read_file(file_name="README.md"),
    long_description_content_type="text/markdown",
    python_requires="==3.12",
    install_requires=[
        'pandas==2.1.4',
        'pytest==6.2.4',
        'nltk==3.6.5',
        'setuptools==69.0.2',
        'jupyter==1.0.0'
    ]
)
