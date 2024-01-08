from setuptools import setup, find_packages

with open(file='pxapp/README.md', mode='r') as f:
    description = f.read()

setup(
    name='RFPX',
    version='0.0.10',
    description="A helping tool",
    package_dir={"": "pxapp"},
    packages=find_packages(where="pxapp"),
    long_description=description,
    author="rf123",
    license="RFPX Software Subscription Agreement",
    install_requires=["bson >= 0.5.10",
                      "twine>=4.0.2"
                      ],
    python_requires=">=3.9"
)
