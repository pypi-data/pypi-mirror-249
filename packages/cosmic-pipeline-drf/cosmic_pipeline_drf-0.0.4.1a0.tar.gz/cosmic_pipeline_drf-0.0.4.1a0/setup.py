from setuptools import setup
from setuptools import find_packages

def get_requirements():
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
    return requirements


setup(
    name="cosmic_pipeline_drf",
    fullname="CosmicPipeline DRF",
    version="v0.0.4.1-alpha",
    packages=find_packages()+find_packages(where="cosmic_pipeline_drf"),
    include_package_data = True,
    url="",
    license="",
    author="Digital Intelligence GmbH",
    author_email="andrey.bulezyuk@digital-intelligence.eu",
    description="State, Transition, Rule and Pre- & Posthook Framework for Complex Business & Logical Processes.",
    install_requires=get_requirements(),
)
