from setuptools import setup, find_packages

setup(
    name="dynamic_valuation",
    version="1.16",
    author="Eric Larson",
    author_email="ericl3@illinois.edu",
    description="Find present value of a benefit stream subject to dynamics",
    packages=['dynamic_valuation'],
    install_requires=["numpy","matplotlib","scipy"]
)
