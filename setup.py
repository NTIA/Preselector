import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='preselector-its',
    version='0.0.1',
    author='NTIA/ITS',
    description='Enables interaction with a web relay based preselector',
    python_requires =">=3.9"

packages=find_packages(include=
                       )
)

