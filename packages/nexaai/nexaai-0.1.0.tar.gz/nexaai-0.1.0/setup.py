from setuptools import find_packages, setup

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nexaai',  # the name of your library
    packages=find_packages(include=['nexaai']),  # directory where your Python code is
    version='0.1.0',
    description='Nexa AI library for super ai agent',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nexa AI team',
    license='MIT',  # or your choice of license
    install_requires=['numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=4.4.1'],  # specify a minimum version instead
    test_suite='tests',
)
