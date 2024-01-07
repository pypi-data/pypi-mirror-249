# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

setup(
    name="dynamic_valuation",
    version="1.3",
    author="Eric Larson",
    author_email="ericl3@illinois.edu",
    description="Find present value of a benefit stream subject to dynamics",
    packages=find_packages(),
    install_requires=["numpy","pylab","scipy.optimize.minimize","scipy.interpolate.interp1d",
                      "scipy.optimize.root_scalar"]
)
