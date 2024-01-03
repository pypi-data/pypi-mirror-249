from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pyfoggl',
    version='0.1.2',
    author='Foggl dev',
    author_email='jerrybot123+foggl@gmail.com',
    description='A Python client for Foggl',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/foggl-client',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'requests>=2.25.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
