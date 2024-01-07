# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

setup(
    name="dynamic_valuation",
    version="1.5",
    author="Eric Larson",
    author_email="ericl3@illinois.edu",
    description="Find present value of a benefit stream subject to dynamics",
    packages=find_packages(),
    install_requires=["numpy","matplotlib","scipy.optimize.minimize","scipy.interpolate.interp1d",
                      "scipy.optimize.root_scalar"]
)
