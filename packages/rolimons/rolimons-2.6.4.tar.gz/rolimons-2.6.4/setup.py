from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="rolimons",
    version="2.6.4",
    author="walker",
    description="Rolimons API Wrapper",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=['rolimons'],
    url="https://github.com/wa1ker38552/rolimons.py",
    install_requires=["requests", "bs4"],
    python_requires=">=3.7",
    py_modules=["rolimons"]
)