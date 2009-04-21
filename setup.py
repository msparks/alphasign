import setuptools
setuptools.setup(
  name = 'alphasign',
  version = '0.9',
  packages = setuptools.find_packages(),

  install_requires = ['pyserial>=2.4', 'pyyaml>=3.05'],

  author = 'Matt Sparks',
  author_email = 'ms@quadpoint.org',
  description = 'Implementation of the Alpha Sign Communications Protocol',
  long_description = ('Implementation of the Alpha Sign Communications '
                      'Protocol, which is used by many commercial LED signs, '
                      'including the Betabrite.'),
  url = 'http://quadpoint.org/projects/alphasign',
  license = 'BSD',
)
