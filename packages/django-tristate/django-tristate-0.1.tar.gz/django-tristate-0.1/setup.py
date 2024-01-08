from setuptools import setup, find_packages

setup(
    name='django-tristate',  # PyPI package name
    version='0.1',
    packages=['tri'],
    include_package_data=True,
    description='A Django module providing a tri-state field',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chrysochos/django-tristate',
    author='Ioannis Chrysochos',
    author_email='ioannis.chrysochos@cytanet.com.cy',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        ],
)