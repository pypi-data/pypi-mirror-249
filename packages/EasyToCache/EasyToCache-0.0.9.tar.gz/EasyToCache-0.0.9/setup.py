from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='EasyToCache',
  version='0.0.9',
  author='MikoDam',
  author_email='kononov.mixa2045@gmail.com',
  description='This is simple module to cache using json.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/M1KoDam/EasyToCacheLib',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files cache json ',
  project_urls={
    'GitHub': 'https://github.com/M1KoDam/EasyToCacheLib'
  },
  python_requires='>=3.10'
)