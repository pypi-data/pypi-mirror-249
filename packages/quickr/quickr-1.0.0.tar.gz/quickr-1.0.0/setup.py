from setuptools import setup, find_packages

setup(
    name="quickr",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["colorama", "questionary"],
    entry_points={
        "console_scripts": [
            "quickr=quickr.main:main",
        ],
    },
)
