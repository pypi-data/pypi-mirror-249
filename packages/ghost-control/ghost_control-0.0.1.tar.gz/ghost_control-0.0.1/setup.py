from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='ghost_control',  # 包名
      version='0.0.1',  # 版本号
      description='A package for ghost_box',
      long_description=long_description,
      author='zaixia108',
      author_email='zaixia108@gmail.com',
      url='',
      install_requires=[],
      license='GUN GPLv3 License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
