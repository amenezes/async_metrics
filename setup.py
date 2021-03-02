from collections import OrderedDict

import setuptools

from async_metrics import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="async_metrics",
    version=f"{__version__}",
    author="alexandre menezes",
    author_email="alexandre.fmenezes@gmail.com",
    description="async_metrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    url="https://github.com/amenezes/async_metrics",
    packages=setuptools.find_packages(include=["async_metrics", "async_metrics.*"]),
    python_requires=">=3.8.*",
    project_urls=OrderedDict(
        (
            ("Documentation", "https://async_metrics.amenezes.net"),
            ("Code", "https://github.com/amenezes/async_metrics"),
            ("Issue tracker", "https://github.com/amenezes/async_metrics/issues"),
        )
    ),
    install_requires=["psutil>=5.7.3"],
    tests_require=[
        "isort",
        "black",
        "portray",
        "flake8",
        "pytest",
        "pytest-asyncio",
        "pytest-cov",
        "codecov",
        "coverage",
        "mypy",
        "tox",
        "tox-asdf",
    ],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: AsyncIO",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries",
    ],
)
