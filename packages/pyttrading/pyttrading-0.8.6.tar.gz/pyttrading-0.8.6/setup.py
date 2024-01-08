from setuptools import find_packages, setup

setup(
    name='pyttrading',
    packages=find_packages(),
    version='0.8.6',
    description='Trading Library',
    author='Cecilio Cannavacciuolo Diaz',
    install_requires=[],
    setup_requires=[
        'pytest-runner',
        'stock-dataframe==0.1.0',
        'mlflow==2.9.2',
        'backtesting==0.3.3'
    ],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    python_requires='>=3.6'
)

# pip uninstall -y pyttrading && python setup.py sdist && twine upload dist/* 