import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    'nut2',
    'requests',
    'smtplib',
    ]

setup(name='webNUT',
      version='0.0.2',
      description='webNUT',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: System :: Power (UPS)",
        ],
      author='aenrione',
      author_email='aenrione@aenrione.xyz',
      url='https://github.com/aenrione/webNUT',
      keywords='web pyramid pylons nut network ups tools',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = webnut:main
      """,
      )
