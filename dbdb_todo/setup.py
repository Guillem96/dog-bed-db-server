import io

from setuptools import find_packages, setup

setup(
    name='dbdb_todo',
    version='1.0.0',
    license='GPL',
    maintainer='Guillem96',
    maintainer_email='guillem.orellana@gmail.com',
    description='Example app to demonstrate DBDB utility',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
        ],
    },
)
