from setuptools import setup, find_packages

setup(
    name="databrickslib",
    version="0.0.1",
    author="Vinit",
    author_email="",
    description="Databricks library",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11"
    ],
    python_requires='>=3.11',
    install_requires=["pyspark==3.5.0", "Pyyaml==6.0.1"],
    tests_require=['pytest'],
    entry_points={"console_scripts": []}
)