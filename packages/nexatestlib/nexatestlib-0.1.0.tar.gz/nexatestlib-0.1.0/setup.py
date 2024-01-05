from setuptools import find_packages, setup

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nexatestlib',  # the name of your library
    packages=find_packages(include=['nexatestlib']),  # directory where your Python code is
    version='0.1.0',
    description='NexaTestLib',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alex',
    license='MIT',  # or your choice of license
    install_requires=['numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=4.4.1'],  # specify a minimum version instead
    test_suite='tests',
)
