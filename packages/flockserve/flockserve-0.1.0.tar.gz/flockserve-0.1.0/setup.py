#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ "skypilot[all]", "opentelemetry-api", "opentelemetry-instrumentation", "opentelemetry-sdk"]

test_requirements = ['pytest>=3', ]

setup(
    author="Antti Puurula, Anil Gurbuz",
    author_email='antti.puurula@yahoo.com, anl_grbz@outlook.com',
    python_requires='>=3.7, <=3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="Open-source Sky Computing Inference Endpoint",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='flockserve',
    name='flockserve',
    packages=find_packages(include=['flockserve', 'flockserve.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jdooodle/flockserve',
    version='0.1.0',
    zip_safe=False,
)
