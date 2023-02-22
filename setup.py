from setuptools import setup

setup(
    name="cubeserver",
    version="0.0.0",
    packages=["cubeserver"],
    include_package_data=True,
    install_requires=["flask", "boto3"]
)
