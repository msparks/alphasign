import setuptools
setuptools.setup(
  name = 'alphasign',
  version = '1.0',
  packages = setuptools.find_packages(),

  install_requires = ['pyserial>=2.4', 'pyusb>=1.0.0a2', 'pyyaml>=3.05'],

  author = 'Matt Sparks',
  author_email = 'ms@quadpoint.org',
  description = 'Implementation of the Alpha Sign Communications Protocol',
  long_description = ('Implementation of the Alpha Sign Communications '
                      'Protocol, which is used by many commercial LED signs, '
                      'including the Betabrite.'),
  url = 'https://github.com/msparks/alphasign',
  license = 'BSD',
)
