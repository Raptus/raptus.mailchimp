from setuptools import setup, find_packages
import os

version = '1.0b3'

setup(name='raptus.mailchimp',
      version=version,
      description="MailChimp plone integration",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Raptus',
      author_email='sriolo@raptus.com',
      url='raptus.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['raptus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'greatape'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      """,
      setup_requires=[ ],
      paster_plugins = [ ],
      )
