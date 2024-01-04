from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='pulpo-config',
      version='2.0.2',
      author='Mighty Pulpo',
      author_email='jayray.net@gmail.com',
      description='Simple configuration library',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
      ],
      python_requires='>=3.6',
      install_requires='pyyaml==6.0.1',
      keywords='configuration')