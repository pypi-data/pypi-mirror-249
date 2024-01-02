from setuptools import setup
from pathlib import Path
long_description = Path('README.md').read_text()
print(long_description)

setup(
    name='EasyDataR',
    version='1.0',
    description='EasyDataR is a unofficial R package to read in data from EasyData platform of the State Bank of Pakistan',
    long_description=long_description,
    author='Dr Ateeb Syed',
    url='https://github.com/drateeb/EasyDataR',
    long_description_content_type='text/markdown',
    keywords=['R', 'EasyData', 'EasyDataR'],
    install_requires=[
        'rpy2',
        'readme_md',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Programming Language :: Python'
    ],
)