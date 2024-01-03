from setuptools import setup
from setuptools import find_packages

def get_requirements():
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
    return requirements


setup(
    name="cosmic_pipeline",
    fullname="CosmicPipeline",
    version="v0.0.6",
    packages=find_packages() + find_packages(where="cosmic_pipeline_drf"),
    include_package_data = True,
    url="",
    license="",
    python_requires=">=3.6",
    author="Digital Intelligence GmbH",
    author_email="",
    description="",
    install_requires=get_requirements(),
)
