from setuptools import setup, find_packages

setup(
    name='cv_sample_package_01',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'your_script_name = your_package.module:main',
        ],
    },
)
