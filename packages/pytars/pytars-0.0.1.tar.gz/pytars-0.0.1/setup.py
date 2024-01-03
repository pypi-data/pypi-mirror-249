from setuptools import find_packages, setup

setup(
    name="pytars",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
        "tqdm",
        "requests",
        "pillow",
    ],
    author="hokiespurs",
    description="Python Tools for Applied Remote Sensing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
