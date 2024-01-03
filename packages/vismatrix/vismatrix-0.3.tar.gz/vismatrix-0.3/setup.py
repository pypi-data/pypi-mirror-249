from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='vismatrix',
      author='VolodyaHoi',
      version='0.3',
      description='Output matrix or table in beautiful form',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['vismatrix'],
      install_requires=['multipledispatch'],
      url="https://github.com/VolodyaHoi/vismatrix",
      author_email='i4masyrov@gmail.com',
      zip_safe=False)
