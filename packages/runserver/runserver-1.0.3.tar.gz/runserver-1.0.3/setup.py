from setuptools import setup, find_packages

setup(
    name='runserver',
    version='1.0.3',
    packages=['FlaskWebProject1'],
    include_package_data=True,
    install_requires=[
        'Flask',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'runserver=FlaskWebProject1.app:run',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)
