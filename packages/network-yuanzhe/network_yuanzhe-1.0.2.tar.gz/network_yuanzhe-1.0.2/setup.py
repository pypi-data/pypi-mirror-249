from distutils.core import setup
from setuptools import find_packages
with open("README.md", "r") as f:
    long_description = f.read()
setup(name='network_yuanzhe',
      version='1.0.2',
      description='Build A Neural Network from Scratch',
      long_description=long_description,
      author='Yuanzhe Jia',
      author_email='jiayuanzhe1@gmail.com',
      install_requires=["numpy"],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries'
      ],
)
