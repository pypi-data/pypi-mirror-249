from setuptools import setup

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(name='slinn',
      version='1.1.6',
      description='HTTPS and HTTP server framework',
      packages=['slinn', 'slinn.default'],
      author='Mark Radin',
      author_email='mrybs2@gmail.com',
      url='https://slinn.miotp.ru/',
      long_description=readme(),
      long_description_content_type='text/markdown',
      python_requires='>=3.11',
      zip_safe=True)