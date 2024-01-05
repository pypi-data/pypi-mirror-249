from setuptools import setup, find_packages

setup(
    name='import-for-gcp',
    version='0.1.21',
    author='Caleb Hopkins',
    author_email='caleb.hopkins@method.com',
    description='Use to import classes from .py files saved on google cloud storage',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=[
        'google-cloud-storage>=2.14.0'
    ]
)