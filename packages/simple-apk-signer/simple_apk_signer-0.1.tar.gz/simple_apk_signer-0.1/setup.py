from setuptools import setup, find_packages

setup(
    name='simple_apk_signer',
    version='0.1',
    packages=find_packages(),
    description='A simple library to sign APKs',
    include_package_data=True,  # This will include non-code files specified in MANIFEST.in
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
