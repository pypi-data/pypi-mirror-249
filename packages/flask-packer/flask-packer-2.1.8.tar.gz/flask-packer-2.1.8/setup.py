from setuptools import setup, find_packages

from version import __version__


def find_requirements() -> list[str]:
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    author="H.P. Mertens",
    author_email="stnmertens@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Build Tools",
    ],
    description="A Flask extension to bundle and compress CSS and JS files.",
    install_requires=find_requirements(),
    keywords=["flask", "packer", "static", "compress", "bundle", "minify", "combine"],
    license="GNU General Public License v3.0",
    name="flask-packer",
    packages=find_packages(),
    python_requires=">=3.11",
    url="https://github.com/stan5079/flask-packer",
    version=__version__,
)
