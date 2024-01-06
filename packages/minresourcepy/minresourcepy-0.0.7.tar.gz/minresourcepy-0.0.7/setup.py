from setuptools import setup

# read the contents of the README file
from pathlib import Path
directory = Path(__file__).parent
long_description = (directory / "README.md").read_text()
  
setup( 
    name='minresourcepy', 
    version='0.0.7',
    description='Tools for Resource Geologists', 
    url = 'https://github.com/renanlo/MinResourcepy',
    author='Renan Lopes', 
    author_email='renanglopes@gmail.com', 
    license='MIT License',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[ 
        'numpy>=1.24.3',
        'pandas>=2.0.3',
        'transforms3d>=0.4.1',
        'plotly>=5.9.0',
        'matplotlib>=3.7.2'],
) 