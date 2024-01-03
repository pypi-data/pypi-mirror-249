import io
from distutils.core import setup

import setuptools

with io.open("README.md", mode="r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="fastmq",
    version="0.0.1",
    author="Denghui Zhao",
    author_email="zdh990831@163.com",
    description="Use FastMQ, Do MQ development just like FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/bob-zhao/FastMQ",
    install_requires=[],
    tests_require=["pytest", "adal"],
    test_suite="tests",
    license="Apache",
    keywords="git",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
    ]
)