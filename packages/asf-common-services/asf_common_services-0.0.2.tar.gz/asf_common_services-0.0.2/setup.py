from setuptools import setup, find_packages

setup(
    name='asf_common_services',
    version='0.0.2',
    packages=find_packages(),
    package_data={'asf_common_services': ['*.pyi']},  # Include .pyi files
    include_package_data=True,
    install_requires=[
        'protobuf',  # Add other dependencies here
        # Other dependencies...
    ],
)
