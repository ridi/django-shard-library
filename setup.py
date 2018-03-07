from setuptools import setup, find_packages

version = '0.0.1'

with open('requirements/base.txt') as f:
    install_requires = [line for line in f if line and not line.startswith('-')]


setup(
    name='django-shard-library',
    version=version,
    url='https://github.com/ridi/djang-shard-library',
    license='BSD',
    description='Django Shard Library',
    keywords=['django', 'shard', 'ridi', 'ridibooks'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: BSD License',
        'Framework :: Django :: 2.0',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=('tests', 'docs',)),
    install_requires=install_requires,
    include_package_data=True,
)
