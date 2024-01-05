from setuptools import setup

setup(
  name='neuq',
  version='0.1.2',
  packages=['neuq'],
  entry_points={
      'console_scripts': ['neuq=neuq.server:main']
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
  description="Supercharge your analysis with AI",
  include_package_data=True,
  # long_description=open('README.md').read(), #TODO
)