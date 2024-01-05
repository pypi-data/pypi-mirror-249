from setuptools import setup

setup(
  name='neuq',
  version='0.1.0',
  packages=['./'],
  entry_points={
      'console_scripts': ['neuq=server:main']
  },
  install_requires=[
    'Flask==3.0.0',
    'Flask-Cors==4.0.0'
  ],
  classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
  ],
  description="Supercharge your analysis with the power of AI.",
  # long_description=open('README.md').read(), #TODO
)