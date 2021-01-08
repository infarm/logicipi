from setuptools import find_packages, setup


def get_long_description() -> str:
    with open("README.md", "r", encoding="utf-8") as readme:
        return readme.read()


setup(
    name="logicipi",  # Replace with your own username
    version="0.0.1",
    author="Infarm Software developers",
    author_email="fsd@infarm.com",
    description="A logger for GCP",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/infarm/logicipi",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=["structlog==^20.1.0", "google-cloud-logging==^1.15.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
