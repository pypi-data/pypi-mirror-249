from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
  name='cleverdb',
  version='0.0.1',
  author='reques6e',
  author_email='none@gmail.com',
  description='A simple wrapper for working with SQLite in Python',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/reques6e/CloverDB',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='sqlite sqlite3 database wrapper sql',
  project_urls={
    'GitHub': 'https://github.com/reques6e/CloverDB'
  },
  python_requires='>=3.6'
)