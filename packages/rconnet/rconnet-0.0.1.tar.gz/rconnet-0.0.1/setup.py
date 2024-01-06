from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='rconnet',
  version='0.0.1',
  author='VordyV',
  author_email='vordy.production@gmail.com',
  description='Python RCON client for the Battlefield 2142 server',
  long_description_content_type='text/markdown',
  long_description=readme(),
  url='https://github.com/VordyV/rconnet',
  packages=find_packages(),
  keywords='rcon client',
  python_requires='>=3.11'
)