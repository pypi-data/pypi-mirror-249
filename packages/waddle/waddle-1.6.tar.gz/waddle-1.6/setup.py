from setuptools import setup, find_packages

version = '1.6'

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='waddle',
    version=version,
    description="A pathy wrapper around aws parameter store",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'License :: OSI Approved :: BSD License',
    ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='aws python parameter-store kms',
    author='Preetam Shingavi',
    author_email='p.shingavi@yahoo.com',
    url='https://github.com/angry-penguins/waddle',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'pyyaml',
        'boto3>=1.9.0',
        'click>=7.0',
        'murmuration>=1.3',
        'ruamel.yaml>=0.15.87',
        'halo>=0.0.26',
    ],
    entry_points={
        'console_scripts': [
            'waddle=waddle.cli:main',
        ]
    })
