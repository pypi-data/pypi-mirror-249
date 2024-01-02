from setuptools import find_packages, setup
import semantic_version

# v = semantic_version.Version('0.4.3')


setup(
    name='pyttrading',
    packages=find_packages(),
    version='0.4.3',
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