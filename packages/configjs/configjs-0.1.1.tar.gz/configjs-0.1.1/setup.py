from setuptools import setup, find_packages

setup(
    name='configjs',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
    },
    author='Doosik Kim',
    author_email='doosik71@gmail.com',
    description='A Python package to read "config.json" in the working directory and access its content using the package name itself.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/doosik71/configjs',
    license='MIT',
)
