from setuptools import setup, find_packages

setup(
    name="iscasmodel",
    version="0.16",
    packages=find_packages(),
    install_requires=[
        'requests',
        'torch==2.0.0'  # 如果你用requests替代urllib，需要添加这个依赖
    ],
    author="ls",
    author_email="your.email@example.com",
    description="A library to send accuracy data",
    long_description="A longer description of your library",
    url="https://github.com/yourusername/mylibrary",
)
