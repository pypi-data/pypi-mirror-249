from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
readme = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="dtype",
    version="0.0.0",
    description="dtype.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/dtype/dtype",
    author="dtype",
    #author_email="oqibz@example.com",
    license="MIT",
    classifiers=[

    ],
    packages=find_packages(exclude=["dtype.tests", "dtype.tests.*", "tests"]),
    include_package_data=True,
    install_requires=["typing"],
    python_requires=">=3.7",
)