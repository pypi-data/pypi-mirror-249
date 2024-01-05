from setuptools import setup, find_packages

setup(
    name='runserver',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'runserver=app:run',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)
